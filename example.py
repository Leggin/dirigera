import time
from hub.dirigera_hub import DirigeraHub
import config

dirigera_hub = DirigeraHub(
    token=config.DIRIGERA_TOKEN, base_url=config.DIRIGERA_IP_ADDRESS
)
lights = dirigera_hub.get_lights()
print("All lamps you have:")
for light in lights:
    print(light.custom_name)


kitchen_light = dirigera_hub.get_light_by_name("Kitchen light")
kitchen_light.set_light(True)
kitchen_light.set_light_level(50)
time.sleep(1)
kitchen_light.set_color_temperature(2222)
time.sleep(1)
kitchen_light.set_light(False)
