from typing import Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.open_close_sensor import (
    OpenCloseSensor,
    dict_to_open_close_sensor,
)


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="fake_sensor")
def fixture_sensor(fake_client: FakeDirigeraHub) -> OpenCloseSensor:
    return OpenCloseSensor(
        dirigeraClient=fake_client,
        **{
            "id": "abc123",
            "type": "sensor",
            "deviceType": "openclose ensor",
            "createdAt": "2023-01-07T20:07:19.000Z",
            "isReachable": True,
            "lastSeen": "2023-10-28T04:42:15.000Z",
            "customIcon": "lighting_nightstand_light",
            "attributes": {
                "customName": "Sensor 1",
                "model": "Wireless Door/Window Sensor",
                "manufacturer": "SONOFF",
                "firmwareVersion": "1.0.11",
                "hardwareVersion": "1",
                "serialNumber": "00124B0029121E50",
                "productCode": "SNZB-04",
                "isOpen": False,
                "otaStatus": "upToDate",
                "otaState": "readyToCheck",
                "otaProgress": 0,
                "otaPolicy": "autoUpdate",
                "otaScheduleStart": "00:00",
                "otaScheduleEnd": "00:00",
            },
            "room": {
                "id": "23g2w34-d0b7-42b3-a5a1-324zaerfg3",
                "name": "upstairs",
                "color": "ikea_yellow_no_24",
                "icon": "lamp",
            },
            "deviceSet": [],
            "remoteLinks": ["3838120-12f0-256-9c63-bdf2dfg232"],
            "isHidden": False,
            "capabilities": {"canSend": [], "canReceive": ["customName"]},
        },
    )


@pytest.fixture(name="sensor_dict")
def fixture_sensor_dict() -> Dict:
    return {
        "id": "abc123",
        "type": "sensor",
        "deviceType": "openclose ensor",
        "createdAt": "2023-01-07T20:07:19.000Z",
        "isReachable": True,
        "lastSeen": "2023-10-28T04:42:15.000Z",
        "customIcon": "lighting_nightstand_light",
        "attributes": {
            "customName": "Sensor 1",
            "model": "Wireless Door/Window Sensor",
            "manufacturer": "SONOFF",
            "firmwareVersion": "1.0.11",
            "hardwareVersion": "1",
            "serialNumber": "00124B0029121E50",
            "productCode": "SNZB-04",
            "isOpen": False,
            "otaStatus": "upToDate",
            "otaState": "readyToCheck",
            "otaProgress": 0,
            "otaPolicy": "autoUpdate",
            "otaScheduleStart": "00:00",
            "otaScheduleEnd": "00:00",
        },
        "room": {
            "id": "23g2w34-d0b7-42b3-a5a1-324zaerfg3",
            "name": "upstairs",
            "color": "ikea_yellow_no_24",
            "icon": "lamp",
        },
        "deviceSet": [],
        "remoteLinks": ["3838120-12f0-256-9c63-bdf2dfg232"],
        "isHidden": False,
        "capabilities": {"canSend": [], "canReceive": ["customName"]},
    }


def test_set_name(fake_sensor: OpenCloseSensor, fake_client: FakeDirigeraHub) -> None:
    new_name = "staubsensor"
    fake_sensor.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_sensor.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_sensor.attributes.custom_name == new_name


def test_dict_to_sensor(fake_client: FakeDirigeraHub, sensor_dict: Dict) -> None:
    sensor = dict_to_open_close_sensor(sensor_dict, fake_client)
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
    assert sensor.attributes.is_open == sensor_dict["attributes"]["isOpen"]
    assert sensor.capabilities.can_receive == sensor_dict["capabilities"]["canReceive"]
    assert sensor.room.id == sensor_dict["room"]["id"]
    assert sensor.room.name == sensor_dict["room"]["name"]
    assert sensor.attributes.manufacturer == sensor_dict["attributes"]["manufacturer"]
