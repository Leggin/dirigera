import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.controller import dict_to_controller
from src.dirigera.devices.controller import Controller


@pytest.fixture(name="fake_client")
def fixture_fake_client():
    return FakeDirigeraHub()


@pytest.fixture(name="fake_controller")
def fixture_controller(fake_client: FakeDirigeraHub):
    return Controller(
        dirigera_client=fake_client,
        device_id="abcd",
        is_reachable=True,
        custom_name="good lamp",
        is_on=True,
        room_id="123",
        room_name="Upstairs",
        battery_percentage=1,
        firmware_version="1",
        hardware_version="1",
        model="a",
        manufacturer="IKEA",
        serial_number="abc-abc",
        can_receive=["customName"],
    )


def test_set_name(fake_controller: Controller, fake_client: FakeDirigeraHub):
    new_name = "outofcontrol"
    fake_controller.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_controller.device_id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_controller.custom_name == new_name


def test_dict_to_controller(fake_client: FakeDirigeraHub):
    data = {
        "id": "1237-343-2dfa",
        "type": "controller",
        "deviceType": "lightController",
        "isReachable": True,
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
            "id": "19aa77553369",
            "name": "Living room",
        },
    }

    light = dict_to_controller(data, fake_client)
    assert light.dirigera_client == fake_client
    assert light.device_id == data["id"]
    assert light.is_reachable == data["isReachable"]
    assert light.custom_name == data["attributes"]["customName"]
    assert light.is_on == data["attributes"]["isOn"]
    assert light.battery_percentage == data["attributes"]["batteryPercentage"]
    assert light.can_receive == data["capabilities"]["canReceive"]
    assert light.room_id == data["room"]["id"]
    assert light.room_name == data["room"]["name"]
    assert light.firmware_version == data["attributes"]["firmwareVersion"]
    assert light.hardware_version == data["attributes"]["hardwareVersion"]
    assert light.model == data["attributes"]["model"]
    assert light.manufacturer == data["attributes"]["manufacturer"]
