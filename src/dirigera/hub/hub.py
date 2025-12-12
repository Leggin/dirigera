# pylint:disable=too-many-public-methods
import ssl
from typing import Any, Dict, List, Optional
import requests
import websocket  # type: ignore
import urllib3
from requests import HTTPError
from urllib3.exceptions import InsecureRequestWarning

from .utils import camelize_dict
from ..devices.device import Device
from .abstract_smart_home_hub import AbstractSmartHomeHub
from ..devices.air_purifier import AirPurifier, dict_to_air_purifier
from ..devices.light import Light, dict_to_light
from ..devices.blinds import Blind, dict_to_blind
from ..devices.controller import Controller, dict_to_controller
from ..devices.outlet import Outlet, dict_to_outlet
from ..devices.environment_sensor import EnvironmentSensor, dict_to_environment_sensor
from ..devices.motion_sensor import MotionSensor, dict_to_motion_sensor
from ..devices.open_close_sensor import OpenCloseSensor, dict_to_open_close_sensor
from ..devices.scene import Action, Info, Scene, SceneType, Trigger, dict_to_scene
from ..devices.water_sensor import WaterSensor, dict_to_water_sensor
from ..devices.occupancy_sensor import OccupancySensor, dict_to_occupancy_sensor
from ..devices.light_sensor import LightSensor, dict_to_light_sensor

urllib3.disable_warnings(category=InsecureRequestWarning)


