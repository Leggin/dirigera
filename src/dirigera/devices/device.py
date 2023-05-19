from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class StartupEnum(Enum):
    START_ON = "startOn"
    START_OFF = "startOff"
    START_PREVIOUS = "startPrevious"
    START_TOGGLE = "startToggle"


@dataclass
class Device:
    device_id: str
    custom_name: str
    room_id: str
    room_name: str
    firmware_version: Optional[str]
    hardware_version: Optional[str]
    model: Optional[str]
    manufacturer: Optional[str]
    serial_number: Optional[str]
    can_receive: List[str]
