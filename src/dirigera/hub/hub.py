import ssl
from typing import Any
import requests
import websocket
from urllib3.exceptions import InsecureRequestWarning

from .abstract_smart_home_hub import AbstractSmartHomeHub
from ..devices.light import Light, dict_to_light
from ..devices.environment_sensor import EnvironmentSensor, dict_to_environment_sensor

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
        on_open: Any | None = None,
        on_message: Any | None = None,
        on_error: Any | None = None,
        on_close: Any | None = None,
        on_ping: Any | None = None,
        on_pong: Any | None = None,
        on_data: Any | None = None,
        on_cont_message: Any | None = None,
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

    def patch(self, route: str, data: dict[str, Any]) -> dict[str, Any]:
        response = requests.patch(
            f"{self.api_base_url}{route}",
            headers=self.headers(),
            json=data,
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        return response.text

    def get(self, route: str) -> dict[str, Any]:
        response = requests.get(
            f"{self.api_base_url}{route}",
            headers=self.headers(),
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        return response.json()

    def get_lights(self) -> list[Light]:
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

    def get_environment_sensors(self) -> list[EnvironmentSensor]:
        """
        Fetches all environment sensors registered in the Hub
        """
        devices = self.get("/devices")
        sensors = list(
            filter(lambda x: x["deviceType"] == "environmentSensor", devices)
        )
        return [dict_to_environment_sensor(sensor, self) for sensor in sensors]
