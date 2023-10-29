from typing import Any, Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.blinds import dict_to_blind
from src.dirigera.devices.blinds import Blind


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="fake_blind")
def fixture_blind(fake_client: FakeDirigeraHub) -> Blind:
    return Blind(
        dirigeraClient=fake_client,
        **{
            "id": "1237-343-2dfa",
            "type": "blind",
            "deviceType": "blinds",
            "createdAt": "2023-01-07T20:07:19.000Z",
            "isReachable": True,
            "lastSeen": "2023-10-28T04:42:15.000Z",
            "customIcon": "lighting_nightstand_light",
            "attributes": {
                "customName": "Light 2",
                "model": "FYRTUR",
                "manufacturer": "IKEA of Sweden",
                "firmwareVersion": "2.3.093",
                "serialNumber": "84",
                "hardwareVersion": "2",
                "blindsTargetLevel": 15,
                "blindsCurrentLevel": 90,
                "blindsState": "down",
                "productCode": "LED2003G10",
            },
            "capabilities": {
                "canSend": [],
                "canReceive": [
                    "customName",
                    "blindsCurrentLevel",
                    "blindsTargetLevel",
                    "blindsState",
                ],
            },
            "room": {
                "id": "23g2w34-d0b7-42b3-a5a1-324zaerfg3",
                "name": "Bedroom",
                "color": "ikea_yellow_no_24",
                "icon": "rooms_bed",
            },
            "deviceSet": [],
            "remoteLinks": ["3838120-12f0-256-9c63-bdf2dfg232"],
        },
    )


def test_set_name(fake_blind: Blind, fake_client: FakeDirigeraHub) -> None:
    new_name = "blindedbythelight"
    fake_blind.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_blind.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_blind.attributes.custom_name == new_name


def test_set_target_level(fake_blind: Blind, fake_client: FakeDirigeraHub) -> None:
    target_level = 80
    fake_blind.set_target_level(target_level)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_blind.id}"
    assert action["data"] == [{"attributes": {"blindsTargetLevel": target_level}}]
    assert fake_blind.attributes.blinds_target_level == target_level
    assert fake_blind.attributes.blinds_current_level == 90


def test_dict_to_blind(fake_client: FakeDirigeraHub) -> None:
    data: Dict[str, Any] = {
        "id": "1237-343-2dfa",
        "type": "blind",
        "deviceType": "blinds",
        "createdAt": "2023-01-07T20:07:19.000Z",
        "isReachable": True,
        "lastSeen": "2023-10-28T04:42:15.000Z",
        "customIcon": "lighting_nightstand_light",
        "attributes": {
            "customName": "Light 2",
            "model": "FYRTUR",
            "manufacturer": "IKEA of Sweden",
            "firmwareVersion": "2.3.093",
            "serialNumber": "84",
            "hardwareVersion": "2",
            "blindsTargetLevel": 15,
            "blindsCurrentLevel": 90,
            "blindsState": "down",
            "productCode": "LED2003G10",
        },
        "capabilities": {
            "canSend": [],
            "canReceive": [
                "customName",
                "blindsCurrentLevel",
                "blindsTargetLevel",
                "blindsState",
            ],
        },
        "room": {
            "id": "23g2w34-d0b7-42b3-a5a1-324zaerfg3",
            "name": "Bedroom",
            "color": "ikea_yellow_no_24",
            "icon": "rooms_bed",
        },
        "deviceSet": [],
        "remoteLinks": ["3838120-12f0-256-9c63-bdf2dfg232"],
    }

    blind = dict_to_blind(data, fake_client)
    assert blind.dirigera_client == fake_client
    assert blind.id == data["id"]
    assert blind.is_reachable == data["isReachable"]
    assert blind.attributes.custom_name == data["attributes"]["customName"]
    assert (
        blind.attributes.blinds_target_level == data["attributes"]["blindsTargetLevel"]
    )
    assert (
        blind.attributes.blinds_current_level
        == data["attributes"]["blindsCurrentLevel"]
    )
    assert blind.attributes.blinds_state == data["attributes"]["blindsState"]
    assert blind.capabilities.can_receive == data["capabilities"]["canReceive"]
    assert blind.room.id == data["room"]["id"]
    assert blind.room.name == data["room"]["name"]
    assert blind.attributes.firmware_version == data["attributes"]["firmwareVersion"]
    assert blind.attributes.hardware_version == data["attributes"]["hardwareVersion"]
    assert blind.attributes.model == data["attributes"]["model"]
    assert blind.attributes.manufacturer == data["attributes"]["manufacturer"]
