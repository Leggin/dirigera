import datetime
from typing import Any, Dict
import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.scene import Scene, dict_to_scene, ControllerType

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
    data1: Dict[str, Any] = {
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

    scene1 = dict_to_scene(data1, fake_client)
    assert scene1.id == TEST_ID
    assert scene1.info.name == TEST_NAME
    assert scene1.info.icon.value == TEST_ICON
    assert scene1.last_completed == datetime.datetime.strptime(
        TEST_LAST_COMPLETED, "%Y-%m-%dT%H:%M:%S.%f%z"
    )

    data2: Dict[str, Any] = {
        "id": "00a0a00a-0aa0-0000-a000-00a0000a0a00",
        "info": {
            "name": "Night",
            "icon": "scenes_clean_sparkles"
        },
        "type": "userScene",
        "triggers": [
            {
                "id": "0000a0a0-0a00-000a-0a00-aaaaaa000000",
                "type": "app",
                "triggeredAt": "2024-04-23T21:34:51.619Z",
                "disabled": False
            },
            {
                "id": "a0000000-a000-0000-aaaa-0aaa000aa000",
                "type": "controller",
                "triggeredAt": "2024-04-20T05:49:20.178Z",
                "disabled": False,
                "trigger": {
                    "days": [
                        "Mon",
                        "Tue",
                        "Wed",
                        "Thu",
                        "Fri",
                        "Sat",
                        "Sun"
                    ],
                    "controllerType": "shortcutController",
                    "clickPattern": "doublePress",
                    "buttonIndex": 0,
                    "deviceId": "0000aaaa-0000-0000-aa00-0a0aa0a000a0_2"
                }
            },
            {
                "id": "a0000000-a000-0000-aaaa-0aaa000aa000",
                "type": "sunriseSunset",
                "triggeredAt": "2024-04-24T17:49:00.989Z",
                "disabled": False,
                "trigger": {
                    "days": [
                        "Tue",
                        "Wed",
                        "Sun",
                        "Mon",
                        "Fri",
                        "Sat",
                        "Thu"
                    ],
                    "type": "sunset",
                    "offset": 0
                },
                "nextTriggerAt": "2024-04-25T17:49:00.000Z"
            }
        ],
        "actions": [],
        "commands": [],
        "createdAt": "2023-11-06T22:10:14.806Z",
        "lastCompleted": "2024-04-24T05:13:24.352Z",
        "lastTriggered": "2024-04-24T05:13:24.352Z",
        "undoAllowedDuration": 30
    }

    scene2 = dict_to_scene(data2, fake_client)
    assert scene2.triggers[1].trigger is not None
    assert scene2.triggers[1].trigger.controllerType == ControllerType.SHORTCUT_CONTROLLER
