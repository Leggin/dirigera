from __future__ import annotations
from typing import Any, Optional, Dict
from .device import Attributes, Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


class ControllerAttributes(Attributes):
    is_on: Optional[bool] = None
    battery_percentage: Optional[int] = None
    switch_label: Optional[str] = None


class Controller(Device):
    dirigera_client: AbstractSmartHomeHub
    attributes: ControllerAttributes

    def reload(self) -> Controller:
        data = self.dirigera_client.get(route=f"/devices/{self.id}")
        return Controller(dirigeraClient=self.dirigera_client, **data)

    def set_name(self, name: str) -> None:
        if "customName" not in self.capabilities.can_receive:
            raise AssertionError(
                "This controller does not support the set_name function"
            )

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.custom_name = name


def dict_to_controller(
    data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub
) -> Controller:
    return Controller(dirigeraClient=dirigera_client, **data)
