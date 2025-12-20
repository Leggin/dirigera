from __future__ import annotations
import datetime
from enum import Enum
from typing import Dict, Any, List, Optional, Union
from .base_ikea_model import BaseIkeaModel
from .device import Attributes
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


class SceneAttributes(Attributes):
    scene_id: str
    name: str
    icon: str
    last_completed: Optional[str] = None
    last_triggered: Optional[str] = None
    last_undo: Optional[str] = None


class Icon(Enum):
    SCENES_ARRIVE_HOME = "scenes_arrive_home"
    SCENES_BOOK = "scenes_book"
    SCENES_BRIEFCASE = "scenes_briefcase"
    SCENES_BRIGHTNESS_UP = "scenes_brightness_up"
    SCENES_BROOM = "scenes_broom"
    SCENES_CAKE = "scenes_cake"
    SCENES_CLAPPER = "scenes_clapper"
    SCENES_CLEAN_SPARKLES = "scenes_clean_sparkles"
    SCENES_CUTLERY = "scenes_cutlery"
    SCENES_DISCO_BALL = "scenes_disco_ball"
    SCENES_GAME_PAD = "scenes_game_pad"
    SCENES_GIFT_BAG = "scenes_gift_bag"
    SCENES_GIFT_BOX = "scenes_gift_box"
    SCENES_HEADPHONES = "scenes_headphones"
    SCENES_HEART = "scenes_heart"
    SCENES_HOME_FILLED = "scenes_home_filled"
    SCENES_HOT_DRINK = "scenes_hot_drink"
    SCENES_LADLE = "scenes_ladle"
    SCENES_LEAF = "scenes_leaf"
    SCENES_LEAVE_HOME = "scenes_leave_home"
    SCENES_MOON = "scenes_moon"
    SCENES_MUSIC_NOTE = "scenes_music_note"
    SCENES_PAINTING = "scenes_painting"
    SCENES_POPCORN = "scenes_popcorn"
    SCENES_POT_WITH_LID = "scenes_pot_with_lid"
    SCENES_SPEAKER_GENERIC = "scenes_speaker_generic"
    SCENES_SPRAY_BOTTLE = "scenes_spray_bottle"
    SCENES_SUITCASE = "scenes_suitcase"
    SCENES_SUITCASE_2 = "scenes_suitcase_2"
    SCENES_SUN_HORIZON = "scenes_sun_horizon"
    SCENES_TREE = "scenes_tree"
    SCENES_TROPHY = "scenes_trophy"
    SCENES_WAKE_UP = "scenes_wake_up"
    SCENES_WEIGHTS = "scenes_weights"
    SCENES_YOGA = "scenes_yoga"
    SCENES_COLD_DRINK_CONTENTS = "scenes_cold_drink_contents"
    SCENES_FLAME = "scenes_flame"
    SCENES_SNOWFLAKE = "scenes_snowflake"


class Info(BaseIkeaModel):
    name: str
    icon: Icon


class EndTriggerEvent(BaseIkeaModel):
    type: str
    trigger: TriggerDetails


class Trigger(BaseIkeaModel):
    id: Optional[str] = (
        None  # Optional to allow creation of Trigger instances for create_scene()
    )
    type: str
    triggered_at: Optional[datetime.datetime] = None
    disabled: bool
    trigger: Optional[TriggerDetails] = None
    next_trigger_at: Optional[datetime.datetime] = None
    end_trigger: Optional[EndTriggerEvent] = None
    end_trigger_event: Optional[EndTriggerEvent] = None


class TriggerDetails(BaseIkeaModel):
    days: Optional[List[str]] = None
    time: Optional[str] = None
    controllerType: Optional[ControllerType] = None
    buttonIndex: Optional[int] = None
    clickPattern: Optional[ClickPattern] = None
    deviceId: Optional[str] = None
    offset: Optional[int] = None
    type: Optional[str] = None


class ControllerType(Enum):
    SHORTCUT_CONTROLLER = "shortcutController"


class ClickPattern(Enum):
    LONG_PRESS = "longPress"
    DOUBLE_PRESS = "doublePress"
    SINGLE_PRESS = "singlePress"


class ActionAttributes(BaseIkeaModel, extra="allow"):
    is_on: Optional[bool] = None


class Action(BaseIkeaModel):
    id: str
    type: str
    enabled: Optional[bool] = None
    attributes: Optional[ActionAttributes] = None


class SceneType(Enum):
    USER_SCENE = "userScene"
    CUSTOM_SCENE = "customScene"
    PLAYLIST_SCENE = "playlistScene"
    WAKEUP_SCENE = "wakeUpScene"


class Scene(BaseIkeaModel):
    dirigera_client: AbstractSmartHomeHub
    id: str
    type: SceneType
    info: Info
    triggers: List[Trigger]
    actions: List[Action]
    created_at: datetime.datetime
    last_completed: Optional[datetime.datetime] = None
    last_triggered: Optional[datetime.datetime] = None
    last_undo: Optional[datetime.datetime] = None
    commands: List[Union[str, Dict[str, Any]]]
    undo_allowed_duration: int

    def reload(self) -> Scene:
        data = self.dirigera_client.get(route=f"/scenes/{self.id}")
        return Scene(dirigeraClient=self.dirigera_client, **data)

    def trigger(self) -> None:
        self.dirigera_client.post(route=f"/scenes/{self.id}/trigger")

    def undo(self) -> None:
        self.dirigera_client.post(route=f"/scenes/{self.id}/undo")


def dict_to_scene(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub) -> Scene:
    return Scene(dirigeraClient=dirigera_client, **data)
