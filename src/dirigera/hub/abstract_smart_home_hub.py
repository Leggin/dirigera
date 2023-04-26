import abc
from typing import Any, Dict, List


class AbstractSmartHomeHub(abc.ABC):
    @abc.abstractmethod
    def patch(self, route: str, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, route: str) -> Dict[str, Any]:
        raise NotImplementedError


class FakeDirigeraHub(AbstractSmartHomeHub):
    def __init__(self) -> None:
        self.patch_actions: List = []
        self.get_actions: List = []

    def patch(self, route: str, data: Dict[str, Any]) -> Dict[str, Any]:
        self.patch_actions.append({"route": route, "data": data})

    def get(self, route: str) -> Dict[str, Any]:
        self.get_actions.append({"route": route})
