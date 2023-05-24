from dataclasses import dataclass
from typing import Any, Optional, Dict

from .device import Device, StartupEnum

from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub

# Quirks:
# TRADFRI control outlet / IKEA of Sweden:
# device has lightLevel attribute and canReceive capability, neither of
# them affect the state of relay.

@dataclass
class Outlet(Device):
    dirigera_client: AbstractSmartHomeHub
    is_reachable: bool
    is_on: bool
    startup_on_off: Optional[StartupEnum]

    def refresh(self) -> None:
        data = self.dirigera_client.get(route=f"/devices/{self.device_id}")
        attributes: Dict[str, Any] = data["attributes"]

        if "startupOnOff" in attributes:
            startup_on_off = StartupEnum(attributes.get("startupOnOff"))
        else:
            startup_on_off = None

        self.device_id = data["id"]
        self.is_reachable = data["isReachable"]
        self.custom_name = attributes["customName"]
        self.is_on = attributes["isOn"]
        self.startup_on_off = startup_on_off
        self.firmware_version = attributes.get("firmwareVersion")
        self.room_id = data["room"]["id"]
        self.room_name = data["room"]["name"]
        self.can_receive = data["capabilities"]["canReceive"]

    def set_name(self, name: str) -> None:
        if "customName" not in self.can_receive:
            raise AssertionError("This device does not support the customName capability")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.custom_name = name

    def set_on(self, outlet_on: bool) -> None:
        if "isOn" not in self.can_receive:
            raise AssertionError("This device does not support the isOn function")

        data = [{"attributes": {"isOn": outlet_on}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.is_on = outlet_on

    def set_startup_behaviour(self, behaviour: StartupEnum) -> None:
        """
        Sets the behaviour of the device in case of a power outage.
        When set to START_ON the device will turn on once the power is back.
        When set to START_OFF the device will stay off once the power is back.
        When set to START_PREVIOUS the device will resume its state at power outage.
        When set to START_TOGGLE, a sequence of power-off -> power-on, will toggle the device state
        """
        data = [{"attributes": {"startupOnOff": behaviour.value}}]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.startup_on_off = behaviour


def dict_to_outlet(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub):
    attributes: Dict[str, Any] = data["attributes"]

    if "startupOnOff" in attributes:
        startup_on_off = StartupEnum(attributes.get("startupOnOff"))
    else:
        startup_on_off = None

    return Outlet(
        dirigera_client=dirigera_client,
        device_id=data["id"],
        is_reachable=data["isReachable"],
        custom_name=attributes["customName"],
        is_on=attributes["isOn"],
        startup_on_off=startup_on_off,
        can_receive=data["capabilities"]["canReceive"],
        room_id=data["room"]["id"],
        room_name=data["room"]["name"],
        firmware_version=attributes.get("firmwareVersion"),
        hardware_version=attributes.get("hardwareVersion"),
        model=attributes.get("model"),
        manufacturer=attributes.get("manufacturer"),
        serial_number=attributes.get("serialNumber"),
    )
