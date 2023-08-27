from dataclasses import dataclass
from typing import Dict, Any

from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


@dataclass
class Scene:
    dirigera_client: AbstractSmartHomeHub
    scene_id: str
    name: str
    icon: str

    def trigger(self) -> None:
        self.dirigera_client.post(route=f"/scenes/{self.scene_id}/trigger")


def dict_to_scene(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub) -> Scene:
    return Scene(
        dirigera_client=dirigera_client,
        scene_id=data["id"],
        name=data["info"]["name"],
        icon=data["info"]["icon"]
    )
