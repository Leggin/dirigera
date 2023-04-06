from dataclasses import dataclass


@dataclass
class Device:
    device_id: str
    custom_name: str
    room_id: str
    room_name: str
    firmware_version: str | None
    hardware_version: str | None
    model: str | None
    manufacturer: str | None
    serial_number: str | None
    can_receive: list[str]
