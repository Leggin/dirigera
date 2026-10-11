from typing import Any, Dict, List

import pytest

from src.dirigera.devices.electrical_sensor import ElectricalSensor
from src.dirigera.devices.outlet import Outlet
from src.dirigera.hub.hub import Hub

RELATION_ID = "44444444-4444-4444-4444-444444444444"


def _device(id_: str, type_: str, device_type: str, attributes: Dict) -> Dict:
    return {
        "id": id_,
        "relationId": RELATION_ID,
        "type": type_,
        "deviceType": device_type,
        "createdAt": "2025-10-01T18:28:57.000Z",
        "isReachable": True,
        "lastSeen": "2025-10-02T17:30:48.000Z",
        "attributes": {
            "customName": "Grill Plug",
            "firmwareVersion": "1.0.0",
            "hardwareVersion": "1",
            "manufacturer": "IKEA of Sweden",
            "model": "GRILLPLATS Plug",
            "productCode": "E2491-EU",
            **attributes,
        },
        "capabilities": {"canSend": [], "canReceive": ["customName"]},
        "deviceSet": [],
        "remoteLinks": [],
    }


@pytest.fixture(name="grillplats_devices")
def fixture_grillplats_devices() -> List[Dict]:
    # The plug is reported as two devices which share the same relationId.
    # Some firmware versions report the metering part with type "outlet".
    return [
        _device(f"{RELATION_ID}_1", "outlet", "outlet", {"isOn": True}),
        _device(
            f"{RELATION_ID}_2",
            "outlet",
            "electricalSensor",
            {"currentActivePower": 1.4, "totalEnergyConsumed": 0.706},
        ),
    ]


@pytest.fixture(name="hub")
def fixture_hub(
    grillplats_devices: List[Dict], monkeypatch: pytest.MonkeyPatch
) -> Hub:
    hub = Hub(token="token", ip_address="127.0.0.1")
    replies: Dict[str, Any] = {"/devices": grillplats_devices}
    replies.update({f"/devices/{device['id']}": device for device in grillplats_devices})
    monkeypatch.setattr(hub, "get", lambda route: replies[route])
    return hub


def test_get_outlets_ignores_electrical_sensors(hub: Hub) -> None:
    outlets = hub.get_outlets()
    assert [outlet.id for outlet in outlets] == [f"{RELATION_ID}_1"]
    assert outlets[0].attributes.is_on


def test_get_electrical_sensors(hub: Hub) -> None:
    sensors = hub.get_electrical_sensors()
    assert [sensor.id for sensor in sensors] == [f"{RELATION_ID}_2"]
    assert sensors[0].relation_id == RELATION_ID
    assert sensors[0].attributes.current_active_power == 1.4


def test_get_outlet_by_id(hub: Hub) -> None:
    assert hub.get_outlet_by_id(f"{RELATION_ID}_1").id == f"{RELATION_ID}_1"
    with pytest.raises(ValueError):
        hub.get_outlet_by_id(f"{RELATION_ID}_2")


def test_get_electrical_sensor_by_id(hub: Hub) -> None:
    assert (
        hub.get_electrical_sensor_by_id(f"{RELATION_ID}_2").id == f"{RELATION_ID}_2"
    )
    with pytest.raises(ValueError):
        hub.get_electrical_sensor_by_id(f"{RELATION_ID}_1")


def test_get_all_devices_contains_outlet_and_electrical_sensor(hub: Hub) -> None:
    devices: List[Any] = hub.get_all_devices()
    assert len(devices) == 2
    assert len([d for d in devices if isinstance(d, Outlet)]) == 1
    assert len([d for d in devices if isinstance(d, ElectricalSensor)]) == 1
