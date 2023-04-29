import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.blinds import dict_to_blind
from src.dirigera.devices.blinds import Blind


@pytest.fixture(name="fake_client")
def fixture_fake_client():
    return FakeDirigeraHub()


@pytest.fixture(name="fake_blind")
def fixture_blind(fake_client: FakeDirigeraHub):
    return Blind(
        dirigera_client=fake_client,
        device_id="abcd",
        is_reachable=True,
        custom_name="a blind",
        target_level=20,
        current_level=45,
        state='up',
        room_id="123",
        room_name="Upstairs",
        firmware_version="1",
        hardware_version="1",
        model="a",
        manufacturer="IKEA",
        serial_number="abc-abc",
        can_receive=[
            "customName",
            "blindsCurrentLevel",
            "blindsTargetLevel",
            "blindsState",
        ],
    )


def test_set_name(fake_blind: Blind, fake_client: FakeDirigeraHub):
    new_name = "blindedbythelight"
    fake_blind.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_blind.device_id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_blind.custom_name == new_name


def test_set_target_level(fake_blind: Blind, fake_client: FakeDirigeraHub) -> None:
    target_level = 80
    fake_blind.set_target_level(target_level)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_blind.device_id}"
    assert action["data"] == [{"attributes": {"blindsTargetLevel": target_level}}]
    assert fake_blind.target_level == target_level
    assert fake_blind.current_level == 45



def test_dict_to_blind(fake_client: FakeDirigeraHub):
    data = {
        "id": "1237-343-2dfa",
        "type": "blind",
        "deviceType": "blinds",
        "isReachable": True,
        "attributes": {
            "customName": "Light 2",
            "model": "FYRTUR",
            "manufacturer": "IKEA of Sweden",
            "firmwareVersion": "2.3.093",
            "hardwareVersion": "2",
            "blindsTargetLevel": 15,
            "blindsCurrentLevel": 90,
            "blindsState": 'down',
        },
        "capabilities": {
            "canSend": [],
            "canReceive": ["customName", "blindsCurrentLevel", "blindsTargetLevel", "blindsState"],
        },
        "room": {
            "id": "19aa77553369",
            "name": "Living room",
        },
    }

    blind = dict_to_blind(data, fake_client)
    assert blind.dirigera_client == fake_client
    assert blind.device_id == data["id"]
    assert blind.is_reachable == data["isReachable"]
    assert blind.custom_name == data["attributes"]["customName"]
    assert blind.target_level == data["attributes"]["blindsTargetLevel"]
    assert blind.current_level == data["attributes"]["blindsCurrentLevel"]
    assert blind.state == data["attributes"]["blindsState"]
    assert blind.can_receive == data["capabilities"]["canReceive"]
    assert blind.room_id == data["room"]["id"]
    assert blind.room_name == data["room"]["name"]
    assert blind.firmware_version == data["attributes"]["firmwareVersion"]
    assert blind.hardware_version == data["attributes"]["hardwareVersion"]
    assert blind.model == data["attributes"]["model"]
    assert blind.manufacturer == data["attributes"]["manufacturer"]
