from typing import Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.motion_sensor import MotionSensor, dict_to_motion_sensor


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="motion_sensor_dict_non_ikea")
def fixture_motion_sensor_dict_non_ikea() -> Dict:
    return {
        "id": "62e95143-c8b6-4f28-b581-adfd622c0db7_1",
        "type": "sensor",
        "deviceType": "motionSensor",
        "createdAt": "2023-12-14T18:28:57.000Z",
        "isReachable": True,
        "lastSeen": "2023-12-14T17:30:48.000Z",
        "attributes": {
            "customName": "Bewegungssensor",
            "firmwareVersion": "",
            "hardwareVersion": "",
            "manufacturer": "SONOFF",
            "model": "Wireless Motion Sensor",
            "productCode": "SNZB-03",
            "serialNumber": "9",
            "isOn": False,
            "permittingJoin": False,
            "sensorConfig": {
                "scheduleOn": False,
                "onDuration": 120,
                "schedule": {
                    "onCondition": {"time": "sunset", "offset": -60},
                    "offCondition": {"time": "sunrise", "offset": 60},
                },
            },
            "circadianPresets": [],
        },
        "capabilities": {
            "canSend": ["isOn", "lightLevel"],
            "canReceive": ["customName"],
        },
        "room": {
            "id": "e1631a64-9ceb-4113-a6b3-1d866216503c",
            "name": "Zimmer",
            "color": "ikea_beige_1",
            "icon": "rooms_arm_chair",
        },
        "deviceSet": [],
        "remoteLinks": [],
        "isHidden": False,
    }


@pytest.fixture(name="motion_sensor_dict")
def fixture_motion_sensor_dict() -> Dict:
    return {
        "id": "62e95143-c8b6-4f28-b581-adfd622c0db7_1",
        "type": "sensor",
        "deviceType": "motionSensor",
        "createdAt": "2023-12-14T18:28:57.000Z",
        "isReachable": True,
        "lastSeen": "2023-12-14T17:30:48.000Z",
        "attributes": {
            "customName": "Bewegungssensor",
            "firmwareVersion": "24.4.5",
            "hardwareVersion": "1",
            "manufacturer": "IKEA of Sweden",
            "model": "TRADFRI motion sensor",
            "productCode": "E1745",
            "serialNumber": "142D51FFFE229101",
            "batteryPercentage": 100,
            "isOn": False,
            "lightLevel": 1,
            "permittingJoin": False,
            "otaPolicy": "autoUpdate",
            "otaProgress": 0,
            "otaScheduleEnd": "00:00",
            "otaScheduleStart": "00:00",
            "otaState": "readyToCheck",
            "otaStatus": "upToDate",
            "sensorConfig": {
                "scheduleOn": False,
                "onDuration": 120,
                "schedule": {
                    "onCondition": {"time": "sunset", "offset": -60},
                    "offCondition": {"time": "sunrise", "offset": 60},
                },
            },
            "circadianPresets": [],
        },
        "capabilities": {
            "canSend": ["isOn", "lightLevel"],
            "canReceive": ["customName"],
        },
        "room": {
            "id": "e1631a64-9ceb-4113-a6b3-1d866216503c",
            "name": "Zimmer",
            "color": "ikea_beige_1",
            "icon": "rooms_arm_chair",
        },
        "deviceSet": [],
        "remoteLinks": [],
        "isHidden": False,
    }


@pytest.fixture(name="fake_motion_sensor")
def fixture_blind(
    motion_sensor_dict: Dict, fake_client: FakeDirigeraHub
) -> MotionSensor:
    return MotionSensor(
        dirigeraClient=fake_client,
        **motion_sensor_dict,
    )


def test_set_motion_sensor_name(
    fake_motion_sensor: MotionSensor, fake_client: FakeDirigeraHub
) -> None:
    new_name = "motion_sensor_name"
    assert fake_motion_sensor.attributes.custom_name != new_name
    fake_motion_sensor.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_motion_sensor.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_motion_sensor.attributes.custom_name == new_name


def test_dict_to_motion_sensor(motion_sensor_dict: Dict, fake_client: FakeDirigeraHub) -> None:
    motion_sensor = dict_to_motion_sensor(motion_sensor_dict, fake_client)
    assert motion_sensor.dirigera_client == fake_client
    assert motion_sensor.id == motion_sensor_dict["id"]
    assert motion_sensor.is_reachable == motion_sensor_dict["isReachable"]
    assert (
        motion_sensor.attributes.custom_name
        == motion_sensor_dict["attributes"]["customName"]
    )
    assert (
        motion_sensor.attributes.battery_percentage
        == motion_sensor_dict["attributes"]["batteryPercentage"]
    )
    assert motion_sensor.attributes.is_on == motion_sensor_dict["attributes"]["isOn"]
    assert (
        motion_sensor.attributes.light_level
        == motion_sensor_dict["attributes"]["lightLevel"]
    )
    assert (
        motion_sensor.capabilities.can_receive
        == motion_sensor_dict["capabilities"]["canReceive"]
    )
    assert motion_sensor.room.id == motion_sensor_dict["room"]["id"]
    assert motion_sensor.room.name == motion_sensor_dict["room"]["name"]
    assert (
        motion_sensor.attributes.firmware_version
        == motion_sensor_dict["attributes"]["firmwareVersion"]
    )
    assert (
        motion_sensor.attributes.hardware_version
        == motion_sensor_dict["attributes"]["hardwareVersion"]
    )
    assert motion_sensor.attributes.model == motion_sensor_dict["attributes"]["model"]
    assert (
        motion_sensor.attributes.manufacturer
        == motion_sensor_dict["attributes"]["manufacturer"]
    )

def test_dict_to_motion_sensor_optional_fields(motion_sensor_dict_non_ikea: Dict, fake_client: FakeDirigeraHub) -> None:
    motion_sensor = dict_to_motion_sensor(motion_sensor_dict_non_ikea, fake_client)

    assert motion_sensor.attributes.battery_percentage is None
