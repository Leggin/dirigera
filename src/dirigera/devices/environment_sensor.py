from __future__ import annotations
from typing import Any, Dict, Optional
from .device import Attributes, Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


class EnvironmentSensorAttributes(Attributes):
    current_temperature: Optional[float] = None
    current_r_h: Optional[int] = None
    current_p_m25: Optional[int] = None
    max_measured_p_m25: Optional[int] = None
    min_measured_p_m25: Optional[int] = None
    voc_index: Optional[int] = None
    battery_percentage: Optional[int] = None


class EnvironmentSensor(Device):
    dirigera_client: AbstractSmartHomeHub
    attributes: EnvironmentSensorAttributes

    def reload(self) -> EnvironmentSensor:
        data = self.dirigera_client.get(route=f"/devices/{self.id}")
        return EnvironmentSensor(dirigeraClient=self.dirigera_client, **data)

    def set_name(self, name: str) -> None:
        if "customName" not in self.capabilities.can_receive:
            raise AssertionError("This sensor does not support the set_name function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.custom_name = name


def dict_to_environment_sensor(
    data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub
) -> EnvironmentSensor:
    return EnvironmentSensor(dirigeraClient=dirigera_client, **data)
