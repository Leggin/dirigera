from dataclasses import dataclass
from typing import Any, Dict

from .device import Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


@dataclass
class OpenCloseSensor(Device):
    dirigera_client: AbstractSmartHomeHub
    is_reachable: bool
    is_open: bool

    def refresh(self) -> None:
        data = self.dirigera_client.get(route=f"/devices/{self.device_id}")
        attributes: Dict[str, Any] = data["attributes"]
        self.firmware_version = attributes["firmwareVersion"]
        self.is_open = attributes["isOpen"]
        self.room_id = data["room"]["id"]
        self.room_name = data["room"]["name"]

    def set_name(self, name: str) -> None:
        if "customName" not in self.can_receive:
            raise AssertionError("This sensor does not support the set_name function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.custom_name = name


def dict_to_open_close_sensor(
    data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub
):
    attributes: Dict[str, Any] = data["attributes"]
    return OpenCloseSensor(
        dirigera_client=dirigera_client,
        device_id=data["id"],
        is_reachable=data["isReachable"],
        custom_name=attributes["customName"],
        firmware_version=attributes.get("firmwareVersion"),
        hardware_version=attributes.get("hardwareVersion"),
        model=attributes.get("model"),
        manufacturer=attributes.get("manufacturer"),
        serial_number=attributes.get("serialNumber"),
        is_open=attributes["isOpen"],
        room_id=data["room"]["id"],
        room_name=data["room"]["name"],
        can_receive=data["capabilities"]["canReceive"],
    )
