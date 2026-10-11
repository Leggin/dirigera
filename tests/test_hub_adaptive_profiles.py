from typing import Any, Dict
import pytest
from src.dirigera.hub.hub import Hub

PROFILE_ID = "19d31644-5fc5-405b-8f0c-b2f0634190f6"

# the profile as reported by /home, the hub did not send a name for it
HOME: Dict[str, Any] = {
    "adaptiveProfiles": [
        {
            "id": PROFILE_ID,
            "adaptiveSchedule": [
                {"startTime": "00:00", "lightLevel": 10, "colorTemperature": 1000},
                {"startTime": "05:00", "lightLevel": 10, "colorTemperature": 1000},
                {"startTime": "08:00", "lightLevel": 90, "colorTemperature": 3600},
                {"startTime": "14:00", "lightLevel": 100, "colorTemperature": 8000},
                {"startTime": "18:00", "lightLevel": 90, "colorTemperature": 2400},
                {"startTime": "20:00", "lightLevel": 80, "colorTemperature": 1800},
            ],
        }
    ]
}


@pytest.fixture(name="hub")
def fixture_hub() -> Hub:
    return Hub(token="fake-token", ip_address="127.0.0.1")


def test_get_adaptive_profiles(monkeypatch: pytest.MonkeyPatch, hub: Hub) -> None:
    replies = {"/home": HOME}
    monkeypatch.setattr(Hub, "get", lambda _self, route: replies[route])

    profiles = hub.get_adaptive_profiles()

    assert len(profiles) == 1
    assert profiles[0].id == PROFILE_ID
    assert profiles[0].name is None
    schedule = profiles[0].adaptive_schedule
    assert [entry.start_time for entry in schedule] == [
        "00:00",
        "05:00",
        "08:00",
        "14:00",
        "18:00",
        "20:00",
    ]
    assert [entry.light_level for entry in schedule] == [10, 10, 90, 100, 90, 80]
    assert [entry.color_temperature for entry in schedule] == [
        1000,
        1000,
        3600,
        8000,
        2400,
        1800,
    ]


def test_get_adaptive_profiles_without_profiles(
    monkeypatch: pytest.MonkeyPatch, hub: Hub
) -> None:
    monkeypatch.setattr(Hub, "get", lambda _self, _route: {})
    assert hub.get_adaptive_profiles() == []
