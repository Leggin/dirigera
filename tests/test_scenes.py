import datetime
from typing import Any, Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.scene import Scene, dict_to_scene

TEST_ID = "c9bbf831-6dcd-4442-8195-53eedb66a598"
TEST_NAME = "Tesscene"
TEST_ICON = "scenes_clean_sparkles"
TEST_LAST_COMPLETED = "2023-08-27T11:01:14.767Z"
TEST_LAST_TRIGGERED = "2023-08-27T11:01:14.767Z"
TEST_LAST_UNDO = "2023-08-27T10:29:33.049Z"


@pytest.fixture(name="fake_client")
def fixture_fake_client() -> FakeDirigeraHub:
    return FakeDirigeraHub()


@pytest.fixture(name="fake_scene")
def fixture_scene(fake_client: FakeDirigeraHub) -> Scene:
    return Scene(
        dirigeraClient=fake_client,
        **{
            "id": "c9bbf831-6dcd-4442-8195-53eedb66a598",
            "info": {"name": "Tesscene", "icon": "scenes_clean_sparkles"},
            "type": "userScene",
            "triggers": [
                {
                    "id": "f3ad4585-1a73-4e9c-9329-f926bedf509c",
                    "type": "app",
                    "triggeredAt": "2023-08-27T11:01:14.747Z",
                    "disabled": False,
                }
            ],
            "actions": [
                {
                    "id": "d0bf2ebf-3fcf-4e68-9810-0dc552e40388",
                    "type": "deviceSet",
                    "attributes": {"isOn": True, "lightLevel": 100},
                }
            ],
            "commands": [],
            "createdAt": "2023-08-27T10:28:48.096Z",
            "lastCompleted": "2023-08-27T11:01:14.767Z",
            "lastTriggered": "2023-08-27T11:01:14.767Z",
            "undoAllowedDuration": 30,
            "lastUndo": "2023-08-27T10:29:33.049Z",
        },
    )


def test_trigger(fake_scene: Scene, fake_client: FakeDirigeraHub) -> None:
    fake_scene.trigger()
    action = fake_client.post_actions.pop()
    assert action["route"] == f"/scenes/{fake_scene.id}/trigger"


def test_dict_to_scene(fake_client: FakeDirigeraHub) -> None:
    data: Dict[str, Any] = {
        "id": "c9bbf831-6dcd-4442-8195-53eedb66a598",
        "info": {"name": "Tesscene", "icon": "scenes_clean_sparkles"},
        "type": "userScene",
        "triggers": [
            {
                "id": "f3ad4585-1a73-4e9c-9329-f926bedf509c",
                "type": "app",
                "triggeredAt": "2023-08-27T11:01:14.747Z",
                "disabled": False,
            }
        ],
        "actions": [
            {
                "id": "d0bf2ebf-3fcf-4e68-9810-0dc552e40388",
                "type": "deviceSet",
                "attributes": {"isOn": True, "lightLevel": 100},
            }
        ],
        "commands": [],
        "createdAt": "2023-08-27T10:28:48.096Z",
        "lastCompleted": "2023-08-27T11:01:14.767Z",
        "lastTriggered": "2023-08-27T11:01:14.767Z",
        "undoAllowedDuration": 30,
        "lastUndo": "2023-08-27T10:29:33.049Z",
    }

    scene = dict_to_scene(data, fake_client)
    assert scene.id == TEST_ID
    assert scene.info.name == TEST_NAME
    assert scene.info.icon == TEST_ICON
    assert scene.last_completed == datetime.datetime.strptime(
        TEST_LAST_COMPLETED, "%Y-%m-%dT%H:%M:%S.%f%z"
    )
