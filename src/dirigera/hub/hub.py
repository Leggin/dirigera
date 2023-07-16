import ssl
from typing import Any, Dict, List
import requests
import websocket
from urllib3.exceptions import InsecureRequestWarning

from .abstract_smart_home_hub import AbstractSmartHomeHub
from ..devices.light import Light, dict_to_light
from ..devices.blinds import Blind, dict_to_blind
from ..devices.controller import Controller, dict_to_controller
from ..devices.outlet import Outlet, dict_to_outlet
from ..devices.environment_sensor import EnvironmentSensor, dict_to_environment_sensor
from ..devices.open_close_sensor import OpenCloseSensor, dict_to_open_close_sensor
from ..devices.motion_sensor import MotionSensor, dict_to_motion_sensor

requests.packages.urllib3.disable_warnings(  # pylint: disable=no-member
    category=InsecureRequestWarning
)


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

    def headers(self):
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
    ):
        wsapp = websocket.WebSocketApp(
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

        wsapp.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def patch(self, route: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.patch(
            f"{self.api_base_url}{route}",
            headers=self.headers(),
            json=data,
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        return response.text

    def get(self, route: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.api_base_url}{route}",
            headers=self.headers(),
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        return response.json()

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
        lights = list(filter(lambda x: x.custom_name == lamp_name, lights))
        if len(lights) == 0:
            raise AssertionError(f"No light found with name {lamp_name}")
        return lights[0]

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
        outlets = list(filter(lambda x: x.custom_name == outlet_name, outlets))
        if len(outlets) == 0:
            raise AssertionError(f"No outlet found with name {outlet_name}")
        return outlets[0]

    def get_environment_sensors(self) -> List[EnvironmentSensor]:
        """
        Fetches all environment sensors registered in the Hub
        """
        devices = self.get("/devices")
        sensors = list(
            filter(lambda x: x["deviceType"] == "environmentSensor", devices)
        )
        return [dict_to_environment_sensor(sensor, self) for sensor in sensors]

    def get_open_close_sensors(self) -> List[OpenCloseSensor]:
        """
        Fetches all open/close sensors registered in the Hub
        """
        devices = self.get("/devices")
        sensors = list(
            filter(lambda x: x["deviceType"] == "openCloseSensor", devices)
        )
        return [dict_to_open_close_sensor(sensor, self) for sensor in sensors]

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
        blinds = list(filter(lambda x: x.custom_name == blind_name, blinds))
        if len(blinds) == 0:
            raise AssertionError(f"No blind found with name {blind_name}")
        return blinds[0]

    def get_controllers(self) -> List[Controller]:
        """
        Fetches all controllers registered in the Hub
        """
        devices = self.get("/devices")
        controllers = list(
            filter(lambda x: x["type"] == "controller", devices)
        )
        return [
            dict_to_controller(controller, self) for controller in controllers
        ]

    def get_controller_by_name(self, controller_name: str) -> Controller:
        """
        Fetches all controllers and returns first result that matches this name
        """
        controllers = self.get_controllers()
        controllers = list(
            filter(lambda x: x.custom_name == controller_name, controllers)
        )
        if len(controllers) == 0:
            raise AssertionError(f"No controller found with name {controller_name}")
        return controllers[0]

    def get_motion_sensors(self) -> List[MotionSensor]:
        """
        Fetches all motion sensors registered in the hub
        """
        devices = self.get("/devices")
        sensors = list(
            filter(lambda x: x["deviceType"] == "motionSensor", devices)
        )
        return [dict_to_motion_sensor(sensor, self) for sensor in sensors]
