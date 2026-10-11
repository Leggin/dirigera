from typing import Dict

import pytest

from src.dirigera.devices.electrical_sensor import (
    ElectricalSensor,
    dict_to_electrical_sensor,
)
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="electrical_sensor_dict")
def fixture_electrical_sensor_dict() -> Dict:
    return {
        "id": "33333333-3333-3333-3333-333333333333_2",
        "relationId": "33333333-3333-3333-3333-333333333333",
        "type": "unknown",
        "deviceType": "electricalSensor",
        "createdAt": "2025-10-01T18:28:57.000Z",
        "isReachable": True,
        "lastSeen": "2025-10-02T17:30:48.000Z",
        "attributes": {
            "customName": "Grill Plug",
            "firmwareVersion": "1.0.0",
            "hardwareVersion": "1",
            "manufacturer": "IKEA of Sweden",
            "model": "GRILLPLATS Plug",
            "productCode": "E2491-EU",
            "serialNumber": "CCCCCCCCCCCCCCCC",
            "currentActivePower": 1.4,
            "currentAmps": 0.022,
            "currentVoltage": 229,
            "energyConsumedAtLastReset": 0,
            "totalEnergyConsumed": 0.706,
            "totalEnergyConsumedLastUpdated": "2025-10-02T17:30:48.000Z",
            "timeOfLastEnergyReset": "2025-10-01T18:28:57.000Z",
        },
        "capabilities": {"canSend": [], "canReceive": ["customName"]},
        "room": {
            "id": "acaff5ef-2840-45a9-bbc9-19aa77553369",
            "name": "Living room",
            "color": "ikea_green_no_65",
            "icon": "rooms_sofa",
        },
        "deviceSet": [],
        "remoteLinks": [],
        "isHidden": False,
    }


@pytest.fixture(name="fake_electrical_sensor")
def fixture_fake_electrical_sensor(
    electrical_sensor_dict: Dict, fake_client: FakeDirigeraHub
) -> ElectricalSensor:
    return ElectricalSensor(dirigeraClient=fake_client, **electrical_sensor_dict)


def test_set_electrical_sensor_name(
    fake_electrical_sensor: ElectricalSensor, fake_client: FakeDirigeraHub
) -> None:
    new_name = "electrical_sensor_name"
    assert fake_electrical_sensor.attributes.custom_name != new_name
    fake_electrical_sensor.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_electrical_sensor.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_electrical_sensor.attributes.custom_name == new_name


def test_dict_to_electrical_sensor(
    electrical_sensor_dict: Dict, fake_client: FakeDirigeraHub
) -> None:
    sensor = dict_to_electrical_sensor(electrical_sensor_dict, fake_client)
    attributes = electrical_sensor_dict["attributes"]
    assert sensor.dirigera_client == fake_client
    assert sensor.id == electrical_sensor_dict["id"]
    assert sensor.relation_id == electrical_sensor_dict["relationId"]
    assert sensor.is_reachable == electrical_sensor_dict["isReachable"]
    assert sensor.attributes.custom_name == attributes["customName"]
    assert sensor.attributes.current_active_power == attributes["currentActivePower"]
    assert sensor.attributes.current_amps == attributes["currentAmps"]
    assert sensor.attributes.current_voltage == attributes["currentVoltage"]
    assert (
        sensor.attributes.energy_consumed_at_last_reset
        == attributes["energyConsumedAtLastReset"]
    )
    assert sensor.attributes.total_energy_consumed == attributes["totalEnergyConsumed"]
    assert sensor.attributes.total_energy_consumed_last_updated is not None
    assert sensor.attributes.time_of_last_energy_reset is not None
