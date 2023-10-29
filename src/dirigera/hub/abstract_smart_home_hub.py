import abc
from typing import Any, Dict, List, Optional


class AbstractSmartHomeHub(abc.ABC):
    @abc.abstractmethod
    def patch(self, route: str, data: List[Dict[str, Any]]) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, route: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def post(self, route: str, data: Optional[Dict[str, Any]] = None) -> Any:
        raise NotImplementedError


class FakeDirigeraHub(AbstractSmartHomeHub):
    def __init__(self) -> None:
        self.patch_actions: List = []
        self.post_actions: List = []
        self.get_actions: List = []
        self.get_action_replys: Dict = {}

    def patch(self, route: str, data: List[Dict[str, Any]]) -> Any:
        self.patch_actions.append({"route": route, "data": data})
        return {"route": route, "data": data}

    def get(self, route: str) -> Any:
        self.get_actions.append({"route": route})
        return self.get_action_replys[route]

    def post(self, route: str, data: Optional[Dict[str, Any]] = None) -> Any:
        self.post_actions.append({"route": route, "data": data})
