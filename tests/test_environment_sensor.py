from typing import Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.environment_sensor import (
    EnvironmentSensor,
    dict_to_environment_sensor,
)


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="sensor_dict")
def fixture_sensor_dict() -> Dict:
    return {
        "id": "75863f6a-d850-47f1-8a00-e31acdcae0e8_1",
        "type": "sensor",
        "deviceType": "environmentSensor",
        "createdAt": "2023-04-04T13:13:25.000Z",
        "isReachable": True,
        "lastSeen": "2023-10-28T14:19:24.000Z",
        "attributes": {
            "customName": "Envsensor",
            "model": "VINDSTYRKA",
            "manufacturer": "IKEA of Sweden",
            "firmwareVersion": "1.0.11",
            "hardwareVersion": "1",
            "serialNumber": "F4B3B1FFFE00101E",
            "productCode": "E2112",
            "currentTemperature": 21.1,
            "currentRH": 61,
            "currentPM25": 1,
            "maxMeasuredPM25": 999,
            "minMeasuredPM25": 0,
            "vocIndex": 63,
            "identifyStarted": "2000-01-01T00:00:00.000Z",
            "otaStatus": "upToDate",
            "otaState": "readyToCheck",
            "otaProgress": 0,
            "otaPolicy": "autoUpdate",
            "otaScheduleStart": "00:00",
            "otaScheduleEnd": "00:00",
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


@pytest.fixture(name="fake_sensor")
def fixture_sensor(
    fake_client: FakeDirigeraHub, sensor_dict: Dict
) -> EnvironmentSensor:
    return EnvironmentSensor(dirigeraClient=fake_client, **sensor_dict)


def test_set_name(fake_sensor: EnvironmentSensor, fake_client: FakeDirigeraHub) -> None:
    new_name = "staubsensor"
    fake_sensor.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_sensor.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_sensor.attributes.custom_name == new_name


def test_dict_to_sensor(fake_client: FakeDirigeraHub, sensor_dict: Dict) -> None:
    sensor = dict_to_environment_sensor(sensor_dict, fake_client)
    assert sensor.id == sensor_dict["id"]
    assert sensor.is_reachable == sensor_dict["isReachable"]
    assert sensor.attributes.custom_name == sensor_dict["attributes"]["customName"]
    assert (
        sensor.attributes.firmware_version
        == sensor_dict["attributes"]["firmwareVersion"]
    )
    assert (
        sensor.attributes.hardware_version
        == sensor_dict["attributes"]["hardwareVersion"]
    )
    assert sensor.attributes.model == sensor_dict["attributes"]["model"]
    assert sensor.attributes.serial_number == sensor_dict["attributes"]["serialNumber"]
    assert (
        sensor.attributes.current_temperature
        == sensor_dict["attributes"]["currentTemperature"]
    )
    assert sensor.attributes.current_r_h == sensor_dict["attributes"]["currentRH"]
    assert sensor.attributes.current_p_m25 == sensor_dict["attributes"]["currentPM25"]
    assert (
        sensor.attributes.max_measured_p_m25
        == sensor_dict["attributes"]["maxMeasuredPM25"]
    )
    assert (
        sensor.attributes.min_measured_p_m25
        == sensor_dict["attributes"]["minMeasuredPM25"]
    )
    assert sensor.attributes.voc_index == sensor_dict["attributes"]["vocIndex"]
    assert sensor.capabilities.can_receive == sensor_dict["capabilities"]["canReceive"]
    assert sensor.room.id == sensor_dict["room"]["id"]
    assert sensor.room.name == sensor_dict["room"]["name"]
    assert sensor.attributes.manufacturer == sensor_dict["attributes"]["manufacturer"]
