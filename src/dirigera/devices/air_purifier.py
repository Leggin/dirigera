from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Dict, List, Union

from packaging._parser import Op

from .device import Device

from ..hub.abstract_smart_home_hub import AbstractSmartHomeHub


class FanModeEnum(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTO = "auto"


data = {'id': '73b704c0-f619-4cdb-b144-79a92d6e3102_1', 'type': 'airPurifier', 'deviceType': 'airPurifier',
        'createdAt': '2023-05-05T19:45:07.000Z', 'isReachable': True, 'lastSeen': '2023-05-21T20:17:21.000Z',
        'attributes': {'customName': 'Air purifier 1', 'firmwareVersion': '1.1.001', 'hardwareVersion': '1',
                       'manufacturer': 'IKEA of Sweden', 'model': 'STARKVIND Air purifier', 'productCode': 'E2007',
                       'serialNumber': '0C4314FFFED62050', 'fanMode': 'auto', 'fanModeSequence': 'lowMediumHighAuto',
                       'motorRuntime': 6729, 'motorState': 10, 'filterAlarmStatus': False, 'filterElapsedTime': 23134,
                       'filterLifetime': 259200, 'childLock': False, 'statusLight': True, 'currentPM25': 19,
                       'identifyPeriod': 0, 'identifyStarted': '2000-01-01T00:00:00.000Z', 'permittingJoin': False,
                       'otaPolicy': 'autoUpdate', 'otaProgress': 0, 'otaScheduleEnd': '00:00',
                       'otaScheduleStart': '00:00', 'otaState': 'readyToCheck', 'otaStatus': 'upToDate'},
        'capabilities': {'canSend': [],
                         'canReceive': ['customName', 'fanMode', 'fanModeSequence', 'motorState', 'childLock',
                                        'statusLight']},
        'room': {'id': 'a9d6ac9a-12ac-401e-b104-e15d45a32afa', 'name': 'Office', 'color': 'ikea_blue_no_63',
                 'icon': 'rooms_office_chair'}, 'deviceSet': [], 'remoteLinks': [], 'isHidden': False}


@dataclass
class AirPurifier(Device):
    dirigera_client: AbstractSmartHomeHub
    is_reachable: bool
    fan_mode: Optional[None]
    fan_mode_sequence: Optional[None]  # todo
    child_lock: Optional[bool]
    motor_runtime: int
    motor_state: int
    filter_alarm_status: bool
    filter_elapsed_time: int
    filter_lifetime: int
    current_pm25: int

    def refresh(self) -> None:
        """Use stored device id to refresh all data of device."""
        fresh_data = self.dirigera_client.get(route=f"/devices/{self.device_id}")
        attributes: Dict[str, Any] = fresh_data["attributes"]
        self.device_id = fresh_data["id"]
        self.is_reachable = fresh_data["isReachable"]
        self.custom_name = attributes["customName"]
        self.can_receive = fresh_data["capabilities"]["canReceive"]
        self.room_id = fresh_data["room"]["id"]
        self.room_name = fresh_data["room"]["name"]

        self.firmware_version = attributes.get("firmwareVersion")
        self.hardware_version = attributes.get("hardwareVersion")
        self.model = attributes.get("model")
        self.manufacturer = attributes.get("manufacturer")
        self.serial_number = attributes.get("serialNumber")
        self.fan_mode = attributes.get("fanMode")
        self.fan_mode_sequence = attributes.get("fanModeSequence")
        self.motor_state = attributes.get("motorState")
        self.motor_runtime = attributes.get("motorRuntime")
        self.child_lock = attributes.get("childLock")
        self.filter_alarm_status = attributes.get("filterAlarmStatus")
        self.filter_elapsed_time = attributes.get("filterElapsedTime")
        self.filter_lifetime = attributes.get("filterLifetime")
        self.current_pm25 = attributes.get("currentPM25")

    def _set_data(self, data: Union[List[Dict], Dict]) -> None:
        if isinstance(data, dict):
            data = [data]
        self.dirigera_client.patch(route=f"/devices/{self.device_id}", data=data)
        self.refresh()

    def set_fan_mode(self, fan_mode: FanModeEnum) -> None:
        """Sets the fan mode (low, medium, high, auto)."""
        self._set_data(data={"attributes": {"fanMode": fan_mode.value}})


def dict_to_air_purifier(data: Dict[str, Any], dirigera_client: AbstractSmartHomeHub):
    attributes: Dict[str, Any] = data["attributes"]

    return AirPurifier(
        dirigera_client=dirigera_client,
        device_id=data["id"],
        is_reachable=data["isReachable"],
        custom_name=attributes["customName"],
        can_receive=data["capabilities"]["canReceive"],
        room_id=data["room"]["id"],
        room_name=data["room"]["name"],
        firmware_version=attributes.get("firmwareVersion"),
        hardware_version=attributes.get("hardwareVersion"),
        model=attributes.get("model"),
        manufacturer=attributes.get("manufacturer"),
        serial_number=attributes.get("serialNumber"),
        fan_mode=attributes.get("fanMode"),
        fan_mode_sequence=attributes.get("fanModeSequence"),
        motor_state=attributes.get("motorState"),
        motor_runtime=attributes.get("motorRuntime"),
        child_lock=attributes.get("childLock"),
        filter_alarm_status=attributes.get("filterAlarmStatus"),
        filter_elapsed_time=attributes.get("filterElapsedTime"),
        filter_lifetime=attributes.get("filterLifetime"),
        current_pm25=attributes.get("currentPM25"),
    )
