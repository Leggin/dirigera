from dataclasses import dataclass
from typing import Any

from .device import Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


@dataclass
class EnvironmentSensor(Device):
    dirigera_client: AbstractSmartHomeHub
    is_reachable: bool
    current_temperature: str
    current_rh: int
    current_pm25: int
    max_measured_pm25: int
    min_measured_pm25: int
    voc_index: int

    def refresh(self) -> None:
        data = self.dirigera_client.get(route=f"/devices/{self.device_id}")
        attributes: dict[str, Any] = data["attributes"]
        self.firmware_version = attributes["firmwareVersion"]
        self.current_temperature = attributes["currentTemperature"]
        self.current_rh = attributes["currentRH"]
        self.current_pm25 = attributes["currentPM25"]
        self.voc_index = attributes["vocIndex"]
        self.room_id = data["room"]["id"]
        self.room_name = data["room"]["name"]

    def set_name(self, name: str) -> None:
        if "customName" not in self.can_receive:
            raise AssertionError("This sensor does not support the set_name function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.custom_name = name


def dict_to_environment_sensor(
    data: dict[str, Any], dirigera_client: AbstractSmartHomeHub
):
    attributes: dict[str, Any] = data["attributes"]
    return EnvironmentSensor(
        dirigera_client=dirigera_client,
        device_id=data["id"],
        is_reachable=data["isReachable"],
        custom_name=attributes["customName"],
        firmware_version=attributes.get("firmwareVersion"),
        hardware_version=attributes.get("hardwareVersion"),
        model=attributes.get("model"),
        manufacturer=attributes.get("manufacturer"),
        serial_number=attributes.get("serialNumber"),
        current_temperature=attributes["currentTemperature"],
        current_rh=attributes["currentRH"],
        current_pm25=attributes["currentPM25"],
        max_measured_pm25=attributes["maxMeasuredPM25"],
        min_measured_pm25=attributes["minMeasuredPM25"],
        voc_index=attributes["vocIndex"],
        room_id=data["room"]["id"],
        room_name=data["room"]["name"],
        can_receive=data["capabilities"]["canReceive"],
    )
