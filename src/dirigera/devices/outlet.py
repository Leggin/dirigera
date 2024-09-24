from __future__ import annotations
import datetime
from typing import Any, Optional, Dict
from .device import Attributes, Device, StartupEnum
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub

# Quirks:
# TRADFRI control outlet / IKEA of Sweden:
# device has lightLevel attribute and canReceive capability, neither of
# them affect the state of relay.


class OutletAttributes(Attributes):
    is_on: bool
    startup_on_off: Optional[StartupEnum] = None
    status_light: Optional[bool] = None
    identify_period: Optional[int] = None
    permitting_join: Optional[bool] = None
    energy_consumed_at_last_reset: Optional[float] = None
    current_active_power: Optional[float] = None
    current_amps: Optional[float] = None
    current_voltage: Optional[float] = None
    total_energy_consumed: Optional[float] = None
    total_energy_consumed_last_updated: Optional[datetime.datetime] = None
    time_of_last_energy_reset: Optional[datetime.datetime] = None


class Outlet(Device):
    dirigera_client: AbstractSmartHomeHub
    attributes: OutletAttributes

    def reload(self) -> Outlet:
        data = self.dirigera_client.get(route=f"/devices/{self.id}")
        return Outlet(dirigeraClient=self.dirigera_client, **data)

    def set_name(self, name: str) -> None:
        if "customName" not in self.capabilities.can_receive:
            raise AssertionError(
                "This device does not support the customName capability"
            )

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.custom_name = name

    def set_on(self, outlet_on: bool) -> None:
        if "isOn" not in self.capabilities.can_receive:
            raise AssertionError("This device does not support the isOn function")

        data = [{"attributes": {"isOn": outlet_on}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.is_on = outlet_on

    def set_startup_behaviour(self, behaviour: StartupEnum) -> None:
        """
        Sets the behaviour of the device in case of a power outage.
        When set to START_ON the device will turn on once the power is back.
        When set to START_OFF the device will stay off once the power is back.
        When set to START_PREVIOUS the device will resume its state at power outage.
        When set to START_TOGGLE, a sequence of power-off -> power-on, will toggle the device state
        """
        data = [{"attributes": {"startupOnOff": behaviour.value}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.startup_on_off = behaviour


def dict_to_outlet(
    data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub
) -> Outlet:
    return Outlet(dirigeraClient=dirigera_client, **data)
