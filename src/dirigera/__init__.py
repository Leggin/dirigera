import typing

from .hub.hub import Hub

if typing.TYPE_CHECKING:
    from .devices.adaptive_profile import (
        AdaptiveProfile,
        AdaptiveProfileState,
        AdaptiveScheduleEntry,
    )
    from .devices.air_purifier import FanModeEnum, AirPurifierAttributes, AirPurifier
    from .devices.blinds import BlindsStateEnum, BlindAttributes, Blind
    from .devices.controller import Controller, ControllerAttributes
    from .devices.device import StartupEnum, Room, Device
    from .devices.electrical_sensor import ElectricalSensor, ElectricalSensorAttributes
    from .devices.environment_sensor import (
        EnvironmentSensor,
        EnvironmentSensorAttributes,
    )
    from .devices.light import Light, LightAttributes
    from .devices.light_sensor import LightSensor, LightSensorAttributes
    from .devices.motion_sensor import MotionSensor, MotionSensorAttributes
    from .devices.occupancy_sensor import OccupancySensor, OccupancySensorAttributes
    from .devices.open_close_sensor import OpenCloseSensor, OpenCloseSensorAttributes
    from .devices.outlet import Outlet, OutletAttributes
    from .devices.scene import (
        SceneAttributes,
        Icon,
        Info,
        EndTriggerEvent,
        Trigger,
        TriggerDetails,
        ControllerType,
        ClickPattern,
        ActionAttributes,
        Action,
        SceneType,
        Scene,
    )
    from .devices.water_sensor import WaterSensor, WaterSensorAttributes
