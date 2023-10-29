from typing import Any, Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.outlet import dict_to_outlet
from src.dirigera.devices.outlet import Outlet
from src.dirigera.devices.device import StartupEnum


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="fake_outlet_dict")
def fixture_outlet_dict() -> Dict:
    return {
        "id": "f430fd01",
        "type": "outlet",
        "deviceType": "outlet",
        "isReachable": True,
        "lastSeen": "2023-01-07T20:07:19.000Z",
        "createdAt": "2023-01-07T20:07:19.000Z",
        "attributes": {
            "customName": "coffee",
            "model": "TRADFRI control outlet",
            "manufacturer": "IKEA of Sweden",
            "firmwareVersion": "2.3.089",
            "hardwareVersion": "1",
            "serialNumber": "1",
            "productCode": "E1603",
            "isOn": True,
            "startupOnOff": "startPrevious",
            "lightLevel": 100,
            "startUpCurrentLevel": -1,
            "identifyStarted": "2000-01-01T00:00:00.000Z",
            "identifyPeriod": 0,
            "permittingJoin": False,
            "otaStatus": "upToDate",
            "otaState": "readyToCheck",
            "otaProgress": 0,
            "otaPolicy": "autoUpdate",
            "otaScheduleStart": "00:00",
            "otaScheduleEnd": "00:00",
        },
        "capabilities": {
            "canSend": [],
            "canReceive": ["customName", "isOn", "lightLevel"],
        },
        "room": {"id": "63ffdf20", "name": "kitchen", "color": "color", "icon": "icon"},
        "deviceSet": [],
        "remoteLinks": ["152461d3"],
        "isHidden": False,
    }


@pytest.fixture(name="fake_outlet")
def fixture_outlet(fake_outlet_dict: Dict, fake_client: FakeDirigeraHub) -> Outlet:
    return Outlet(dirigeraClient=fake_client, **fake_outlet_dict)


def test_set_name(fake_outlet: Outlet, fake_client: FakeDirigeraHub) -> None:
    new_name = "teapot"
    fake_outlet.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_outlet.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_outlet.attributes.custom_name == new_name


def test_set_outlet_on(fake_outlet: Outlet, fake_client: FakeDirigeraHub) -> None:
    fake_outlet.set_on(True)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_outlet.id}"
    assert action["data"] == [{"attributes": {"isOn": True}}]
    assert fake_outlet.attributes.is_on


def test_set_outlet_off(fake_outlet: Outlet, fake_client: FakeDirigeraHub) -> None:
    fake_outlet.set_on(False)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_outlet.id}"
    assert action["data"] == [{"attributes": {"isOn": False}}]
    assert not fake_outlet.attributes.is_on


def test_set_startup_behaviour_off(
    fake_outlet: Outlet, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_OFF
    fake_outlet.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_outlet.id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour.value}}]
    assert fake_outlet.attributes.startup_on_off == behaviour


def test_dict_to_outlet(fake_client: FakeDirigeraHub) -> None:
    data: Dict[str, Any] = {
        "id": "f430fd01",
        "type": "outlet",
        "deviceType": "outlet",
        "isReachable": True,
        "lastSeen": "2023-01-07T20:07:19.000Z",
        "createdAt": "2023-01-07T20:07:19.000Z",
        "attributes": {
            "customName": "coffee",
            "model": "TRADFRI control outlet",
            "manufacturer": "IKEA of Sweden",
            "firmwareVersion": "2.3.089",
            "hardwareVersion": "1",
            "serialNumber": "1",
            "productCode": "E1603",
            "isOn": True,
            "startupOnOff": "startPrevious",
            "lightLevel": 100,
            "startUpCurrentLevel": -1,
            "identifyStarted": "2000-01-01T00:00:00.000Z",
            "identifyPeriod": 0,
            "permittingJoin": False,
            "otaStatus": "upToDate",
            "otaState": "readyToCheck",
            "otaProgress": 0,
            "otaPolicy": "autoUpdate",
            "otaScheduleStart": "00:00",
            "otaScheduleEnd": "00:00",
        },
        "capabilities": {
            "canSend": [],
            "canReceive": ["customName", "isOn", "lightLevel"],
        },
        "room": {"id": "63ffdf20", "name": "kitchen", "color": "color", "icon": "icon"},
        "deviceSet": [],
        "remoteLinks": ["152461d3"],
        "isHidden": False,
    }

    outlet = dict_to_outlet(data, fake_client)
    assert outlet.dirigera_client == fake_client
    assert outlet.id == data["id"]
    assert outlet.is_reachable == data["isReachable"]
    assert outlet.attributes.custom_name == data["attributes"]["customName"]
    assert outlet.attributes.is_on == data["attributes"]["isOn"]
    assert outlet.attributes.startup_on_off == StartupEnum(
        data["attributes"]["startupOnOff"]
    )
    assert outlet.capabilities.can_receive == data["capabilities"]["canReceive"]
    assert outlet.room.id == data["room"]["id"]
    assert outlet.room.name == data["room"]["name"]
    assert outlet.attributes.firmware_version == data["attributes"]["firmwareVersion"]
    assert outlet.attributes.hardware_version == data["attributes"]["hardwareVersion"]
    assert outlet.attributes.model == data["attributes"]["model"]
    assert outlet.attributes.manufacturer == data["attributes"]["manufacturer"]
    assert outlet.attributes.serial_number == data["attributes"]["serialNumber"]
