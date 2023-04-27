import ssl
from typing import Any, Dict, List, Optional
import requests
import websocket
from urllib3.exceptions import InsecureRequestWarning

from .room import Color, Room, dict_to_room
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

    def post(self, route: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            f"{self.api_base_url}{route}",
            headers=self.headers(),
            json=data,
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        return response.json()

    def delete(self, route: str, data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        response = requests.delete(
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

    def get_environment_sensors(self) -> List[EnvironmentSensor]:
        """
        Fetches all environment sensors registered in the Hub
        """
        devices = self.get("/devices")
        sensors = list(
            filter(lambda x: x["deviceType"] == "environmentSensor", devices)
        )
        return [dict_to_environment_sensor(sensor, self) for sensor in sensors]

    def get_rooms(self) -> List[Room]:
        """
        Fetches all rooms registered in the Hub
        """
        rooms = self.get("/rooms")

        return [dict_to_room(room) for room in rooms]

    def create_room(self, name: str, color: Color, icon: str) -> Room:
        """
        Creates a new room with a given name, color and icon.
        """
        data = self.post("/rooms", data={"name": name, "color": color, "icon": icon})
        print(data["id"])
        room_id = data["id"]
        return Room(room_id=room_id, name=name, color=color, icon=icon)

    def delete_room(self, room: Room) -> None:
        """
        Deletes a room.
        """
        self.delete(f"/rooms/{room.room_id}", data=None)
