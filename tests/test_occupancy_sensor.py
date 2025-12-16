from typing import Dict

import pytest

from src.dirigera.devices.occupancy_sensor import OccupancySensor, dict_to_occupancy_sensor
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="occupancy_sensor_dict")
def fixture_occupancy_sensor_dict() -> Dict:
    return {
        "id": "11111111-1111-1111-1111-111111111111_1",
        "type": "sensor",
        "deviceType": "occupancySensor",
        "createdAt": "2023-12-14T18:28:57.000Z",
        "isReachable": True,
        "lastSeen": "2023-12-14T17:30:48.000Z",
        "attributes": {
            "customName": "Occupancy",
            "firmwareVersion": "1.0.0",
            "hardwareVersion": "1",
            "manufacturer": "IKEA of Sweden",
            "model": "SOME OCCUPANCY SENSOR",
            "productCode": "E0000",
            "serialNumber": "AAAAAAAAAAAAAAAA",
            "batteryPercentage": 99,
            "isDetected": False,
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


@pytest.fixture(name="fake_occupancy_sensor")
def fixture_fake_occupancy_sensor(
    occupancy_sensor_dict: Dict, fake_client: FakeDirigeraHub
) -> OccupancySensor:
    return OccupancySensor(dirigeraClient=fake_client, **occupancy_sensor_dict)


def test_set_occupancy_sensor_name(
    fake_occupancy_sensor: OccupancySensor, fake_client: FakeDirigeraHub
) -> None:
    new_name = "occupancy_sensor_name"
    assert fake_occupancy_sensor.attributes.custom_name != new_name
    fake_occupancy_sensor.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_occupancy_sensor.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_occupancy_sensor.attributes.custom_name == new_name


def test_dict_to_occupancy_sensor(
    occupancy_sensor_dict: Dict, fake_client: FakeDirigeraHub
) -> None:
    sensor = dict_to_occupancy_sensor(occupancy_sensor_dict, fake_client)
    assert sensor.dirigera_client == fake_client
    assert sensor.id == occupancy_sensor_dict["id"]
    assert sensor.is_reachable == occupancy_sensor_dict["isReachable"]
    assert sensor.attributes.custom_name == occupancy_sensor_dict["attributes"]["customName"]
    assert (
        sensor.attributes.battery_percentage
        == occupancy_sensor_dict["attributes"]["batteryPercentage"]
    )
    assert sensor.attributes.is_detected == occupancy_sensor_dict["attributes"]["isDetected"]
