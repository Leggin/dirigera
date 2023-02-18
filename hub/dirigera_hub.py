from typing import Any, Dict, List
import requests
from urllib3.exceptions import InsecureRequestWarning

from hub.abstract_smart_home_hub import AbstractSmartHomeHub
from devices.light import dict_to_light
from devices.light import Light
import config

requests.packages.urllib3.disable_warnings(  # pylint: disable=no-member
    category=InsecureRequestWarning
)


class DirigeraHub(AbstractSmartHomeHub):
    def __init__(
        self,
        token: str,
        base_url: str,
        port: str = config.DIRIGERA_PORT,
        api_version: str = config.DIRIGERA_API_VERSION,
    ) -> None:
        self.base_url = f"https://{base_url}:{port}/{api_version}"
        self.token = token

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def patch(self, route: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.patch(
            f"{self.base_url}{route}",
            headers=self.headers(),
            json=data,
            timeout=10,
            verify=False,
        )
        response.raise_for_status()
        return response.text

    def get(self, route: str) -> Dict[str, Any]:
        response = requests.get(
            f"{self.base_url}{route}", headers=self.headers(), timeout=10, verify=False
        )
        response.raise_for_status()
        return response.json()

    def get_lights(self) -> List[Light]:
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
