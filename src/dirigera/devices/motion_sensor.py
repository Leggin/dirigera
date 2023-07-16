from dataclasses import dataclass
from typing import Any, Dict

from .controller import Controller
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


@dataclass
class MotionSensor(Controller):
    dirigera_client: AbstractSmartHomeHub
    is_reachable: bool
    is_on = bool
    sensor_configuration: dict
    on_duration = int
    schedule = dict

    def refresh(self) -> None:
        data = self.dirigera_client.get(route=f"/devices/{self.device_id}")
        attributes: Dict[str, Any] = data["attributes"]
        self.firmware_version = attributes["firmwareVersion"]
        self.is_on = attributes['isOn']
        self.room_id = data["room"]["id"]
        self.room_name = data["room"]["name"]
        self.sensor_configuration = attributes["sensorConfig"]
        self.on_duration = self.sensor_configuration["onDuration"]
        self.schedule = self.sensor_configuration['schedule']

    def set_name(self, name: str) -> None:
        if "customName" not in self.can_receive:
            raise AssertionError("This sensor does not support the set_name function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.custom_name = name

    def set_on_duration(self, duration: int) -> None:
        data = [{"attributes": {"sensorConfig": {"onDuration": duration}}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.on_duration = duration

    def get_configuration(self) -> dict:
        return self.sensor_configuration

    def get_on_duration(self) -> dict:
        return {'on_duration': self.on_duration}

    def get_schedule(self) -> dict:
        return {'schedule': self.schedule}


def dict_to_motion_sensor(
    data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub
):
    attributes: Dict[str, Any] = data["attributes"]
    return MotionSensor(
        dirigera_client=dirigera_client,
        device_id=data["id"],
        is_reachable=data["isReachable"],
        custom_name=attributes["customName"],
        firmware_version=attributes.get("firmwareVersion"),
        hardware_version=attributes.get("hardwareVersion"),
        model=attributes.get("model"),
        manufacturer=attributes.get("manufacturer"),
        serial_number=attributes.get("serialNumber"),
        is_on=attributes["isOn"],
        room_id=data["room"]["id"],
        room_name=data["room"]["name"],
        can_receive=data["capabilities"]["canReceive"],
        battery_percentage=attributes["batteryPercentage"],
        sensor_configuration=attributes["sensorConfig"]
    )
