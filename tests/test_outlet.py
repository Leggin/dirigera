import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.outlet import dict_to_outlet
from src.dirigera.devices.outlet import Outlet
from src.dirigera.devices.device import StartupEnum


@pytest.fixture(name="fake_client")
def fixture_fake_client():
    return FakeDirigeraHub()


@pytest.fixture(name="fake_outlet")
def fixture_outlet(fake_client: FakeDirigeraHub):
    return Outlet(
        dirigera_client=fake_client,
        device_id="abcd",
        is_reachable=True,
        custom_name="coffee",
        is_on=False,
        startup_on_off=StartupEnum.START_PREVIOUS,
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
        ],
    )


def test_set_name(fake_outlet: Outlet, fake_client: FakeDirigeraHub):
    new_name = "teapot"
    fake_outlet.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_outlet.device_id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_outlet.custom_name == new_name


def test_set_outlet_on(fake_outlet: Outlet, fake_client: FakeDirigeraHub) -> None:
    fake_outlet.set_on(True)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_outlet.device_id}"
    assert action["data"] == [{"attributes": {"isOn": True}}]
    assert fake_outlet.is_on


def test_set_outlet_off(fake_outlet: Outlet, fake_client: FakeDirigeraHub) -> None:
    fake_outlet.set_on(False)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_outlet.device_id}"
    assert action["data"] == [{"attributes": {"isOn": False}}]
    assert not fake_outlet.is_on


def test_set_startup_behaviour_off(
    fake_outlet: Outlet, fake_client: FakeDirigeraHub
) -> None:
    behaviour = StartupEnum.START_OFF
    fake_outlet.set_startup_behaviour(behaviour)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_outlet.device_id}"
    assert action["data"] == [{"attributes": {"startupOnOff": behaviour.value}}]
    assert fake_outlet.startup_on_off == behaviour

def test_dict_to_outlet(fake_client: FakeDirigeraHub):
    data = {
        'id': 'f430fd01',
        'type': 'outlet',
        'deviceType': 'outlet',
        'createdAt': '2022-12-18',
        'isReachable': True,
        'lastSeen': '2023-05-19',
        'attributes': {
            'customName': 'coffee',
            'model': 'TRADFRI control outlet',
            'manufacturer': 'IKEA of Sweden',
            'firmwareVersion': '2.3.089',
            'hardwareVersion': '1',
            'serialNumber': '1',
            'productCode': 'E1603',
            'isOn': True,
            'startupOnOff': 'startPrevious',
            'lightLevel': 100,
            'startUpCurrentLevel': -1,
            'identifyStarted': '2000-01-01T00:00:00.000Z',
            'identifyPeriod': 0,
            'permittingJoin': False,
            'otaStatus': 'upToDate',
            'otaState': 'readyToCheck',
            'otaProgress': 0,
            'otaPolicy': 'autoUpdate',
            'otaScheduleStart': '00:00',
            'otaScheduleEnd': '00:00'
        },
        'capabilities': {
            'canSend': [],
            'canReceive': ['customName', 'isOn', 'lightLevel']
        },
        'room': {
            'id': '63ffdf20',
            'name': 'kitchen',
            'color': 'color',
            'icon': 'icon'
        },
        'deviceSet': [],
        'remoteLinks': ['152461d3'],
        'isHidden': False
    }

    outlet = dict_to_outlet(data, fake_client)
    assert outlet.dirigera_client == fake_client
    assert outlet.device_id == data["id"]
    assert outlet.is_reachable == data["isReachable"]
    assert outlet.custom_name == data["attributes"]["customName"]
    assert outlet.is_on == data["attributes"]["isOn"]
    assert outlet.startup_on_off == StartupEnum(data["attributes"]["startupOnOff"])
    assert outlet.can_receive == data["capabilities"]["canReceive"]
    assert outlet.room_id == data["room"]["id"]
    assert outlet.room_name == data["room"]["name"]
    assert outlet.firmware_version == data["attributes"]["firmwareVersion"]
    assert outlet.hardware_version == data["attributes"]["hardwareVersion"]
    assert outlet.model == data["attributes"]["model"]
    assert outlet.manufacturer == data["attributes"]["manufacturer"]
    assert outlet.serial_number == data["attributes"]["serialNumber"]
