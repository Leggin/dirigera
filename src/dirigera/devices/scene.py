from dataclasses import dataclass
from typing import Dict, Any, Optional

from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


@dataclass
class Scene:
    dirigera_client: AbstractSmartHomeHub
    scene_id: str
    name: str
    icon: str
    last_completed: Optional[str]
    last_triggered: Optional[str]
    last_undo: Optional[str]

    def refresh(self) -> None:
        data = self.dirigera_client.get(route=f"/scenes/{self.scene_id}")
        self.scene_id = data["id"]
        self.name = data["info"]["name"]
        self.icon = data["info"]["icon"]
        self.last_completed=data.get("lastCompleted")
        self.last_triggered=data.get("lastTriggered")
        self.last_undo=data.get("lastUndo")


    def trigger(self) -> None:
        self.dirigera_client.post(route=f"/scenes/{self.scene_id}/trigger")

    def undo(self) -> None:
        self.dirigera_client.post(route=f"/scenes/{self.scene_id}/undo")


def dict_to_scene(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub) -> Scene:
    return Scene(
        dirigera_client=dirigera_client,
        scene_id=data["id"],
        name=data["info"]["name"],
        icon=data["info"]["icon"],
        last_completed=data.get("lastCompleted"),
        last_triggered=data.get("lastTriggered"),
        last_undo=data.get("lastUndo")
    )
