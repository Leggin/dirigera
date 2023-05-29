from dataclasses import dataclass
from typing import Any, Optional, Dict

from .device import Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


@dataclass
class Controller(Device):
    dirigera_client: AbstractSmartHomeHub
    is_reachable: bool
    is_on: bool
    battery_percentage: Optional[int]

    def refresh(self):
        data = self.dirigera_client.get(route=f"/devices/{self.device_id}")
        attributes: Dict[str, Any] = data["attributes"]
        self.device_id = data["id"]
        self.is_reachable = data["isReachable"]
        self.custom_name = attributes["customName"]
        self.is_on = attributes["isOn"]
        self.battery_percentage = attributes.get("batteryPercentage")
        self.firmware_version = attributes.get("firmwareVersion")
        self.room_id = data["room"]["id"]
        self.can_receive = data["capabilities"]["canReceive"]
        self.room_name = data["room"]["name"]

    def set_name(self, name: str) -> None:
        if "customName" not in self.can_receive:
            raise AssertionError(
                "This controller does not support the set_name function"
            )

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(
            route=f"/devices/{self.device_id}", data=data
        )
        self.custom_name = name


def dict_to_controller(
    data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub
) -> Controller:
    attributes: Dict[str, Any] = data["attributes"]

    return Controller(
        dirigera_client=dirigera_client,
        device_id=data["id"],
        is_reachable=data["isReachable"],
        custom_name=attributes["customName"],
        is_on=attributes["isOn"],
        battery_percentage=attributes.get("batteryPercentage"),
        can_receive=data["capabilities"]["canReceive"],
        room_id=data["room"]["id"],
        room_name=data["room"]["name"],
        firmware_version=attributes.get("firmwareVersion"),
        hardware_version=attributes.get("hardwareVersion"),
        model=attributes.get("model"),
        manufacturer=attributes.get("manufacturer"),
        serial_number=attributes.get("serialNumber"),
    )
