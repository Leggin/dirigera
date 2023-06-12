from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Dict, List, Union

from .device import Device

from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


class FanModeEnum(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTO = "auto"


@dataclass
class AirPurifier(Device):
    dirigera_client: AbstractSmartHomeHub
    is_reachable: bool
    fan_mode: FanModeEnum
    fan_mode_sequence: str
    is_child_lock_on: bool
    is_status_light_on: bool
    motor_runtime: int
    motor_state: int
    filter_change_needed: bool
    filter_elapsed_time: int
    filter_lifetime: int
    current_pm25: int

    def refresh(self) -> None:
        """Use stored device id to refresh all data of device."""
        fresh_data = self.dirigera_client.get(route=f"/devices/{self.device_id}")
        attributes: Dict[str, Any] = fresh_data["attributes"]
        self.device_id = fresh_data["id"]
        self.is_reachable = fresh_data["isReachable"]
        self.custom_name = attributes["customName"]
        self.can_receive = fresh_data["capabilities"]["canReceive"]
        self.room_id = fresh_data["room"]["id"]
        self.room_name = fresh_data["room"]["name"]

        self.firmware_version = attributes.get("firmwareVersion")
        self.hardware_version = attributes.get("hardwareVersion")
        self.model = attributes.get("model")
        self.manufacturer = attributes.get("manufacturer")
        self.serial_number = attributes.get("serialNumber")
        self.fan_mode = FanModeEnum(attributes.get("fanMode"))
        self.fan_mode_sequence = attributes.get("fanModeSequence")
        self.motor_state = attributes.get("motorState")
        self.motor_runtime = attributes.get("motorRuntime")
        self.is_child_lock_on = attributes.get("childLock")
        self.filter_change_needed = attributes.get("filterAlarmStatus")
        self.filter_elapsed_time = attributes.get("filterElapsedTime")
        self.filter_lifetime = attributes.get("filterLifetime")
        self.current_pm25 = attributes.get("currentPM25")
        self.is_status_light_on = attributes.get("statusLight")

    def _send_data(self, data: Dict) -> None:
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=[data])
        self.refresh()

    def set_fan_mode(self, fan_mode: FanModeEnum) -> None:
        """Sets the fan mode (low, medium, high, auto)."""
        self._send_data(data={"attributes": {"fanMode": fan_mode.value}})

    def set_motor_state(self, motor_state) -> None:
        """Set the motor speed. Accepted values: 0-50.

        Notes:
        - values <10 are interpreted as "set mode to auto"
        - values will be rounded down to multiples of 5
          (e.g. 17 gets interpreted as 15)
        """
        desired_motor_state = int(motor_state)
        if desired_motor_state < 0 or desired_motor_state > 50:
            raise ValueError("Value must be in range 0-50")
        self._send_data(data={"attributes": {"motorState": desired_motor_state}})

    def set_child_lock(self, child_lock: bool) -> None:
        """Call with True to enable child lock, False for disable."""
        self._send_data({"attributes": {"childLock": child_lock}})

    def set_status_light(self, light_state: bool) -> None:
        """Call with False to disable the status lights.

        Note: changing values (e.g. motor state, child lock) can lead to the
        status light to light up again, requiring to set the value to False again.
        """
        self._send_data({"attributes": {"statusLight": light_state}})


def dict_to_air_purifier(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub):
    attributes: Dict[str, Any] = data["attributes"]

    return AirPurifier(
        dirigera_client=dirigera_client,
        device_id=data["id"],
        is_reachable=data["isReachable"],
        custom_name=attributes["customName"],
        can_receive=data["capabilities"]["canReceive"],
        room_id=data["room"]["id"],
        room_name=data["room"]["name"],
        firmware_version=attributes.get("firmwareVersion"),
        hardware_version=attributes.get("hardwareVersion"),
        model=attributes.get("model"),
        manufacturer=attributes.get("manufacturer"),
        serial_number=attributes.get("serialNumber"),
        fan_mode=attributes.get("fanMode"),
        fan_mode_sequence=attributes.get("fanModeSequence"),
        motor_state=attributes.get("motorState"),
        motor_runtime=attributes.get("motorRuntime"),
        is_child_lock_on=attributes.get("childLock"),
        filter_change_needed=attributes.get("filterAlarmStatus"),
        filter_elapsed_time=attributes.get("filterElapsedTime"),
        filter_lifetime=attributes.get("filterLifetime"),
        current_pm25=attributes.get("currentPM25"),
        is_status_light_on=attributes.get("statusLight"),
    )
