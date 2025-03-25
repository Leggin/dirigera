from typing import Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.water_sensor import dict_to_water_sensor
from src.dirigera.devices.water_sensor import WaterSensor

@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="fake_water_sensor_dict_non_ikea")
def fixture_water_sensor_dict_non_ikea() -> Dict:
    return {
        "id": "2b107b0b-73f0-4809-a900-4783273d7104_1",
        "type": "sensor",
        "deviceType": "waterSensor",
        "createdAt": "2024-04-17T12:19:50.000Z",
        "isReachable": True,
        "lastSeen": "2024-04-17T12:34:42.000Z",
        "attributes": {
            "customName": "Watermelder",
            "firmwareVersion": "",
            "hardwareVersion": "",
            "manufacturer": "SONOFF",
            "model": "Fake SONOFF Model",
            "productCode": "E2202",
            "serialNumber": "0",
            "waterLeakDetected": False,
            "permittingJoin": False,
        },
        "capabilities": {
            "canSend": [],
            "canReceive": [
"customName"
        ]
        },
        "room": {
            "id": "f1743e4c-3a87-4f6b-90a4-3e915b8ed753",
            "name": "Zolder",
            "color": "ikea_pink_no_8",
            "icon": "rooms_washing_machine"
        },
        "deviceSet": [],
        "remoteLinks": [],
        "isHidden": False
    }



@pytest.fixture(name="fake_water_sensor_dict")
def fixture_water_sensor_dict() -> Dict:
    return {
        "id": "2b107b0b-73f0-4809-a900-4783273d7104_1",
        "type": "sensor",
        "deviceType": "waterSensor",
        "createdAt": "2024-04-17T12:19:50.000Z",
        "isReachable": True,
        "lastSeen": "2024-04-17T12:34:42.000Z",
        "attributes": {
            "customName": "Watermelder",
            "firmwareVersion": "1.0.7",
            "hardwareVersion": "1",
            "manufacturer": "IKEA of Sweden",
            "model": "BADRING Water Leakage Sensor",
            "productCode": "E2202",
            "serialNumber": "3410F4FFFE8F815D",
            "batteryPercentage": 100,
            "waterLeakDetected": True,
            "permittingJoin": False,
            "otaPolicy": "autoUpdate",
            "otaProgress": 0,
            "otaScheduleEnd": "00:00",
            "otaScheduleStart": "00:00",
            "otaState": "readyToCheck",
            "otaStatus": "upToDate"
        },
        "capabilities": {
            "canSend": [],
            "canReceive": [
"customName"
        ]
        },
        "room": {
            "id": "f1743e4c-3a87-4f6b-90a4-3e915b8ed753",
            "name": "Zolder",
            "color": "ikea_pink_no_8",
            "icon": "rooms_washing_machine"
        },
        "deviceSet": [],
        "remoteLinks": [],
        "isHidden": False
    }


@pytest.fixture(name="fake_water_sensor")
def fixture_water_sensor(fake_water_sensor_dict: Dict, fake_client: FakeDirigeraHub) -> WaterSensor:
    return WaterSensor(dirigeraClient=fake_client, **fake_water_sensor_dict)

def test_set_name(fake_water_sensor: WaterSensor, fake_client: FakeDirigeraHub) -> None:
    new_name = "teapot"
    fake_water_sensor.set_name(new_name)
    action = fake_client.patch_actions.pop()
    assert action["route"] == f"/devices/{fake_water_sensor.id}"
    assert action["data"] == [{"attributes": {"customName": new_name}}]
    assert fake_water_sensor.attributes.custom_name == new_name

def test_dict_to_water_sensor(fake_water_sensor_dict: Dict, fake_client: FakeDirigeraHub) -> None:
    water_sensor = dict_to_water_sensor(fake_water_sensor_dict, fake_client)

    assert water_sensor.dirigera_client == fake_client
    assert water_sensor.id == fake_water_sensor_dict["id"]
    assert water_sensor.is_reachable == fake_water_sensor_dict["isReachable"]
    assert water_sensor.attributes.battery_percentage == 100
    assert water_sensor.attributes.water_leak_detected

def test_dict_to_water_sensor_non_ikea(fake_water_sensor_dict_non_ikea: Dict, fake_client: FakeDirigeraHub) -> None:
    water_sensor = dict_to_water_sensor(fake_water_sensor_dict_non_ikea, fake_client)

    assert water_sensor.attributes.battery_percentage is None
