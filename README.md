# Dirigera Python Client

![Test](https://github.com/Leggin/dirigera/actions/workflows/tests.yml/badge.svg)
![Pypi](https://img.shields.io/pypi/v/dirigera)
[![Downloads](https://static.pepy.tech/badge/dirigera/month)](https://pepy.tech/project/dirigera)
![Downloads](https://img.shields.io/pypi/pyversions/dirigera)

This repository provides an unofficial Python client for controlling the IKEA Dirigera Smart Home Hub. Current features:

- [light control](#controlling-lights)
- [outlet control](#controlling-outlets)
- [blinds control](#controlling-blinds)
- [remote controllers](#remote-controllers) (tested with STYRBAR)
- [environment sensor](#environment-sensor) (tested with VINDSTYRKA)
- [scene](#scene)
- [event listener](#event-listener) for hub events

Support for other features will be added in the future and your input in form of issues and PRs is greatly appreciated.

## Installation

```bash
pip install dirigera
```

## Quickstart

1. Find out the ip-address of your Dirigera (check your router)
2. Once you installed `dirigera` with pip you can run the included generate-token script. Here you can directly set the ip-address of you dirigera as parameter.
   ```bash
   generate-token <Dirigera ip-address>
   ```
3. The script starts the auth process. When prompted, you must push the action button on the bottom of your Dirigera.
4. After that hit ENTER and your `token` will be printed to the console.  
   Example:
   ```
   Press the action button on Dirigera then hit ENTER ...
   Your Token:
   mgwB.aXqwpzV89N0aUwBhZMJjD8a.UBPyzy2InGtqgwo2MO5.xX4ug7.uBcVJquwYzLnAijF7SdYKvNxTo0uzQKahV10A-3ZQOz-UAubGP6sHWt1CJx3QmWZyE7ZcMZKgODXjSzWL1lumKgGz5dUIwFi3rhNxgK-IsBGeGVhNXPt8vGrYEcZePwPvNAIg8RqmlH27L-JZPnkAtP2wHoOdW72Djot3yJsohtEsb0p9mJvoZFSavTlTr4LDuf584vuH5fha5xoR9QhhIvvgbAP-s4EHFqENNi6vrYLHKR.sdqnv4sYw6UH-l6oiPnnRLxinoqBPOlWhlcL9doFviXQE.tZ9X8WVqyBrd0NYHlo9iorEvUbnZuD02BEJrg4NLwgh3rZtyF0Mi46HenynzBohbPn4RnuSYYCiHt5EZnWedxBtDqc7mSTm1ZtyD
   ```
5. Done. Use this token in the hub setup.
   ```
   dirigera.Hub(
      token="mgwB.aXqwpzV89N0aUwBhZMJjD8a...",
      ip_address="192.1..."
   )
   ```

## [Dirigera Hub](./src/dirigera/hub/hub.py)

Setting up the client works by providing the token and ip address.

```python
import dirigera

dirigera_hub = dirigera.Hub(
    token="mgwB.aXqwpzV89N0aUwBhZMJjD8a...",
    ip_address="192.1..."
)
```

# [Devices](./src/dirigera/devices/device.py)

All available devices (Light, Controller, Outlet, ...) consist of the core data defined in [device.py](./src/dirigera/devices/device.py):

### Core Device Data

```python
id: str
type: str
device_type: str
created_at: datetime.datetime
is_reachable: bool
last_seen: datetime.datetime
attributes: Attributes
capabilities: Capabilities
room: Room
device_set: List
remote_links: List[str]
is_hidden: Optional[bool] = None
```

### Attributes

All devices have attributes. Some devices have special attributes (for example Light has `is_on``). These are the core attributes each device has:

```python
custom_name: str
model: str
manufacturer: str
firmware_version: str
hardware_version: str
serial_number: Optional[str] = None
product_code: Optional[str] = None
ota_status: Optional[str] = None
ota_state: Optional[str] = None
ota_progress: Optional[int] = None
ota_policy: Optional[str] = None
ota_schedule_start: Optional[datetime.time] = None
ota_schedule_end: Optional[datetime.time] = None
```

### Capabilities

All devices have capabilities (for some it is just empty lists). Capabilities desrcibe what send/receive actions can be performed:

```python
can_send: List[str]
can_receive: List[str]
```

All devices have a room with the corresponging infos.

### Room

```python
id: str
name: str
color: str
icon: str
```

## [Controlling Lights](./src/dirigera/devices/light.py)

To get information about the available lights, you can use the `get_lights()` method:

```python
lights = dirigera_hub.get_lights()
```

The light object has the following attributes (additional to the core attributes):

```python
startup_on_off: Optional[StartupEnum] = None # Optional attributes are not present on all lights
is_on: bool
light_level: Optional[int] = None
color_temperature: Optional[int] = None
color_temperature_min: Optional[int] = None
color_temperature_max: Optional[int] = None
color_hue: Optional[int] = None
color_saturation: Optional[float] = None
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

## [Controlling Outlets](./src/dirigera/devices/outlet.py)

To get information about the available outlets, you can use the `get_outlets()` method:

```python
outlets = dirigera_hub.get_outlets()
```

The outlet object has the following attributes (additional to the core attributes):

```python
is_on: bool
startup_on_off: Optional[StartupEnum]
```

Available methods for outlet are:

```python
outlet.set_name(name="kitchen socket 1")

outlet.set_on(outlet_on=True)

outlet.set_startup_behaviour(behaviour=StartupEnum.START_OFF)
```

## [Controlling Blinds](./src/dirigera/devices/blinds.py)

To get information about the available blinds, you can use the `get_blinds()` method:

```python
blinds = dirigera_hub.get_blinds()
```

The blind object has the following attributes (additional to the core attributes):

```python
blinds_current_level: Optional[int] = None
blinds_target_level: Optional[int] = None
blinds_state: Optional[str] = None
```

Available methods for blinds are:

```python
blind.set_name(name="kitchen blind 1")

blind.set_target_level(target_level=90)
```

## [Remote Controllers](./src/dirigera/devices/controller.py)

Currently only tested with the STYRBAR remote.

To get information about the available controllers, you can use the `get_controllers()` method:

```python
controllers = dirigera_hub.get_controllers()
```

The controller object has the following attributes (additional to the core attributes):

```python
is_on: bool
battery_percentage: Optional[int] = None
```

Available methods for controller are:

```python
controller.set_name(name="kitchen remote 1")
```

## [Environment Sensor](./src/dirigera/devices/environment_sensor.py)

Currently only tested with the VINDSTYRKA sensor. If you have other sensors please send me the json and I will add support or create a PR.

To get the environment sensors use:

```python
sensors = dirigera_hub.get_environment_sensors()
```

The environment sensor object has the following attributes (additional to the core attributes):

```python
current_temperature: int
current_r_h: int # current humidity
current_p_m25: int # current particulate matter 2.5
max_measured_p_m25: int # maximum measurable particulate matter 2.5
min_measured_p_m25: int # minimum measurable particulate matter 2.5
voc_index: int # current volatile organic compound
```

# [Scene](./src/dirigera/devices/scene.py)

To get the scenes use:

```python
scenes = dirigera_hub.get_scenes()
```

The scene object has the following attributes:

```python
id: str
type: str
info: Info
triggers: List[Trigger]
actions: List[Action]
created_at: datetime.datetime
last_completed: datetime.datetime
last_triggered: datetime.datetime
last_undo: datetime.datetime
commands: List[str]
undo_allowed_duration: int
```

Details to the Trigger, Action and Info class can be found in [scene.py](./src/dirigera/devices/scene.py)

Available methods for scene are:

```python
scene.trigger()
scene.undo()
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

### Setup of dev

For setting up the dev environment I recommend running the `setup.sh` script, which will create a venv and install the `requirements.txt` as well as the `dev-requirements.txt`.

### Tests

To run the tests execute the `run-test.sh` script or just run `pytest .`  
For linting you can run the `run-pylint.sh`.  
For types you can run the `run-mypy.sh`  
To test the different python versions you can use the `run-python-verions-test.sh` (this requires a running docker installation).  
All of these tests are also run when a PR is openend (and the test run is triggered).

## License

The MIT License (MIT)

Copyright (c) 2023 Leggin
