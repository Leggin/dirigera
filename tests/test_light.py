import json
from typing import Any, Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.light import dict_to_light
from src.dirigera.devices.light import Light
from src.dirigera.devices.device import StartupEnum


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="fake_light")
def fixture_light(fake_client: FakeDirigeraHub) -> Light:
    data = """{ "id": "23taswdg-sdf-4eeb-99c2-23asdf2gw",
        "type": "light",
        "deviceType": "light",
        "createdAt": "2023-01-07T20:07:19.000Z",
        "isReachable": true,
        "lastSeen": "2023-10-28T04:42:14.000Z",
        "customIcon": "lighting_nightstand_light",
        "attributes": {
            "customName": "Bed",
            "model": "TRADFRIbulbE27WSglobeopal1055lm",
            "manufacturer": "IKEA of Sweden",
            "firmwareVersion": "1.0.012",
            "hardwareVersion": "1",
            "serialNumber": "04CD15FFFEC08659",
            "productCode": "LED2003G10",
            "isOn": false,
            "startupOnOff": "startOff",
            "lightLevel": 43,
            "colorTemperature": 2222,
            "colorTemperatureMin": 4000,
            "colorTemperatureMax": 2202,
            "startupTemperature": -1,
            "colorHue": 200,
            "colorSaturation": 0.7,
            "colorMode": "temperature",
            "identifyStarted": "2000-01-01T00:00:00.000Z",
            "identifyPeriod": 0,
            "permittingJoin": false,
            "otaStatus": "upToDate",
            "otaState": "readyToCheck",
            "otaProgress": 0,
            "otaPolicy": "autoUpdate",
            "otaScheduleStart": "00:00",
            "otaScheduleEnd": "00:00",
            "circadianRhythmMode": ""
        },
        "capabilities": {
            "canSend": [],
            "canReceive": ["customName", "isOn", "lightLevel", "colorTemperature", "colorSaturation", "colorHue"]
        },
        "room": {
            "id": "23g2w34-d0b7-42b3-a5a1-324zaerfg3",
            "name": "Bedroom",
            "color": "ikea_yellow_no_24",
            "icon": "rooms_bed"
        },
        "deviceSet": [],
        "remoteLinks": ["3838120-12f0-256-9c63-bdf2dfg232"],
        "isHidden": false
    }"""
    return dict_to_light(json.loads(data), fake_client)


def test_refresh(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    data: Dict[str, Any] = {
        "id": "23taswdg-sdf-4eeb-99c2-23asdf2gw",
        "type": "light",
        "deviceType": "light",
        "createdAt": "2023-01-07T20:07:19.000Z",
        "isReachable": False,
        "lastSeen": "2023-10-28T04:42:15.000Z",
        "customIcon": "lighting_nightstand_light",
        "attributes": {
            "customName": "Bed",
            "model": "TRADFRIbulbE27WSglobeopal1055lm",
            "manufacturer": "IKEA of Sweden",
            "firmwareVersion": "1.0.012",
            "hardwareVersion": "1",
            "serialNumber": "04CD15FFFEC08659",
            "productCode": "LED2003G10",
            "isOn": False,
            "lightLevel": 13,
            "colorTemperature": 2222,
            "colorTemperatureMin": 4000,
            "colorTemperatureMax": 2202,
            "colorHue": 100,
            "colorSaturation": 0.8,
            "startupTemperature": -1,
            "colorMode": "temperature",
            "identifyStarted": "2000-01-01T00:00:00.000Z",
            "identifyPeriod": 0,
            "permittingJoin": True,
            "otaStatus": "upToDate",
            "otaState": "readyToCheck",
            "otaProgress": 0,
            "otaPolicy": "autoUpdate",
            "otaScheduleStart": "00:00",
            "otaScheduleEnd": "00:00",
            "circadianRhythmMode": "",
        },
        "capabilities": {
            "canSend": [],
            "canReceive": ["customName", "isOn", "lightLevel", "colorTemperature"],
        },
        "room": {
            "id": "23g2w34-d0b7-42b3-a5a1-324zaerfg3",
            "name": "Bedroom",
            "color": "ikea_yellow_no_24",
            "icon": "rooms_bed",
        },
        "deviceSet": [],
        "remoteLinks": ["3838120-12f0-256-9c63-bdf2dfg232"],
        "isHidden": False,
    }
    fake_client.get_action_replys[f"/devices/{fake_light.id}"] = data
    fake_light = fake_light.reload()
    fake_client.get_actions.pop()
    assert fake_light.dirigera_client == fake_client
    assert fake_light.id == data["id"]
    assert fake_light.is_reachable == data["isReachable"]
    assert fake_light.attributes.custom_name == data["attributes"]["customName"]
    assert fake_light.attributes.is_on == data["attributes"]["isOn"]
    assert fake_light.attributes.startup_on_off is None
    assert fake_light.attributes.light_level == data["attributes"]["lightLevel"]
    assert (
        fake_light.attributes.color_temperature
        == data["attributes"]["colorTemperature"]
    )
    assert (
        fake_light.attributes.color_temperature_min
        == data["attributes"]["colorTemperatureMin"]
    )
    assert (
        fake_light.attributes.color_temperature_max
        == data["attributes"]["colorTemperatureMax"]
    )
    assert fake_light.capabilities.can_receive == data["capabilities"]["canReceive"]
    assert fake_light.room.id == data["room"]["id"]
    assert fake_light.room.name == data["room"]["name"]
    assert (
        fake_light.attributes.firmware_version == data["attributes"]["firmwareVersion"]
    )
    assert (
        fake_light.attributes.hardware_version == data["attributes"]["hardwareVersion"]
    )
    assert fake_light.attributes.model == data["attributes"]["model"]
    assert fake_light.attributes.manufacturer == data["attributes"]["manufacturer"]
    assert fake_light.attributes.serial_number == data["attributes"]["serialNumber"]


def test_set_name(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    new_name = "stadtlampefluss"
    fake_light.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_light.attributes.custom_name == new_name


def test_set_light_on(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    fake_light.set_light(True)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [{"attributes": {"isOn": True}}]
    assert fake_light.attributes.is_on


def test_set_light_off(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    fake_light.set_light(False)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [{"attributes": {"isOn": False}}]
    assert not fake_light.attributes.is_on


def test_set_light_level(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    level = 80
    fake_light.set_light_level(level)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [{"attributes": {"lightLevel": level}}]
    assert fake_light.attributes.light_level == level


def test_set_color_temperature(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    temp = 2203
    fake_light.set_color_temperature(temp)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [{"attributes": {"colorTemperature": temp}}]
    assert fake_light.attributes.color_temperature == temp


def test_set_light_color(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    hue = 120
    saturation = 0.9
    fake_light.set_light_color(hue, saturation)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [
        {"attributes": {"colorHue": hue, "colorSaturation": saturation}}
    ]
    assert fake_light.attributes.color_hue == hue
    assert fake_light.attributes.color_saturation == saturation


def test_set_startup_behaviour_off(
    fake_light: Light, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_OFF
    fake_light.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour.value}}]
    assert fake_light.attributes.startup_on_off == behaviour


def test_set_startup_behaviour_on(
    fake_light: Light, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_ON
    fake_light.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour.value}}]
    assert fake_light.attributes.startup_on_off == behaviour


def test_set_startup_behaviour_previous(
    fake_light: Light, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_PREVIOUS
    fake_light.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour.value}}]
    assert fake_light.attributes.startup_on_off == behaviour


def test_set_startup_behaviour_toggle(
    fake_light: Light, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_TOGGLE
    fake_light.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour.value}}]
    assert fake_light.attributes.startup_on_off == behaviour


