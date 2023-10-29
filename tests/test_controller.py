from typing import Any, Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.controller import dict_to_controller
from src.dirigera.devices.controller import Controller


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="fake_controller")
def fixture_controller(fake_client: FakeDirigeraHub) -> Controller:
    return Controller(
        dirigeraClient=fake_client,
        **{
            "id": "1237-343-2dfa",
            "type": "controller",
            "deviceType": "lightController",
            "createdAt": "2023-01-07T20:07:19.000Z",
            "isReachable": True,
            "lastSeen": "2023-10-28T04:42:15.000Z",
            "customIcon": "lighting_nightstand_light",
            "attributes": {
                "customName": "Remote",
                "model": "TRADFRI STYRBAR",
                "manufacturer": "IKEA of Sweden",
                "firmwareVersion": "2.3.093",
                "hardwareVersion": "2",
                "isOn": False,
                "batteryPercentage": 90,
            },
            "capabilities": {
                "canSend": ["isOn", "lightLevel"],
                "canReceive": [
                    "customName",
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


def test_set_name(fake_controller: Controller, fake_client: FakeDirigeraHub) -> None:
    new_name = "outofcontrol"
    fake_controller.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_controller.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_controller.attributes.custom_name == new_name


def test_dict_to_controller(fake_client: FakeDirigeraHub) -> None:
    data: Dict[str, Any] = {
        "id": "1237-343-2dfa",
        "type": "controller",
        "deviceType": "lightController",
        "createdAt": "2023-01-07T20:07:19.000Z",
        "isReachable": True,
        "lastSeen": "2023-10-28T04:42:15.000Z",
        "customIcon": "lighting_nightstand_light",
        "attributes": {
            "customName": "Remote",
            "model": "TRADFRI STYRBAR",
            "manufacturer": "IKEA of Sweden",
            "firmwareVersion": "2.3.093",
            "hardwareVersion": "2",
            "isOn": False,
            "batteryPercentage": 90,
        },
        "capabilities": {
            "canSend": ["isOn", "lightLevel"],
            "canReceive": [
                "customName",
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

    controller = dict_to_controller(data, fake_client)
    assert controller.dirigera_client == fake_client
    assert controller.id == data["id"]
    assert controller.is_reachable == data["isReachable"]
    assert controller.attributes.custom_name == data["attributes"]["customName"]
    assert controller.attributes.is_on == data["attributes"]["isOn"]
    assert (
        controller.attributes.battery_percentage
        == data["attributes"]["batteryPercentage"]
    )
    assert controller.capabilities.can_receive == data["capabilities"]["canReceive"]
    assert controller.room.id == data["room"]["id"]
    assert controller.room.name == data["room"]["name"]
    assert (
        controller.attributes.firmware_version == data["attributes"]["firmwareVersion"]
    )
    assert (
        controller.attributes.hardware_version == data["attributes"]["hardwareVersion"]
    )
    assert controller.attributes.model == data["attributes"]["model"]
    assert controller.attributes.manufacturer == data["attributes"]["manufacturer"]
