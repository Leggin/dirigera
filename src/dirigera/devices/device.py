from __future__ import annotations
import datetime
from enum import Enum
from typing import Any, Dict, Optional, List

from pydantic import BaseModel, ConfigDict, alias_generators


class StartupEnum(Enum):
    START_ON = "startOn"
    START_OFF = "startOff"
    START_PREVIOUS = "startPrevious"
    START_TOGGLE = "startToggle"


class Attributes(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, arbitrary_types_allowed=True
    )

    custom_name: str
    model: str
    manufacturer: str
    firmware_version: str
    hardware_version: str
    serial_number: Optional[str] = None
    product_code: Optional[str] = None
    ota_status: Optional[str] = None
    ota_state: Optional[str] = None
    ota_progress: Optional[int] = None
    ota_policy: Optional[str] = None
    ota_schedule_start: Optional[datetime.time] = None
    ota_schedule_end: Optional[datetime.time] = None


class Capabilities(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, arbitrary_types_allowed=True
    )

    can_send: List[str]
    can_receive: List[str]


class Room(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, arbitrary_types_allowed=True
    )

    id: str
    name: str
    color: str
    icon: str


class Device(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, arbitrary_types_allowed=True
    )

    id: str
    type: str
    device_type: str
    created_at: datetime.datetime
    is_reachable: bool
    last_seen: datetime.datetime
    attributes: Attributes
    capabilities: Capabilities
    room: Room
    device_set: List
    remote_links: List[str]
    is_hidden: Optional[bool] = None

    def _reload(self, data: Dict[str, Any]) -> Device:
        return Device(**data)
