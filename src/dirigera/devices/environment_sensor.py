from dataclasses import dataclass
from typing import Any
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


@dataclass
class EnvironmentSensor:
    dirigera_client: AbstractSmartHomeHub
    device_id: str
    is_reachable: bool
    custom_name: str
    firmware_version: str
    hardware_version: str
    model: str
    product_code: str
    serial_number: str
    current_temperature: str
    current_rh: int
    current_pm25: int
    max_measured_pm25: int
    min_measured_pm25: int
    voc_index: int
    can_receive: list[str]

    def refresh(self) -> None:
        data = self.dirigera_client.get(route=f"/devices/{self.device_id}")
        attributes: dict[str, Any] = data["attributes"]
        self.firmware_version = attributes["firmwareVersion"]
        self.current_temperature = attributes["currentTemperature"]
        self.current_rh = attributes["currentRH"]
        self.current_pm25 = attributes["currentPM25"]
        self.voc_index = attributes["vocIndex"]

    def set_name(self, name: str) -> None:
        if "customName" not in self.can_receive:
            raise AssertionError("This sensor does not support the set_name function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.custom_name = name


def dict_to_environment_sensor(data: dict[str, Any], dirigera_client: AbstractSmartHomeHub):
    attributes: dict[str, Any] = data["attributes"]
    return EnvironmentSensor(
        dirigera_client=dirigera_client,
        device_id=data["id"],
        is_reachable=data["isReachable"],
        custom_name=attributes["customName"],
        firmware_version=attributes["firmwareVersion"],
        hardware_version=attributes["hardwareVersion"],
        model=attributes["model"],
        product_code=attributes["productCode"],
        serial_number=attributes["serialNumber"],
        current_temperature=attributes["currentTemperature"],
        current_rh=attributes["currentRH"],
        current_pm25=attributes["currentPM25"],
        max_measured_pm25=attributes["maxMeasuredPM25"],
        min_measured_pm25=attributes["minMeasuredPM25"],
        voc_index=attributes["vocIndex"],
        can_receive=data["capabilities"]["canReceive"],
    )
