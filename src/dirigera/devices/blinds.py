from __future__ import annotations
from typing import Any, Optional, Dict
from .device import Attributes, Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


class BlindAttributes(Attributes):
    blinds_current_level: Optional[int] = None
    blinds_target_level: Optional[int] = None
    blinds_state: Optional[str] = None
    battery_percentage: Optional[int] = None


class Blind(Device):
    dirigera_client: AbstractSmartHomeHub
    attributes: BlindAttributes

    def reload(self) -> Blind:
        data = self.dirigera_client.get(route=f"/devices/{self.id}")
        return Blind(dirigeraClient=self.dirigera_client, **data)

    def set_name(self, name: str) -> None:
        if "customName" not in self.capabilities.can_receive:
            raise AssertionError("This blind does not support the customName function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.custom_name = name

    def set_target_level(self, target_level: int) -> None:
        if "blindsTargetLevel" not in self.capabilities.can_receive:
            raise AssertionError(
                "This blind does not support the target level function"
            )

        if target_level < 0 or target_level > 100:
            raise AssertionError("target_level must be a value between 0 and 100")

        data = [{"attributes": {"blindsTargetLevel": target_level}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.blinds_target_level = target_level


def dict_to_blind(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub) -> Blind:
    return Blind(dirigeraClient=dirigera_client, **data)
