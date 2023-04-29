from dataclasses import dataclass
from typing import Any, Optional, Dict

from .device import Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


@dataclass
class Blind(Device):
    dirigera_client: AbstractSmartHomeHub
    is_reachable: bool
    current_level: Optional[int]
    target_level: Optional[int]
    state: Optional[str]

    def refresh(self) -> None:
        data = self.dirigera_client.get(route=f"/devices/{self.device_id}")
        attributes: Dict[str, Any] = data["attributes"]
        self.device_id = data["id"]
        self.is_reachable = data["isReachable"]
        self.custom_name = attributes["customName"]
        self.current_level = attributes.get("blindsCurrentLevel")
        self.target_level = attributes.get("blindsTargetLevel")
        self.state = attributes.get("blindsState")
        self.firmware_version = attributes.get("firmwareVersion")
        self.room_id = data["room"]["id"]
        self.room_name = data["room"]["name"]
        self.can_receive = data["capabilities"]["canReceive"]

    def set_name(self, name: str) -> None:
        if "customName" not in self.can_receive:
            raise AssertionError("This blind does not support the customName function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.custom_name = name

    def set_target_level(self, target_level: int) -> None:
        if "blindsTargetLevel" not in self.can_receive:
            raise AssertionError("This blind does not support the target level function")

        if target_level < 0 or target_level > 100:
            raise AssertionError("target_level must be a value between 0 and 100")

        data = [{"attributes": {"blindsTargetLevel": target_level}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.target_level = target_level


def dict_to_blind(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub) -> Blind:
    attributes: Dict[str, Any] = data["attributes"]

    return Blind(
        dirigera_client=dirigera_client,
        device_id=data["id"],
        is_reachable=data["isReachable"],
        custom_name=attributes["customName"],
        target_level=attributes["blindsTargetLevel"],
        current_level=attributes["blindsCurrentLevel"],
        state=attributes["blindsState"],
        can_receive=data["capabilities"]["canReceive"],
        room_id=data["room"]["id"],
        room_name=data["room"]["name"],
        firmware_version=attributes.get("firmwareVersion"),
        hardware_version=attributes.get("hardwareVersion"),
        model=attributes.get("model"),
        manufacturer=attributes.get("manufacturer"),
        serial_number=attributes.get("serialNumber"),
    )
