import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.light import dict_to_light
from src.dirigera.devices.light import Light, StartupEnum


@pytest.fixture(name="fake_client")
def fixture_fake_client():
    return FakeDirigeraHub()


@pytest.fixture(name="fake_light")
def fixture_light(fake_client: FakeDirigeraHub):
    return Light(
        dirigera_client=fake_client,
        device_id="abcd",
        is_reachable=True,
        custom_name="good lamp",
        is_on=True,
        startup_on_off=StartupEnum.START_ON,
        light_level=20,
        color_temp=45,
        color_temp_min=4000,
        color_temp_max=2000,
        color_hue=200,
        color_saturation=0.7,
        room_id="123",
        room_name="Upstairs",
        firmware_version="1",
        hardware_version="1",
        model="a",
        manufacturer="IKEA",
        serial_number="abc-abc",
        can_receive=[
            "customName",
            "isOn",
            "lightLevel",
            "colorTemperature",
            "colorHue",
            "colorSaturation",
        ],
    )


def test_set_name(fake_light: Light, fake_client: FakeDirigeraHub):
    new_name = "stadtlampefluss"
    fake_light.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_light.custom_name == new_name


def test_set_light_on(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    fake_light.set_light(True)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [{"attributes": {"isOn": True}}]
    assert fake_light.is_on


def test_set_light_off(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    fake_light.set_light(False)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [{"attributes": {"isOn": False}}]
    assert not fake_light.is_on


def test_set_light_level(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    level = 80
    fake_light.set_light_level(level)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [{"attributes": {"lightLevel": level}}]
    assert fake_light.light_level == level


def test_set_color_temperature(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    temp = 2200
    fake_light.set_color_temperature(temp)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [{"attributes": {"colorTemperature": temp}}]
    assert fake_light.color_temp == temp


def test_set_light_color(fake_light: Light, fake_client: FakeDirigeraHub) -> None:
    hue = 120
    saturation = 0.9
    fake_light.set_light_color(hue, saturation)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [
        {"attributes": {"colorHue": hue, "colorSaturation": saturation}}
    ]
    assert fake_light.color_hue == hue
    assert fake_light.color_saturation == saturation


def test_set_startup_behaviour_off(
    fake_light: Light, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_OFF
    fake_light.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour}}]
    assert fake_light.startup_on_off == behaviour


def test_set_startup_behaviour_on(
    fake_light: Light, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_ON
    fake_light.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour}}]
    assert fake_light.startup_on_off == behaviour

def test_set_startup_behaviour_previous(
    fake_light: Light, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_PREVIOUS
    fake_light.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour}}]
    assert fake_light.startup_on_off == behaviour

def test_set_startup_behaviour_toggle(
    fake_light: Light, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_TOGGLE
    fake_light.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_light.device_id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour}}]
    assert fake_light.startup_on_off == behaviour

def test_dict_to_light(fake_client: FakeDirigeraHub):
    data = {
        "id": "1237-343-2dfa",
        "type": "light",
        "deviceType": "light",
        "isReachable": True,
        "attributes": {
            "customName": "Light 2",
            "model": "TRADFRI bulb E27 WW 806lm",
            "manufacturer": "IKEA of Sweden",
            "firmwareVersion": "2.3.093",
            "hardwareVersion": "2",
            "isOn": False,
            "startupOnOff": "startOn",
            "lightLevel": 100,
            "colorTemperature": 2710,
            "colorTemperatureMin": 4000,
            "colorTemperatureMax": 2202,
            "colorMode": "temperature",
        },
        "capabilities": {
            "canSend": [],
            "canReceive": ["customName", "isOn", "lightLevel"],
        },
        "room": {
            "id": "19aa77553369",
            "name": "Living room",
        },
    }

    light = dict_to_light(data, fake_client)
    assert light.dirigera_client == fake_client
    assert light.device_id == data["id"]
    assert light.is_reachable == data["isReachable"]
    assert light.custom_name == data["attributes"]["customName"]
    assert light.is_on == data["attributes"]["isOn"]
    assert light.startup_on_off == data["attributes"]["startupOnOff"]
    assert light.light_level == data["attributes"]["lightLevel"]
    assert light.color_temp == data["attributes"]["colorTemperature"]
    assert light.color_temp_min == data["attributes"]["colorTemperatureMin"]
    assert light.color_temp_max == data["attributes"]["colorTemperatureMax"]
    assert light.can_receive == data["capabilities"]["canReceive"]
    assert light.room_id == data["room"]["id"]
    assert light.room_name == data["room"]["name"]
    assert light.firmware_version == data["attributes"]["firmwareVersion"]
    assert light.hardware_version == data["attributes"]["hardwareVersion"]
    assert light.model == data["attributes"]["model"]
    assert light.manufacturer == data["attributes"]["manufacturer"]
