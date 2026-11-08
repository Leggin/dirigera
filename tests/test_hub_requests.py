from typing import Any, List, Tuple, Union

import pytest
import requests

from src.dirigera.hub.hub import Hub


def _response(status_code: int, body: bytes = b"{}") -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = body  # pylint: disable=protected-access
    return response


class FakeSession:
    """Stands in for requests.Session and hands out the given outcomes in order."""

    def __init__(self, *outcomes: Union[requests.Response, Exception]) -> None:
        self.outcomes = list(outcomes)
        self.calls: List[Tuple[str, str, Any]] = []
        self.closed = 0

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        self.calls.append((method, url, kwargs))
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    def close(self) -> None:
        self.closed += 1


class FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0

    def monotonic(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


@pytest.fixture(name="clock", autouse=True)
def fixture_clock(monkeypatch: pytest.MonkeyPatch) -> FakeClock:
    clock = FakeClock()
    monkeypatch.setattr("src.dirigera.hub.hub.monotonic", clock.monotonic)
    return clock


def _hub(session: FakeSession) -> Hub:
    hub = Hub(token="token", ip_address="127.0.0.1")
    hub._session = session  # type: ignore[assignment] # pylint: disable=protected-access
    return hub


def test_hub_keeps_one_session() -> None:
    hub = Hub(token="token", ip_address="127.0.0.1")
    assert isinstance(hub._session, requests.Session)  # pylint: disable=protected-access


def test_all_requests_go_through_the_session() -> None:
    session = FakeSession(*(_response(200) for _ in range(4)))
    hub = _hub(session)

    hub.get("/devices")
    hub.patch("/devices/1", [{"attributes": {"isOn": True}}])
    hub.post("/scenes/1/trigger")
    hub.delete("/scenes/1")

    assert [(method, url) for method, url, _ in session.calls] == [
        ("GET", "https://127.0.0.1:8443/v1/devices"),
        ("PATCH", "https://127.0.0.1:8443/v1/devices/1"),
        ("POST", "https://127.0.0.1:8443/v1/scenes/1/trigger"),
        ("DELETE", "https://127.0.0.1:8443/v1/scenes/1"),
    ]
    _, _, kwargs = session.calls[1]
    assert kwargs == {
        "headers": {"Authorization": "Bearer token"},
        "json": [{"attributes": {"isOn": True}}],
        "timeout": 10,
        "verify": False,
    }
    assert session.closed == 0


def test_connection_used_recently_is_reused(clock: FakeClock) -> None:
    session = FakeSession(_response(200), _response(200))
    hub = _hub(session)

    hub.get("/devices")
    clock.advance(2.9)
    hub.get("/devices")

    assert session.closed == 0


def test_connection_idle_too_long_is_not_reused(clock: FakeClock) -> None:
    session = FakeSession(_response(200), _response(200))
    hub = _hub(session)

    hub.get("/devices")
    assert session.closed == 0
    clock.advance(3.1)
    hub.post("/scenes/1/trigger")

    assert session.closed == 1
    assert len(session.calls) == 2


def test_idle_time_counts_from_the_end_of_the_last_request(clock: FakeClock) -> None:
    session = FakeSession(_response(200), _response(200))

    def slow_request(method: str, url: str, **kwargs: Any) -> requests.Response:
        clock.advance(5)
        return FakeSession.request(session, method, url, **kwargs)

    hub = _hub(session)
    session.request = slow_request  # type: ignore[method-assign]

    hub.get("/devices")
    clock.advance(1)
    hub.get("/devices")

    assert session.closed == 0


@pytest.mark.parametrize(
    "call",
    [
        lambda hub: hub.get("/devices"),
        lambda hub: hub.patch("/devices/1", [{"attributes": {"isOn": True}}]),
        lambda hub: hub.delete("/scenes/1"),
    ],
    ids=["get", "patch", "delete"],
)
def test_dropped_connection_is_retried_once(call: Any) -> None:
    session = FakeSession(requests.ConnectionError("RemoteDisconnected"), _response(200))
    hub = _hub(session)

    call(hub)

    assert len(session.calls) == 2
    assert session.calls[0] == session.calls[1]
    assert session.closed == 1


def test_second_dropped_connection_is_raised() -> None:
    session = FakeSession(
        requests.ConnectionError("RemoteDisconnected"),
        requests.ConnectionError("RemoteDisconnected"),
    )
    hub = _hub(session)

    with pytest.raises(requests.ConnectionError):
        hub.get("/devices")
    assert len(session.calls) == 2


def test_post_is_not_retried() -> None:
    session = FakeSession(requests.ConnectionError("RemoteDisconnected"), _response(200))
    hub = _hub(session)

    with pytest.raises(requests.ConnectionError):
        hub.post("/scenes", {"info": {}})
    assert len(session.calls) == 1
    assert session.closed == 1


def test_connect_timeout_is_not_retried() -> None:
    session = FakeSession(requests.ConnectTimeout("hub unreachable"), _response(200))
    hub = _hub(session)

    with pytest.raises(requests.ConnectTimeout):
        hub.get("/devices")
    assert len(session.calls) == 1


def test_http_error_is_not_retried() -> None:
    session = FakeSession(_response(500), _response(200))
    hub = _hub(session)

    with pytest.raises(requests.HTTPError):
        hub.patch("/devices/1", [{"attributes": {"isOn": True}}])
    assert len(session.calls) == 1
    assert session.closed == 0
