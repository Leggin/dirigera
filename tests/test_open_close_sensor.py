from typing import Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.open_close_sensor import (
    OpenCloseSensor,
    dict_to_open_close_sensor,
)


@pytest.fixture(name="fake_client")
def fixture_fake_client():
    return FakeDirigeraHub()


@pytest.fixture(name="fake_sensor")
def fixture_sensor(fake_client: FakeDirigeraHub):
    return OpenCloseSensor(
        dirigera_client=fake_client,
        device_id="abc",
        is_reachable=True,
        custom_name="abc",
        firmware_version="abc",
        hardware_version="abc",
        model="abc",
        serial_number="abc",
        is_open=False,
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
            "model": "Wireless Door/Window Sensor",
            "productCode": "SNZB-04",
            "serialNumber": "00124B0029121E50",
            "isOpen": False,
            "manufacturer": "SONOFF",
        },
        "room": {"id": "123", "name": "upstairs"},
        "capabilities": {"canSend": [], "canReceive": ["customName"]},
    }


def test_set_name(fake_sensor: OpenCloseSensor, fake_client: FakeDirigeraHub):
    new_name = "staubsensor"
    fake_sensor.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_sensor.device_id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_sensor.custom_name == new_name


def test_dict_to_sensor(fake_client: FakeDirigeraHub, sensor_dict: Dict):
    sensor = dict_to_open_close_sensor(sensor_dict, fake_client)
    assert sensor.device_id == sensor_dict["id"]
    assert sensor.is_reachable == sensor_dict["isReachable"]
    assert sensor.custom_name == sensor_dict["attributes"]["customName"]
    assert sensor.firmware_version == sensor_dict["attributes"]["firmwareVersion"]
    assert sensor.hardware_version == sensor_dict["attributes"]["hardwareVersion"]
    assert sensor.model == sensor_dict["attributes"]["model"]
    assert sensor.serial_number == sensor_dict["attributes"]["serialNumber"]
    assert sensor.is_open == sensor_dict["attributes"]["isOpen"]
    assert sensor.can_receive == sensor_dict["capabilities"]["canReceive"]
    assert sensor.room_id == sensor_dict["room"]["id"]
    assert sensor.room_name == sensor_dict["room"]["name"]
    assert sensor.manufacturer == sensor_dict["attributes"]["manufacturer"]
