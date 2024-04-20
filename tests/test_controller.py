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

    somrig_button_1: Dict[str, Any] = {
        "id": "1111aaaa-1111-1111-aa11-1a1aa1a111a1_1",
        "relationId": "1111aaaa-1111-1111-aa11-1a1aa1a111a1",
        "type": "controller",
        "deviceType": "shortcutController",
        "createdAt": "2024-04-12T20:50:26.000Z",
        "isReachable": True,
        "lastSeen": "2024-04-12T20:50:32.000Z",
        "attributes": {
          "customName": "Living room button",
          "model": "SOMRIG shortcut button",
          "manufacturer": "IKEA of Sweden",
          "firmwareVersion": "1.0.21",
          "hardwareVersion": "1",
          "serialNumber": "1AA1A1AAAA11A1AA",
          "productCode": "E2213",
          "batteryPercentage": 85,
          "switchLabel": "Shortcut 1",
          "isOn": False,
          "lightLevel": 1,
          "permittingJoin": False,
          "otaStatus": "upToDate",
          "otaState": "readyToCheck",
          "otaProgress": 0,
          "otaPolicy": "autoUpdate",
          "otaScheduleStart": "00:00",
          "otaScheduleEnd": "00:00"
        },
        "capabilities": {
          "canSend": [
            "singlePress",
            "longPress",
            "doublePress"
          ],
          "canReceive": [
            "customName"
          ]
        },
        "room": {
          "id": "1aa1a11a-1a1a-111a-1aaa-111a111a111a",
          "name": "Living room",
          "color": "ikea_green_no_65",
          "icon": "rooms_sofa"
        },
        "deviceSet": [],
        "remoteLinks": [],
        "isHidden": False
    }

    controller = dict_to_controller(somrig_button_1, fake_client)
    assert controller.relation_id == somrig_button_1["relationId"]
    assert (
        controller.attributes.switch_label
        == somrig_button_1["attributes"]["switchLabel"]
    )

    somrig_button_2: Dict[str, Any] = {
        "id": "1111aaaa-1111-1111-aa11-1a1aa1a111a1_2",
        "relationId": "1111aaaa-1111-1111-aa11-1a1aa1a111a1",
        "type": "controller",
        "deviceType": "shortcutController",
        "createdAt": "2024-04-12T20:50:26.000Z",
        "isReachable": True,
        "lastSeen": "2024-04-12T20:50:32.000Z",
        "attributes": {
          "customName": "",
          "model": "SOMRIG shortcut button",
          "manufacturer": "IKEA of Sweden",
          "firmwareVersion": "1.0.21",
          "hardwareVersion": "1",
          "serialNumber": "1AA1A1AAAA11A1AA",
          "productCode": "E2213",
          "switchLabel": "Shortcut 2",
          "isOn": False,
          "lightLevel": 1,
          "permittingJoin": False,
          "otaStatus": "upToDate",
          "otaState": "readyToCheck",
          "otaProgress": 0,
          "otaPolicy": "autoUpdate",
          "otaScheduleStart": "00:00",
          "otaScheduleEnd": "00:00"
        },
        "capabilities": {
          "canSend": [
            "singlePress",
            "longPress",
            "doublePress"
          ],
          "canReceive": [
            "customName"
          ]
        },
        "deviceSet": [],
        "remoteLinks": [],
        "isHidden": False
    }

    controller = dict_to_controller(somrig_button_2, fake_client)
    assert controller.relation_id == somrig_button_2["relationId"]
    assert (
        controller.attributes.switch_label
        == somrig_button_2["attributes"]["switchLabel"]
    )
