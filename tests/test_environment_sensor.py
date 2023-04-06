import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.environment_sensor import (
    EnvironmentSensor,
    dict_to_environment_sensor,
)


@pytest.fixture(name="fake_client")
def fixture_fake_client():
    return FakeDirigeraHub()


@pytest.fixture(name="fake_sensor")
def fixture_sensor(fake_client: FakeDirigeraHub):
    return EnvironmentSensor(
        dirigera_client=fake_client,
        device_id="abc",
        is_reachable=True,
        custom_name="abc",
        firmware_version="abc",
        hardware_version="abc",
        model="abc",
        serial_number="abc",
        current_temperature="abc",
        current_rh=50,
        current_pm25=5,
        max_measured_pm25=999,
        min_measured_pm25=0,
        voc_index=200,
        room_id="123",
        room_name="upstairs",
        manufacturer="IKEA",
        can_receive=[
            "customName",
        ],
    )


@pytest.fixture(name="sensor_dict")
def fixture_sensor_dict():
    return {
        "id": "abc123",
        "isReachable": True,
        "attributes": {
            "customName": "Sensor 1",
            "firmwareVersion": "1.0.11",
            "hardwareVersion": "1",
            "model": "VINDSTYRKA",
            "productCode": "E2E2E",
            "serialNumber": "FFB123",
            "currentTemperature": 19,
            "currentRH": 55,
            "currentPM25": 3,
            "maxMeasuredPM25": 999,
            "minMeasuredPM25": 0,
            "vocIndex": 227,
            "manufacturer": "IKEA",
        },
        "room": {"id": "123", "name": "upstairs"},
        "capabilities": {"canSend": [], "canReceive": ["customName"]},
    }


def test_set_name(fake_sensor: EnvironmentSensor, fake_client: FakeDirigeraHub):
    new_name = "staubsensor"
    fake_sensor.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_sensor.device_id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_sensor.custom_name == new_name


def test_dict_to_sensor(fake_client: FakeDirigeraHub, sensor_dict: dict):
    sensor = dict_to_environment_sensor(sensor_dict, fake_client)
    assert sensor.device_id == sensor_dict["id"]
    assert sensor.is_reachable == sensor_dict["isReachable"]
    assert sensor.custom_name == sensor_dict["attributes"]["customName"]
    assert sensor.firmware_version == sensor_dict["attributes"]["firmwareVersion"]
    assert sensor.hardware_version == sensor_dict["attributes"]["hardwareVersion"]
    assert sensor.model == sensor_dict["attributes"]["model"]
    assert sensor.serial_number == sensor_dict["attributes"]["serialNumber"]
    assert sensor.current_temperature == sensor_dict["attributes"]["currentTemperature"]
    assert sensor.current_rh == sensor_dict["attributes"]["currentRH"]
    assert sensor.current_pm25 == sensor_dict["attributes"]["currentPM25"]
    assert sensor.max_measured_pm25 == sensor_dict["attributes"]["maxMeasuredPM25"]
    assert sensor.min_measured_pm25 == sensor_dict["attributes"]["minMeasuredPM25"]
    assert sensor.voc_index == sensor_dict["attributes"]["vocIndex"]
    assert sensor.can_receive == sensor_dict["capabilities"]["canReceive"]
    assert sensor.room_id == sensor_dict["room"]["id"]
    assert sensor.room_name == sensor_dict["room"]["name"]
    assert sensor.manufacturer == sensor_dict["attributes"]["manufacturer"]
