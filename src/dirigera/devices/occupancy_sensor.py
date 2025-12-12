from __future__ import annotations
from typing import Any, Dict, Optional
from .device import Attributes, Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


class OccupancySensorAttributes(Attributes):
    battery_percentage: Optional[int] = None
    is_detected: Optional[bool] = None

class OccupancySensor(Device):
    dirigera_client: AbstractSmartHomeHub
    attributes: OccupancySensorAttributes

    def reload(self) -> OccupancySensor:
        data = self.dirigera_client.get(route=f"/devices/{self.id}")
        return OccupancySensor(dirigeraClient=self.dirigera_client, **data)

    def set_name(self, name: str) -> None:
        if "customName" not in self.capabilities.can_receive:
            raise AssertionError("This sensor does not support the set_name function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.custom_name = name


def dict_to_occupancy_sensor(
    data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub
) -> OccupancySensor:
    return OccupancySensor(dirigeraClient=dirigera_client, **data)
