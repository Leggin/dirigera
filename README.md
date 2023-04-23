# Dirigera Python Client
![Test](https://github.com/Leggin/dirigera/actions/workflows/tests.yml/badge.svg)
![Pypi](https://img.shields.io/pypi/v/dirigera)
[![Downloads](https://static.pepy.tech/badge/dirigera/month)](https://pepy.tech/project/dirigera)


This repository provides an unofficial Python client for controlling the IKEA Dirigera Smart Home Hub. Current features:
 - [light control](#controlling-lights)
 - [environment sensor](#environment-sensor) (tested with VINDSTYRKA)
 - [event listener](#event-listener) for hub events

Support for other features will be added in the future and your input in form of issues and PRs is greatly appreciated.

## Installation

```bash
pip install dirigera
```

## Quickstart

1. Find out the ip-address of your Dirigera (check your router)
2. Run the generate-token script:
   ```bash
   generate-token <Dirigera ip-address>
   ```
   When prompted, you must push the action button on Dirigera. After that hit ENTER and your `token` will be printed to the console.  
   Example:
   ```
    Press the action button on Dirigera then hit ENTER ...
    Your Token:
    mgwB.aXqwpzV89N0aUwBhZMJjD8a.UBPyzy2InGtqgwo2MO5.xX4ug7.uBcVJquwYzLnAijF7SdYKvNxTo0uzQKahV10A-3ZQOz-UAubGP6sHWt1CJx3QmWZyE7ZcMZKgODXjSzWL1lumKgGz5dUIwFi3rhNxgK-IsBGeGVhNXPt8vGrYEcZePwPvNAIg8RqmlH27L-JZPnkAtP2wHoOdW72Djot3yJsohtEsb0p9mJvoZFSavTlTr4LDuf584vuH5fha5xoR9QhhIvvgbAP-s4EHFqENNi6vrYLHKR.sdqnv4sYw6UH-l6oiPnnRLxinoqBPOlWhlcL9doFviXQE.tZ9X8WVqyBrd0NYHlo9iorEvUbnZuD02BEJrg4NLwgh3rZtyF0Mi46HenynzBohbPn4RnuSYYCiHt5EZnWedxBtDqc7mSTm1ZtyD
   ```
6. Done

## [Dirigera Hub](./src/dirigera/hub/hub.py)

Setting up the client works by providing the token and ip address.

```python
import dirigera

dirigera_hub = dirigera.Hub(
    token="mgwB.aXqwpzV89N0aUwBhZMJjD8a...",
    ip_address="192.1..."
)
```

## [Controlling Lights](./src/dirigera/devices/light.py)

To get information about the available lights, you can use the `get_lights()` method:

```python
lights = dirigera_hub.get_lights()
```

The light object has the following attributes:

```python
device_id: str
is_reachable: bool
custom_name: str
is_on: bool
startup_on_off: StartupEnum | None
light_level: int | None  # not all lights have a light level
color_temp: int | None  # not all lights have a color temperature
color_temp_min: int | None
color_temp_max: int | None
color_hue: int | None  # not all lights have a color hue
color_saturation: float | None  # not all lights have a color saturation
room_id: str
room_name: str
can_receive: List[str]  # list of all available commands ["customName", "isOn", "lightLevel", ...]
```

Available methods for light are:

```python
light.set_name(name="kitchen light 1")

light.set_light(lamp_on=True)

light.set_light_level(light_level=90)

light.set_color_temperature(color_temp=3000)

light.set_light_color(hue=128, saturation=0.5)

light.set_startup_behaviour(behaviour=StartupEnum.START_OFF)
```

## [Environment Sensor](./src/dirigera/devices/environment_sensor.py)
Currently only tested with the VINDSTYRKA sensor. If you have other sensors please send me the json and I will add support or create a PR.


To get the environment sensors use:
```python
sensors = dirigera_hub.get_environment_sensors()
```

The environment sensor object has the following attributes:
```python
device_id: str
is_reachable: bool
custom_name: str
current_temperature: str
current_rh: int  # current humidity
current_pm25: int  # current particulate matter 2.5
max_measured_pm25: int  # maximum measurable particulate matter 2.5
min_measured_pm25: int  # minimum measurable particulate matter 2.5
voc_index: int  # current volatile organic compound
room_id: str
room_name: str
can_receive: list[str]  # list of all available commands ["customName"]
```


## Event Listener
The event listener allows you to listen to events that are published by your Dirigera hub. This is useful if you want to automate tasks based on events such as when a light is turned on or off, or when the color temperature of a light is changed.

```python
import json
from typing import Any


def on_message(ws: Any, message: str):
    message_dict = json.loads(message)
    data = message_dict["data"]
    if data["id"] == bed_light.light_id:
        print(f"{message_dict['type']} event on {bed_light.custom_name}, attributes: {data['attributes']}")

def on_error(ws: Any, message: str):
    print(message)

dirigera_hub.create_event_listener(
    on_message=on_message, on_error=on_error
)
```
```
deviceStateChanged event on Bed Light, attributes: {'isOn': False}
```

## Motivation
The primary motivation for this project was to provide users with the ability to control the startup behavior of their smart home lamps when there is a power outage.  
The default behavior of the hub is to turn on all lights when power is restored, which can be problematic if the user is away from home or on vacation, and a small power fluctuation causes all lights to turn on and stay on. Unfortunately, the IKEA app does not offer a way to change this default behavior.  
The `set_startup_behaviour()` function enables users to override the default behavior and choose the startup behavior that best suits their needs (START_ON = turn on light when power is back, START_OFF = light stays off when power is back).  
I can not guarantee that all IKEA lamps offer this functionality.

## Contributing

Contributions are welcome! If you have an idea for a new feature or a bug fix, please post and issue or submit a pull request.

## License

The MIT License (MIT)

Copyright (c) 2023 Leggin