class Hub(AbstractSmartHomeHub):
    def __init__(
        self,
        token: str,
        ip_address: str,
        port: str = "8443",
        api_version: str = "v1",
    ) -> None:
        """
        Initializes a new instance of the Hub class.

        Args:
            token (str): The authentication token for the hub.
            ip_address (str): The IP address of the hub.
            port (str, optional): The port number for the hub API. Defaults to "8443".
            api_version (str, optional): The version of the API to use. Defaults to "v1".
        """
        self.api_base_url = f"https://{ip_address}:{port}/{api_version}"
        self.websocket_base_url = f"wss://{ip_address}:{port}/{api_version}"
        self.token = token
        self.wsapp: Any = None

    def headers(self) -> Dict[str, Any]:
        return {"Authorization": f"Bearer {self.token}"}

    def create_event_listener(
        self,
        on_open: Any = None,
        on_message: Any = None,
        on_error: Any = None,
        on_close: Any = None,
        on_ping: Any = None,
        on_pong: Any = None,
        on_data: Any = None,
        on_cont_message: Any = None,
        ping_intervall: int = 60,
    ) -> None:
        """
        Create an event listener.

        Args:
            on_open (Any, optional)
            on_message (Any, optional)
            on_error (Any, optional)
            on_close (Any, optional)
            on_ping (Any, optional)
            on_pong (Any, optional)
            on_data (Any, optional)
            on_cont_message (Any, optional)
            ping_intervall (int, optional): Ping interval in Seconds. Defaults to 60.
        """
        self.wsapp = websocket.WebSocketApp(
            self.websocket_base_url,
            header={"Authorization": f"Bearer {self.token}"},
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_ping=on_ping,
            on_pong=on_pong,
            on_data=on_data,
            on_cont_message=on_cont_message,
        )

        self.wsapp.run_forever(
            sslopt={"cert_reqs": ssl.CERT_NONE}, ping_interval=ping_intervall
        )

    def stop_event_listener(self) -> None:
        if self.wsapp is not None:
            self.wsapp.close()
            self.wsapp = None

    def patch(self, route: str, data: List[Dict[str, Any]]) -> Any:
        response = requests.patch(
            f"{self.api_base_url}{route}",
            headers=self.headers(),
            json=data,
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        return response.text

    def get(self, route: str) -> Any:
        response = requests.get(
            f"{self.api_base_url}{route}",
            headers=self.headers(),
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        return response.json()

    def post(self, route: str, data: Optional[Dict[str, Any]] = None) -> Any:
        response = requests.post(
            f"{self.api_base_url}{route}",
            headers=self.headers(),
            json=data,
            timeout=10,
            verify=False,
        )
        if not response.ok:
            print(response.text)
        response.raise_for_status()

        if len(response.content) == 0:
            return None

        return response.json()

    def delete(self, route: str, data: Optional[Dict[str, Any]] = None) -> Any:
        response = requests.delete(
            f"{self.api_base_url}{route}",
            headers=self.headers(),
            json=data,
            timeout=10,
            verify=False,
        )
        response.raise_for_status()

        if len(response.content) == 0:
            return None

        return response.json()

    def _get_device_data_by_id(self, id_: str) -> Dict:
        """
        Fetches device data by its id
        """
        try:
            return self.get("/devices/" + id_)
        except HTTPError as err:
            if err.response is not None and err.response.status_code == 404:
                raise ValueError("Device id not found") from err
            raise err

    def get_air_purifiers(self) -> List[AirPurifier]:
        """
        Fetches all air purifiers registered in the Hub
        """
        devices = self.get("/devices")
        airpurifiers = list(filter(lambda x: x["type"] == "airPurifier", devices))
        return [dict_to_air_purifier(air_p, self) for air_p in airpurifiers]

    def get_air_purifier_by_id(self, id_: str) -> AirPurifier:
        air_purifier_device = self._get_device_data_by_id(id_)
        if air_purifier_device["deviceType"] != "airPurifier":
            raise ValueError("Device is not an Air Purifier")
        return dict_to_air_purifier(air_purifier_device, self)

    def get_lights(self) -> List[Light]:
        """
        Fetches all lights registered in the Hub
        """
        devices = self.get("/devices")
        lights = list(filter(lambda x: x["type"] == "light", devices))
        return [dict_to_light(light, self) for light in lights]

    def get_light_by_name(self, lamp_name: str) -> Light:
        """
        Fetches all lights and returns first result that matches this name
        """
        lights = self.get_lights()
        lights = list(filter(lambda x: x.attributes.custom_name == lamp_name, lights))
        if len(lights) == 0:
            raise AssertionError(f"No light found with name {lamp_name}")
        return lights[0]

    def get_light_by_id(self, id_: str) -> Light:
        """
        Fetches a light by its id if that light does not exist or is a device of another type raises ValueError
        """
        light = self._get_device_data_by_id(id_)
        if light["type"] != "light":
            raise ValueError("Device is not a light")
        return dict_to_light(light, self)

    def get_outlets(self) -> List[Outlet]:
        """
        Fetches all outlets registered in the Hub
        """
        devices = self.get("/devices")
        outlets = list(filter(lambda x: x["type"] == "outlet", devices))
        return [dict_to_outlet(outlet, self) for outlet in outlets]

    def get_outlet_by_name(self, outlet_name: str) -> Outlet:
        """
        Fetches all outlets and returns first result that matches this name
        """
        outlets = self.get_outlets()
        outlets = list(
            filter(lambda x: x.attributes.custom_name == outlet_name, outlets)
        )
        if len(outlets) == 0:
            raise AssertionError(f"No outlet found with name {outlet_name}")
        return outlets[0]

    def get_outlet_by_id(self, id_: str) -> Outlet:
        """
        Fetches an outlet by its id if that outlet does not exist or is a device of another type raises ValueError
        """
        outlet = self._get_device_data_by_id(id_)
        if outlet["type"] != "outlet":
            raise ValueError("Device is not an outlet")
        return dict_to_outlet(outlet, self)

    def get_environment_sensors(self) -> List[EnvironmentSensor]:
        """
        Fetches all environment sensors registered in the Hub
        """
        devices = self.get("/devices")
        sensors = list(
            filter(lambda x: x["deviceType"] == "environmentSensor", devices)
        )
        return [dict_to_environment_sensor(sensor, self) for sensor in sensors]

    def get_environment_sensor_by_id(self, id_: str) -> EnvironmentSensor:
        environment_sensor = self._get_device_data_by_id(id_)
        if environment_sensor["deviceType"] != "environmentSensor":
            raise ValueError("Device is not an EnvironmentSensor")
        return dict_to_environment_sensor(environment_sensor, self)

    def get_motion_sensors(self) -> List[MotionSensor]:
        """
        Fetches all motion sensors registered in the Hub
        """
        devices = self.get("/devices")
        sensors = list(filter(lambda x: x["deviceType"] == "motionSensor", devices))
        return [dict_to_motion_sensor(sensor, self) for sensor in sensors]

    def get_motion_sensor_by_name(self, motion_sensor_name: str) -> MotionSensor:
        """
        Fetches all motion sensors and returns first result that matches this name
        """
        motion_sensors = self.get_motion_sensors()
        motion_sensors = list(filter(lambda x: x.attributes.custom_name == motion_sensor_name, motion_sensors))
        if len(motion_sensors) == 0:
            raise AssertionError(f"No motion sensor found with name {motion_sensor_name}")
        return motion_sensors[0]

    def get_motion_sensor_by_id(self, id_: str) -> MotionSensor:
        motion_sensor = self._get_device_data_by_id(id_)
        if motion_sensor["deviceType"] != "motionSensor":
            raise ValueError("Device is not an MotionSensor")
        return dict_to_motion_sensor(motion_sensor, self)

    def get_open_close_sensors(self) -> List[OpenCloseSensor]:
        """
        Fetches all open/close sensors registered in the Hub
        """
        devices = self.get("/devices")
        sensors = list(filter(lambda x: x["deviceType"] == "openCloseSensor", devices))
        return [dict_to_open_close_sensor(sensor, self) for sensor in sensors]

    def get_open_close_by_id(self, id_: str) -> OpenCloseSensor:
        open_close_sensor = self._get_device_data_by_id(id_)
        if open_close_sensor["deviceType"] != "openCloseSensor":
            raise ValueError("Device is not an OpenCloseSensor")
        return dict_to_open_close_sensor(open_close_sensor, self)

    def get_blinds(self) -> List[Blind]:
        """
        Fetches all blinds registered in the Hub
        """
        devices = self.get("/devices")
        blinds = list(filter(lambda x: x["type"] == "blinds", devices))
        return [dict_to_blind(blind, self) for blind in blinds]

    def get_blind_by_name(self, blind_name: str) -> Blind:
        """
        Fetches all blinds and returns first result that matches this name
        """
        blinds = self.get_blinds()
        blinds = list(filter(lambda x: x.attributes.custom_name == blind_name, blinds))
        if len(blinds) == 0:
            raise AssertionError(f"No blind found with name {blind_name}")
        return blinds[0]

    def get_blinds_by_id(self, id_: str) -> Blind:
        blind_sensor = self._get_device_data_by_id(id_)
        if blind_sensor["deviceType"] != "blinds":
            raise ValueError("Device is not a Blind")
        return dict_to_blind(blind_sensor, self)

    def get_controllers(self) -> List[Controller]:
        """
        Fetches all controllers registered in the Hub
        """
        devices = self.get("/devices")
        controllers = list(filter(lambda x: x["type"] == "controller", devices))
        return [dict_to_controller(controller, self) for controller in controllers]

    def get_controller_by_name(self, controller_name: str) -> Controller:
        """
        Fetches all controllers and returns first result that matches this name
        """
        controllers = self.get_controllers()
        controllers = list(
            filter(lambda x: x.attributes.custom_name == controller_name, controllers)
        )
        if len(controllers) == 0:
            raise AssertionError(f"No controller found with name {controller_name}")
        return controllers[0]

    def get_controller_by_id(self, id_: str) -> Controller:
        """
        Fetches a controller by its id
        if that controller does not exist or is a device of another type raises ValueError
        """
        controller = self._get_device_data_by_id(id_)
        if controller["type"] != "controller":
            raise ValueError("Device is not a controller")
        return dict_to_controller(controller, self)

    def get_scenes(self) -> List[Scene]:
        """
        Fetches all scenes
        """
        scenes: List = self.get("/scenes")
        return [dict_to_scene(scene, self) for scene in scenes]

    def get_scene_by_id(self, scene_id: str) -> Scene:
        """
        Fetches a specific scene by a given id
        """
        data = self.get(f"/scenes/{scene_id}")
        return dict_to_scene(data, self)

    def get_scene_by_name(self, scene_name: str) -> Scene:
        """
        Fetches all scenes and returns the first result that matches scene_name
        """
        scenes = self.get_scenes()
        scenes = list(filter(lambda x: x.info.name == scene_name, scenes))
        if len(scenes) == 0:
            raise AssertionError(f"No Scene found with name {scene_name}")
        return scenes[0]

    def get_water_sensors(self) -> List[WaterSensor]:
        """
        Fetches all water sensors registered in the Hub
        """
        devices = self.get("/devices")
        water_sensors = list(
            filter(lambda x: x["deviceType"] == "waterSensor", devices)
        )
        return [
            dict_to_water_sensor(water_sensor, self) for water_sensor in water_sensors
        ]

    def get_water_sensor_by_id(self, id_: str) -> WaterSensor:
        """
        Fetches a water sensor by its id
        if that water sensors does not exist or is a device of another type raises ValueError
        """
        water_sensor = self._get_device_data_by_id(id_)
        if water_sensor["deviceType"] != "waterSensor":
            raise ValueError("Device is not a WaterSensor")
        return dict_to_water_sensor(water_sensor, self)

    def get_light_sensors(self) -> List[LightSensor]:
        """
        Fetches all light sensors registered in the Hub
        """
        devices = self.get("/devices")
        sensors = list(filter(lambda x: x["deviceType"] == "lightSensor", devices))
        return [dict_to_light_sensor(sensor, self) for sensor in sensors]

    def get_light_sensor_by_id(self, id_: str) -> LightSensor:
        """
        Fetches a light sensor by its id
        if that light sensor does not exist or is a device of another type raises ValueError
        """
        sensor = self._get_device_data_by_id(id_)
        if sensor["deviceType"] != "lightSensor":
            raise ValueError("Device is not a LightSensor")
        return dict_to_light_sensor(sensor, self)

    def get_occupancy_sensors(self) -> List[OccupancySensor]:
        """
        Fetches all occupancy sensors registered in the Hub
        """
        devices = self.get("/devices")
        sensors = list(filter(lambda x: x["deviceType"] == "occupancySensor", devices))
        return [dict_to_occupancy_sensor(sensor, self) for sensor in sensors]

    def get_occupancy_sensor_by_id(self, id_: str) -> OccupancySensor:
        """
        Fetches an occupancy sensor by its id
        if that occupancy sensor does not exist or is a device of another type raises ValueError
        """
        sensor = self._get_device_data_by_id(id_)
        if sensor["deviceType"] != "occupancySensor":
            raise ValueError("Device is not an OccupancySensor")
        return dict_to_occupancy_sensor(sensor, self)

    def get_all_devices(self) -> List[Device]:
        """
        Fetches all devices registered in the Hub
        """
        devices: List[Device] = []
        devices.extend(self.get_air_purifiers())
        devices.extend(self.get_blinds())
        devices.extend(self.get_controllers())
        devices.extend(self.get_environment_sensors())
        devices.extend(self.get_lights())
        devices.extend(self.get_motion_sensors())
        devices.extend(self.get_open_close_sensors())
        devices.extend(self.get_outlets())
        devices.extend(self.get_water_sensors())
        devices.extend(self.get_occupancy_sensors())
        devices.extend(self.get_light_sensors())

        return devices

    def create_scene(
        self,
        info: Info,
        scene_type: SceneType = SceneType.USER_SCENE,
        triggers: Optional[List[Trigger]] = None,
        actions: Optional[List[Action]] = None,
    ) -> Scene:
        """Creates a new scene.

        Note:
        To create an empty scene leave actions and triggers None.

        Args:
            info (Info): Name & Icon
            type (SceneType): typically USER_SCENE
            triggers (List[Trigger]): Triggers for the Scene (An app trigger will be created automatically)
            actions (List[Action]): Actions that will be run on Trigger

        Returns:
            Scene: Returns the newly created scene.
        """
        trigger_list = []
        if triggers:
            trigger_list = [
                x.model_dump(mode="json", exclude_none=True) for x in triggers
            ]

        action_list = []
        if actions:
            action_list = [
                x.model_dump(mode="json", exclude_none=True) for x in actions
            ]
        data = {
            "info": info.model_dump(mode="json", exclude_none=True),
            "type": scene_type.value,
            "triggers": trigger_list,
            "actions": action_list,
        }
        data = camelize_dict(data)  # type: ignore
        response_dict = self.post(
            "/scenes/",
            data=data,
        )
        scene_id = response_dict["id"]
        return self.get_scene_by_id(scene_id)

    def delete_scene(self, scene_id: str) -> None:
        self.delete(
            f"/scenes/{scene_id}",
        )
