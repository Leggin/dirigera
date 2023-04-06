from dataclasses import dataclass


@dataclass
class Device:
    device_id: str
    custom_name: str
    room_id: str
    room_name: str
    can_receive: list[str]
