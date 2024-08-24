from __future__ import annotations
from enum import Enum
from typing import Any, Dict
from .device import Attributes, Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub

class FanModeEnum(Enum):
    OFF = "off"
    ON = "on"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTO = "auto"

class AirPurifierAttributes(Attributes):
    """canReceive"""
    fan_mode: FanModeEnum
    fan_mode_sequence: str
    motor_state: int
    child_lock: bool
    status_light: bool
    """readOnly"""
    motor_runtime: int
    filter_alarm_status: bool
    filter_elapsed_time: int
    filter_lifetime: int
    current_p_m25: int

class AirPurifier(Device):
    dirigera_client: AbstractSmartHomeHub
    attributes: AirPurifierAttributes

    def reload(self) -> AirPurifier:
        data = self.dirigera_client.get(route=f"/devices/{self.id}")
        return AirPurifier(dirigeraClient=self.dirigera_client, **data)

    def set_name(self, name: str) -> None:
        if "customName" not in self.capabilities.can_receive:
            raise AssertionError("This airpurifier does not support the set_name function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.custom_name = name

    def set_fan_mode(self, fan_mode: FanModeEnum) -> None:
        data = [{"attributes": {"fanMode": fan_mode.value}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.fan_mode = fan_mode

    def set_motor_state(self, motor_state: int) -> None:
        """
        Sets the fan behaviour.
        Values 0 to 50 allowed.
        0 == off
        1 == auto
        """
        desired_motor_state = int(motor_state)
        if desired_motor_state < 0 or desired_motor_state > 50:
            raise ValueError("Motor state must be a value between 0 and 50")

        data = [{"attributes": {"motorState": desired_motor_state}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.motor_state = desired_motor_state

    def set_child_lock(self, child_lock: bool) -> None:
        if "childLock" not in self.capabilities.can_receive:
            raise AssertionError("This air-purifier does not support the child lock function")

        data = [{"attributes": {"childLock": child_lock}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.child_lock = child_lock

    def set_status_light(self, light_state: bool) -> None:
        data = [{"attributes": {"statusLight": light_state}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.status_light = light_state

def dict_to_air_purifier(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub) -> AirPurifier:
    return AirPurifier(
        dirigeraClient=dirigera_client,
        **data
    )