def test_dict_to_light_3rdparty(fake_client: FakeDirigeraHub) -> None:
    data: Dict[str, Any] = {
        "id": "1237-343-2dfa",
        "type": "light",
        "deviceType": "light",
        "createdAt": "2023-01-07T20:07:19.000Z",
        "isReachable": True,
        "lastSeen": "2023-10-28T04:42:15.000Z",
        "customIcon": "lighting_nightstand_light",
        "attributes": {
            "customName": "Light 2",
            "model": "3rd party bulb no startupOnOff",
            "manufacturer": "3rd party",
            "firmwareVersion": "2.3.093",
            "hardwareVersion": "2",
            "serialNumber": "84",
            "productCode": "LED2003G10",
            "isOn": False,
            "lightLevel": 100,
            "colorTemperature": 2710,
            "colorTemperatureMin": 4000,
            "colorTemperatureMax": 2202,
            "colorMode": "temperature",
            "identifyStarted": "2000-01-01T00:00:00.000Z",
            "identifyPeriod": 0,
            "permittingJoin": True,
            "otaStatus": "upToDate",
            "otaState": "readyToCheck",
            "otaProgress": 0,
            "otaPolicy": "autoUpdate",
            "otaScheduleStart": "00:00",
            "otaScheduleEnd": "00:00",
            "circadianRhythmMode": "",
        },
        "capabilities": {
            "canSend": [],
            "canReceive": ["customName", "isOn", "lightLevel"],
        },
        "room": {
            "id": "23g2w34-d0b7-42b3-a5a1-324zaerfg3",
            "name": "Bedroom",
            "color": "ikea_yellow_no_24",
            "icon": "rooms_bed",
        },
        "deviceSet": [],
        "remoteLinks": ["3838120-12f0-256-9c63-bdf2dfg232"],
        "isHidden": False,
    }

    light = dict_to_light(data, fake_client)
    assert light.dirigera_client == fake_client
    assert light.id == data["id"]
    assert light.is_reachable == data["isReachable"]
    assert light.attributes.custom_name == data["attributes"]["customName"]
    assert light.attributes.is_on == data["attributes"]["isOn"]
    assert light.attributes.startup_on_off is None
    assert light.attributes.light_level == data["attributes"]["lightLevel"]
    assert light.attributes.color_temperature == data["attributes"]["colorTemperature"]
    assert (
        light.attributes.color_temperature_min
        == data["attributes"]["colorTemperatureMin"]
    )
    assert (
        light.attributes.color_temperature_max
        == data["attributes"]["colorTemperatureMax"]
    )
    assert light.capabilities.can_receive == data["capabilities"]["canReceive"]
    assert light.room.id == data["room"]["id"]
    assert light.room.name == data["room"]["name"]
    assert light.attributes.firmware_version == data["attributes"]["firmwareVersion"]
    assert light.attributes.hardware_version == data["attributes"]["hardwareVersion"]
    assert light.attributes.model == data["attributes"]["model"]
    assert light.attributes.manufacturer == data["attributes"]["manufacturer"]
    assert light.attributes.serial_number == data["attributes"]["serialNumber"]
