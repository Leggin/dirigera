from __future__ import annotations
import datetime
from typing import Any, Dict, Optional
from .device import Attributes, Device
from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


class ElectricalSensorAttributes(Attributes):
    current_active_power: Optional[float] = None
    current_amps: Optional[float] = None
    current_voltage: Optional[float] = None
    energy_consumed_at_last_reset: Optional[float] = None
    total_energy_consumed: Optional[float] = None
    total_energy_consumed_last_updated: Optional[datetime.datetime] = None
    time_of_last_energy_reset: Optional[datetime.datetime] = None


class ElectricalSensor(Device):
    dirigera_client: AbstractSmartHomeHub
    attributes: ElectricalSensorAttributes

    def reload(self) -> ElectricalSensor:
        data = self.dirigera_client.get(route=f"/devices/{self.id}")
        return ElectricalSensor(dirigeraClient=self.dirigera_client, **data)

    def set_name(self, name: str) -> None:
        if "customName" not in self.capabilities.can_receive:
            raise AssertionError("This sensor does not support the set_name function")

        data = [{"attributes": {"customName": name}}]
        self.dirigera_client.patch(route=f"/devices/{self.id}", data=data)
        self.attributes.custom_name = name


def dict_to_electrical_sensor(
    data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub
) -> ElectricalSensor:
    return ElectricalSensor(dirigeraClient=dirigera_client, **data)
