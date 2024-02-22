from typing import Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.air_purifier import (
    AirPurifier,
    FanModeEnum,
    dict_to_air_purifier
)


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()

@pytest.fixture(name="purifier_dict")
def fixture_fake_air_purifier_dict() -> dict:
    return {
        "id": "d121f38a-fc37-4bd9-8a3c-f79e4f45fccf_1",
        "type": "airPurifier",
        "deviceType": "airPurifier",
        "createdAt": "2023-08-09T12:31:59.000Z",
        "isReachable": True,
        "lastSeen": "2024-02-21T19:55:44.000Z",
        "attributes": {
            "customName": "Air Purifier",
            "firmwareVersion": "1.0.033",
            "hardwareVersion": "1",
            "manufacturer": "IKEA of Sweden",
            "model": "STARKVIND Air purifier",
            "productCode": "E2007",
            "serialNumber": "2C1165FFFE89F47C",
            "fanMode": "auto",
            "fanModeSequence": "lowMediumHighAuto",
            "motorRuntime": 106570,
            "motorState": 15,
            "filterAlarmStatus": False,
            "filterElapsedTime": 227980,
            "filterLifetime": 259200,
            "childLock": False,
            "statusLight": True,
            "currentPM25": 3,
            "identifyPeriod": 0,
            "identifyStarted": "2000-01-01T00:00:00.000Z",
            "permittingJoin": False,
            "otaPolicy": "autoUpdate",
            "otaProgress": 0,
            "otaScheduleEnd": "00:00",
            "otaScheduleStart": "00:00",
            "otaState": "readyToCheck",
            "otaStatus": "updateAvailable",
        },
        "capabilities": {
            "canSend": [],
            "canReceive": [
                "customName",
                "fanMode",
                "fanModeSequence",
                "motorState",
                "childLock",
                "statusLight",
            ],
        },
        "room": {
            "id": "1a846fdc-317c-4d94-8722-cb0196256a16",
            "name": "Livingroom",
            "color": "ikea_green_no_66",
            "icon": "rooms_arm_chair",
        },
        "deviceSet": [],
        "remoteLinks": [],
        "isHidden": False,
    }


@pytest.fixture(name="fake_purifier")
def fixture_purifier(
    fake_client: FakeDirigeraHub, purifier_dict: Dict
) -> AirPurifier:
    return AirPurifier(dirigeraClient=fake_client, **purifier_dict)

def test_set_name(fake_purifier: AirPurifier, fake_client: FakeDirigeraHub) -> None:
    new_name = "Luftreiniger"
    fake_purifier.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_purifier.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_purifier.attributes.custom_name == new_name

def test_set_fan_mode_enum(fake_purifier: AirPurifier, fake_client: FakeDirigeraHub) -> None:
    new_mode = FanModeEnum.LOW
    fake_purifier.set_fan_mode(new_mode)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_purifier.id}"
    assert action["data"] == [{"attributes": {"fanMode": new_mode.value}}]
    assert fake_purifier.attributes.fan_mode == new_mode

def test_set_motor_state(fake_purifier: AirPurifier, fake_client: FakeDirigeraHub) -> None:
    new_motor_state = 42
    fake_purifier.set_motor_state(new_motor_state)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_purifier.id}"
    assert action["data"] == [{"attributes": {"motorState": new_motor_state}}]
    assert fake_purifier.attributes.motor_state == new_motor_state

def test_set_child_lock(fake_purifier: AirPurifier, fake_client: FakeDirigeraHub) -> None:
    new_child_lock = True
    fake_purifier.set_child_lock(new_child_lock)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_purifier.id}"
    assert action["data"] == [{"attributes": {"childLock": new_child_lock}}]
    assert fake_purifier.attributes.child_lock == new_child_lock

def test_status_light(fake_purifier: AirPurifier, fake_client: FakeDirigeraHub) -> None:
    new_status_light = False
    fake_purifier.set_status_light(new_status_light)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_purifier.id}"
    assert action["data"] == [{"attributes": {"statusLight": new_status_light}}]
    assert fake_purifier.attributes.status_light == new_status_light


def test_dict_to_purifier(fake_client: FakeDirigeraHub, purifier_dict: Dict) -> None:
    purifier = dict_to_air_purifier(purifier_dict, fake_client)
    assert purifier.id == purifier_dict["id"]
    assert purifier.is_reachable == purifier_dict["isReachable"]
    assert purifier.attributes.custom_name == purifier_dict["attributes"]["customName"]
    assert (
        purifier.attributes.firmware_version
        == purifier_dict["attributes"]["firmwareVersion"]
    )
    assert (
        purifier.attributes.hardware_version
        == purifier_dict["attributes"]["hardwareVersion"]
    )
    assert purifier.attributes.model == purifier_dict["attributes"]["model"]
    assert purifier.attributes.serial_number == purifier_dict["attributes"]["serialNumber"]
    assert purifier.attributes.manufacturer == purifier_dict["attributes"]["manufacturer"]
    assert purifier.attributes.fan_mode.value == purifier_dict["attributes"]["fanMode"]
    assert purifier.attributes.fan_mode_sequence == purifier_dict["attributes"]["fanModeSequence"]
    assert purifier.attributes.motor_state == purifier_dict["attributes"]["motorState"]
    assert purifier.attributes.child_lock == purifier_dict["attributes"]["childLock"]
    assert purifier.attributes.status_light == purifier_dict["attributes"]["statusLight"]
    assert purifier.attributes.motor_runtime == purifier_dict["attributes"]["motorRuntime"]
    assert purifier.attributes.filter_alarm_status == purifier_dict["attributes"]["filterAlarmStatus"]
    assert purifier.attributes.filter_elapsed_time == purifier_dict["attributes"]["filterElapsedTime"]
    assert purifier.attributes.filter_lifetime == purifier_dict["attributes"]["filterLifetime"]
    assert purifier.attributes.current_p_m25 == purifier_dict["attributes"]["currentPM25"]
    assert purifier.capabilities.can_receive == purifier_dict["capabilities"]["canReceive"]
    assert purifier.room.id == purifier_dict["room"]["id"]
    assert purifier.room.name == purifier_dict["room"]["name"]
