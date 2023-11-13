from __future__ import annotations
from typing import Any, Optional, Dict
from .device import Attributes, Device, StartupEnum
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


class LightAttributes(Attributes):
    startup_on_off: Optional[StartupEnum] = None
    is_on: bool
    light_level: Optional[int] = None
    color_temperature: Optional[int] = None
    color_temperature_min: Optional[int] = None
    color_temperature_max: Optional[int] = None
    color_hue: Optional[float] = None
    color_saturation: Optional[float] = None


class Light(Device):
    dirigera_client: AbstractSmartHomeHub
    attributes: LightAttributes

    def reload(self) -> Light:
        data = self.dirigera_client.get(route=f"/devices/{self.id}")
        return Light(dirigeraClient=self.dirigera_client, **data)

    def set_name(self, name: str) -> None:
        if "customName" not in self.capabilities.can_receive:
            raise AssertionError("This lamp does not support the swith-off function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.custom_name = name

    def set_light(self, lamp_on: bool) -> None:
        if "isOn" not in self.capabilities.can_receive:
            raise AssertionError("This lamp does not support the swith-off function")

        data = [{"attributes": {"isOn": lamp_on}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.is_on = lamp_on

    def set_light_level(self, light_level: int) -> None:
        if "lightLevel" not in self.capabilities.can_receive:
            raise AssertionError(
                "This lamp does not support the set lightLevel function"
            )
        if light_level < 1 or light_level > 100:
            raise ValueError("light_level must be a value between 1 and 100")

        data = [{"attributes": {"lightLevel": light_level}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.light_level = light_level

    def set_color_temperature(self, color_temp: int) -> None:
        if "colorTemperature" not in self.capabilities.can_receive:
            raise AssertionError(
                "This lamp does not support the set colorTemperature function"
            )
        if (
            self.attributes.color_temperature_max is None
            or self.attributes.color_temperature_min is None
        ):
            raise ValueError("Values of color_temp_max or color_temp_min are None")
        if (
            color_temp < self.attributes.color_temperature_max
            or color_temp > self.attributes.color_temperature_min
        ):
            raise ValueError(
                "color_temperature must be a value between "
                f"{self.attributes.color_temperature_max} and {self.attributes.color_temperature_min}"
            )

        data = [{"attributes": {"colorTemperature": color_temp}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.color_temperature = color_temp

    def set_light_color(self, hue: float, saturation: float) -> None:
        if (
            "colorHue" not in self.capabilities.can_receive
            or "colorSaturation" not in self.capabilities.can_receive
        ):
            raise AssertionError(
                "This lamp does not support the set light color function"
            )
        if hue < 0 or hue > 360:
            raise ValueError("hue must be a value between 0 and 360")
        if saturation < 0.0 or saturation > 1.0:
            raise ValueError("saturation must be a value between 0.0 and 1.0")

        data = [{"attributes": {"colorHue": hue, "colorSaturation": saturation}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.color_hue = hue
        self.attributes.color_saturation = saturation

    def set_startup_behaviour(self, behaviour: StartupEnum) -> None:
        """
        Sets the behaviour of the lamp in case of a power outage.
        When set to START_ON the lamp will turn on once the power is back.
        When set to START_OFF the lamp will stay off once the power is back.
        When set to START_PREVIOUS the lamp will resume its state at power outage.
        When set to START_TOGGLE, a sequence of power-off -> power-on, will toggle the lamp state
        """
        data = [{"attributes": {"startupOnOff": behaviour.value}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.startup_on_off = behaviour


def dict_to_light(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub) -> Light:
    return Light(
        dirigeraClient=dirigera_client,
        **data,
    )
