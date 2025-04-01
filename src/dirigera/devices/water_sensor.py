from __future__ import annotations
from typing import Any, Dict, Optional
from .device import Attributes, Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub

class WaterSensorAttributes(Attributes):
    battery_percentage: Optional[int] = None
    water_leak_detected: bool

class WaterSensor(Device):
    dirigera_client: AbstractSmartHomeHub
    attributes: WaterSensorAttributes

    def reload(self) -> WaterSensor:
        data = self.dirigera_client.get(route=f"/devices/{self.id}")
        return WaterSensor(dirigeraClient=self.dirigera_client, **data)

    def set_name(self, name: str) -> None:
        if "customName" not in self.capabilities.can_receive:
            raise AssertionError("This sensor does not support the set_name function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.custom_name = name

def dict_to_water_sensor(
    data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub
) -> WaterSensor:
    return WaterSensor(dirigeraClient=dirigera_client, **data)
