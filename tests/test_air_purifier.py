import pytest

from dirigera.devices.air_purifier import AirPurifier, dict_to_air_purifier, FanModeEnum
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub

FAKE_DEVICE_ID = "abcd"
FAKE_PURIFIER_DATA = {
    "id": FAKE_DEVICE_ID,
    "type": "airPurifier",
    "deviceType": "airPurifier",
    "createdAt": "2023-05-05T19:45:07.000Z",
    "isReachable": True,
    "lastSeen": "2023-05-21T20:17:21.000Z",
    "attributes": {
        "customName": "Air purifier 1",
        "firmwareVersion": "1.1.001",
        "hardwareVersion": "1",
        "manufacturer": "IKEA of Sweden",
        "model": "STARKVIND Air purifier",
        "productCode": "E2007",
        "serialNumber": "0C4314FFFED62050",
        "fanMode": "auto",
        "fanModeSequence": "lowMediumHighAuto",
        "motorRuntime": 6729,
        "motorState": 10,
        "filterAlarmStatus": False,
        "filterElapsedTime": 23134,
        "filterLifetime": 259200,
        "childLock": False,
        "statusLight": True,
        "currentPM25": 19,
        "identifyPeriod": 0,
        "identifyStarted": "2000-01-01T00:00:00.000Z",
        "permittingJoin": False,
        "otaPolicy": "autoUpdate",
        "otaProgress": 0,
        "otaScheduleEnd": "00:00",
        "otaScheduleStart": "00:00",
        "otaState": "readyToCheck",
        "otaStatus": "upToDate",
    },
    "capabilities": {
        "canSend": [],
        "canReceive": ["customName", "fanMode", "fanModeSequence", "motorState", "childLock", "statusLight"],
    },
    "room": {
        "id": "a9d6ac9a-12ac-401e-b104-e15d45a32afa",
        "name": "Office",
        "color": "ikea_blue_no_63",
        "icon": "rooms_office_chair",
    },
    "deviceSet": [],
    "remoteLinks": [],
    "isHidden": False,
}


@pytest.fixture(name="fake_client")
def fixture_fake_client():
    noisy_fake_hub = FakeDirigeraHub()
    noisy_fake_hub.get_action_replys = {f"/devices/{FAKE_DEVICE_ID}": FAKE_PURIFIER_DATA}
    return noisy_fake_hub


@pytest.fixture(name="fake_purifier")
def fixture_purifier(fake_client: FakeDirigeraHub):
    return AirPurifier(
        dirigera_client=fake_client,
        device_id=FAKE_DEVICE_ID,
        is_reachable=True,
        custom_name="purifierMcPurifierFace",
        fan_mode="auto",
        fan_mode_sequence="lowMediumHighAuto",
        child_lock=False,
        motor_runtime=10,
        motor_state=50,
        filter_alarm_status=False,
        filter_elapsed_time=100,
        filter_lifetime=1000,
        current_pm25=42,
        can_receive=["customName", "fanMode", "fanModeSequence", "motorState", "childLock", "statusLight"],
        serial_number="987654321",
        manufacturer="AcmeCorp",
        firmware_version="23",
        hardware_version="08/15",
        model="T-800",
        room_id="234",
        room_name="Downstairs",
        status_light=False,
    )


def test_set_fan_mode(fake_purifier: AirPurifier, fake_client: FakeDirigeraHub):
    new_mode = FanModeEnum.LOW
    fake_purifier.set_fan_mode(new_mode)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_purifier.device_id}"
    assert action["data"] == [{"attributes": {"fanMode": new_mode.value}}]


def test_set_motor_state(fake_purifier: AirPurifier, fake_client: FakeDirigeraHub):
    new_state = 23
    fake_purifier.set_motor_state(new_state)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_purifier.device_id}"
    assert action["data"] == [{"attributes": {"motorState": new_state}}]


def test_set_child_lock(fake_purifier: AirPurifier, fake_client: FakeDirigeraHub):
    for cl in [True, False, False, True]:
        fake_purifier.set_child_lock(cl)
        action = fake_client.patch_actions.pop()
        assert action["route"] == f"/devices/{fake_purifier.device_id}"
        assert action["data"] == [{"attributes": {"childLock": cl}}]


def test_status_light(fake_purifier: AirPurifier, fake_client: FakeDirigeraHub):
    for st_light in [True, False, False, True]:
        fake_purifier.set_status_light(st_light)
        action = fake_client.patch_actions.pop()
        assert action["route"] == f"/devices/{fake_purifier.device_id}"
        assert action["data"] == [{"attributes": {"statusLight": st_light}}]


def test_dict_to_outlet(fake_client: FakeDirigeraHub):
    data = FAKE_PURIFIER_DATA

    air_purifier = dict_to_air_purifier(data=data, dirigera_client=fake_client)
    assert air_purifier.dirigera_client == fake_client
    assert air_purifier.device_id == data["id"]
    assert air_purifier.is_reachable == data["isReachable"]
    assert air_purifier.custom_name == data["attributes"]["customName"]
    assert air_purifier.can_receive == data["capabilities"]["canReceive"]
    assert air_purifier.room_id == data["room"]["id"]
    assert air_purifier.room_name == data["room"]["name"]
    assert air_purifier.firmware_version == data["attributes"]["firmwareVersion"]
    assert air_purifier.hardware_version == data["attributes"]["hardwareVersion"]
    assert air_purifier.model == data["attributes"]["model"]
    assert air_purifier.manufacturer == data["attributes"]["manufacturer"]
    assert air_purifier.serial_number == data["attributes"]["serialNumber"]
    assert air_purifier.fan_mode == data["attributes"]["fanMode"]
    assert air_purifier.fan_mode_sequence == data["attributes"]["fanModeSequence"]
    assert air_purifier.status_light == data["attributes"]["statusLight"]
