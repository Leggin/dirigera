from typing import Dict

import pytest

from src.dirigera.devices.light_sensor import LightSensor, dict_to_light_sensor
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="light_sensor_dict")
def fixture_light_sensor_dict() -> Dict:
    return {
        "id": "22222222-2222-2222-2222-222222222222_1",
        "type": "sensor",
        "deviceType": "lightSensor",
        "createdAt": "2023-12-14T18:28:57.000Z",
        "isReachable": True,
        "lastSeen": "2023-12-14T17:30:48.000Z",
        "attributes": {
            "customName": "Light Sensor",
            "firmwareVersion": "1.0.0",
            "hardwareVersion": "1",
            "manufacturer": "IKEA of Sweden",
            "model": "SOME LIGHT SENSOR",
            "productCode": "E0001",
            "serialNumber": "BBBBBBBBBBBBBBBB",
            "batteryPercentage": 88,
            "illuminance": 21790,
            "maxIlluminance": 40001,
            "minIlluminance": 1,
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


@pytest.fixture(name="fake_light_sensor")
def fixture_fake_light_sensor(
    light_sensor_dict: Dict, fake_client: FakeDirigeraHub
) -> LightSensor:
    return LightSensor(dirigeraClient=fake_client, **light_sensor_dict)


def test_set_light_sensor_name(
    fake_light_sensor: LightSensor, fake_client: FakeDirigeraHub
) -> None:
    new_name = "light_sensor_name"
    assert fake_light_sensor.attributes.custom_name != new_name
    fake_light_sensor.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light_sensor.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_light_sensor.attributes.custom_name == new_name


def test_dict_to_light_sensor(light_sensor_dict: Dict, fake_client: FakeDirigeraHub) -> None:
    sensor = dict_to_light_sensor(light_sensor_dict, fake_client)
    assert sensor.dirigera_client == fake_client
    assert sensor.id == light_sensor_dict["id"]
    assert sensor.is_reachable == light_sensor_dict["isReachable"]
    assert sensor.attributes.custom_name == light_sensor_dict["attributes"]["customName"]
    assert sensor.attributes.battery_percentage == light_sensor_dict["attributes"]["batteryPercentage"]
    assert sensor.attributes.illuminance == light_sensor_dict["attributes"]["illuminance"]
    assert sensor.attributes.max_illuminance == light_sensor_dict["attributes"]["maxIlluminance"]
    assert sensor.attributes.min_illuminance == light_sensor_dict["attributes"]["minIlluminance"]
