from typing import Any, Dict, List, Optional
import pytest
from src.dirigera.hub.hub import Hub


def device_dict(
    id_: str,
    name: str,
    type_: str,
    device_type: str,
    extra_attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    attributes = {
        "customName": name,
        "model": "Fake Model",
        "manufacturer": "IKEA of Sweden",
        "firmwareVersion": "1.0.0",
        "hardwareVersion": "1",
    }
    attributes.update(extra_attributes or {})
    return {
        "id": id_,
        "type": type_,
        "deviceType": device_type,
        "createdAt": "2023-01-07T20:07:19.000Z",
        "isReachable": True,
        "lastSeen": "2023-10-28T04:42:15.000Z",
        "attributes": attributes,
        "capabilities": {"canSend": [], "canReceive": ["customName"]},
        "deviceSet": [],
        "remoteLinks": [],
        "isHidden": False,
    }


AIR_PURIFIER_ATTRIBUTES: Dict[str, Any] = {
    "fanMode": "auto",
    "fanModeSequence": "lowMediumHighAuto",
    "motorState": 20,
    "childLock": False,
    "statusLight": True,
    "motorRuntime": 100,
    "filterAlarmStatus": False,
    "filterElapsedTime": 100,
    "filterLifetime": 259200,
    "currentPM25": 5,
}


def build_devices(
    type_: str, device_type: str, extra_attributes: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    return [
        # a device of another type with the same name must never be returned
        device_dict("light-1", "Shared name", "light", "light"),
        device_dict("first", "First", type_, device_type, extra_attributes),
        device_dict("second", "Second", type_, device_type, extra_attributes),
    ]


DEVICE_CASES = [
    pytest.param(
        "get_open_close_sensor_by_name",
        "sensor",
        "openCloseSensor",
        {"isOpen": False},
        id="open_close_sensor",
    ),
    pytest.param(
        "get_environment_sensor_by_name",
        "sensor",
        "environmentSensor",
        {"currentTemperature": 21.5},
        id="environment_sensor",
    ),
    pytest.param(
        "get_water_sensor_by_name",
        "sensor",
        "waterSensor",
        {"waterLeakDetected": False},
        id="water_sensor",
    ),
    pytest.param(
        "get_air_purifier_by_name",
        "airPurifier",
        "airPurifier",
        AIR_PURIFIER_ATTRIBUTES,
        id="air_purifier",
    ),
    pytest.param(
        "get_light_sensor_by_name",
        "sensor",
        "lightSensor",
        {"illuminance": 100},
        id="light_sensor",
    ),
    pytest.param(
        "get_occupancy_sensor_by_name",
        "sensor",
        "occupancySensor",
        {"isDetected": False},
        id="occupancy_sensor",
    ),
]


@pytest.fixture(name="hub")
def fixture_hub() -> Hub:
    return Hub(token="fake-token", ip_address="127.0.0.1")


@pytest.mark.parametrize(
    "method_name, type_, device_type, extra_attributes", DEVICE_CASES
)
def test_get_device_by_name_finds_device_independent_of_order(
    monkeypatch: pytest.MonkeyPatch,
    hub: Hub,
    method_name: str,
    type_: str,
    device_type: str,
    extra_attributes: Dict[str, Any],
) -> None:
    devices = build_devices(type_, device_type, extra_attributes)
    monkeypatch.setattr(Hub, "get", lambda _self, _route: devices)
    get_by_name = getattr(hub, method_name)

    assert get_by_name("First").id == "first"
    assert get_by_name("Second").id == "second"

    # the hub does not guarantee the order of the devices
    devices.reverse()
    assert get_by_name("First").id == "first"
    assert get_by_name("Second").id == "second"


@pytest.mark.parametrize(
    "method_name, type_, device_type, extra_attributes", DEVICE_CASES
)
def test_get_device_by_name_raises_if_no_device_has_that_name(
    monkeypatch: pytest.MonkeyPatch,
    hub: Hub,
    method_name: str,
    type_: str,
    device_type: str,
    extra_attributes: Dict[str, Any],
) -> None:
    devices = build_devices(type_, device_type, extra_attributes)
    monkeypatch.setattr(Hub, "get", lambda _self, _route: devices)
    get_by_name = getattr(hub, method_name)

    with pytest.raises(AssertionError, match="No .* found with name Unknown"):
        get_by_name("Unknown")

    # a device of another type that has the requested name is not a match
    with pytest.raises(AssertionError, match="No .* found with name Shared name"):
        get_by_name("Shared name")
