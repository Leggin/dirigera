import pytest
from src.dirigera.hub.abstract_smart_home_hub import FakeDirigeraHub
from src.dirigera.devices.scene import Scene, dict_to_scene

TEST_ID = "00000000-0000-0000-0000-000000000000"
TEST_NAME = "NAME"
TEST_ICON = "ICON"
TEST_LAST_COMPLETED = "2023-10-26T10:39:39.176Z"
TEST_LAST_TRIGGERED = "2023-10-26T10:39:39.176Z"
TEST_LAST_UNDO = "2023-10-26T10:42:14.847Z"

@pytest.fixture(name="fake_client")
def fixture_fake_client():
    return FakeDirigeraHub()


@pytest.fixture(name="fake_scene")
def fixture_scene(fake_client: FakeDirigeraHub):
    return Scene(
        dirigera_client=fake_client,
        scene_id=TEST_ID,
        name=TEST_NAME,
        icon=TEST_ICON,
        last_completed=TEST_LAST_COMPLETED,
        last_triggered=TEST_LAST_TRIGGERED,
        last_undo=TEST_LAST_UNDO
    )


def test_trigger(fake_scene, fake_client) -> None:
    fake_scene.trigger()
    action = fake_client.post_actions.pop()
    assert action["route"] == f"/scenes/{fake_scene.scene_id}/trigger"


def test_dict_to_scene(fake_client):
    data = {
        "id": TEST_ID,
        "info": {
            "name": TEST_NAME,
            "icon": TEST_ICON
        },
        "lastCompleted": TEST_LAST_COMPLETED,
        "lastTriggered": TEST_LAST_TRIGGERED,
        "lastUndo": TEST_LAST_UNDO
    }

    scene = dict_to_scene(data, fake_client)
    assert scene.scene_id == TEST_ID
    assert scene.name == TEST_NAME
    assert scene.icon == TEST_ICON
