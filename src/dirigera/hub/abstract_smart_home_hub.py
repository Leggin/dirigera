import abc
from typing import Any


class AbstractSmartHomeHub(abc.ABC):
    @abc.abstractmethod
    def patch(self, route: str, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, route: str) -> dict[str, Any]:
        raise NotImplementedError


class FakeDirigeraHub(AbstractSmartHomeHub):
    def __init__(self) -> None:
        self.patch_actions: list = []
        self.get_actions: list = []

    def patch(self, route: str, data: dict[str, Any]) -> dict[str, Any]:
        self.patch_actions.append({"route": route, "data": data})

    def get(self, route: str) -> dict[str, Any]:
        self.get_actions.append({"route": route})
