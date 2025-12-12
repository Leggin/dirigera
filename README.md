# Dirigera Python Client

![Test](https://github.com/Leggin/dirigera/actions/workflows/tests.yml/badge.svg)
![Pypi](https://img.shields.io/pypi/v/dirigera)
[![Downloads](https://static.pepy.tech/badge/dirigera/month)](https://pepy.tech/project/dirigera)
![Downloads](https://img.shields.io/pypi/pyversions/dirigera)

This repository provides an unofficial Python client for controlling the IKEA Dirigera Smart Home Hub. Current features:

- [light control](#controlling-lights)
- [outlet control](#controlling-outlets)
- [air purifier control](#controlling-air-purifier)
- [blinds control](#controlling-blinds)
- [remote controllers](#remote-controllers) (tested with STYRBAR)
- [environment sensor](#environment-sensor) (tested with VINDSTYRKA)
- [light sensor](#light-sensor) (tested with MYGGSPRAY)
- [scene](#scene)
- [motion sensor](#motion-sensor)
- [occupancy sensor](#occupancy-sensor) (tested with MYGGSPRAY)
- [open/close sensor](#open-close-sensor)
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

<details>
  <summary>List dirigera_hub functions</summary>

```python
# Send a PATCH request to the hub
response = dirigera_hub.patch(route="/devices/1", data=[{"attributes": {"customName": "new name"}}])

# Send a GET request to the hub
response = dirigera_hub.get(route="/devices")

# Send a POST request to the hub
response = dirigera_hub.post(route="/scenes", data={"name": "new scene"})

# Send a DELETE request to the hub
response = dirigera_hub.delete(route="/scenes/1")

# Fetch all air purifiers registered in the hub
air_purifiers = dirigera_hub.get_air_purifiers()

# Fetch an air purifier by its ID
air_purifier = dirigera_hub.get_air_purifier_by_id(id_="1")

# Fetch all lights registered in the hub
lights = dirigera_hub.get_lights()

# Fetch a light by its name
light = dirigera_hub.get_light_by_name(lamp_name="kitchen light")

# Fetch a light by its ID
light = dirigera_hub.get_light_by_id(id_="1")

# Fetch all outlets registered in the hub
outlets = dirigera_hub.get_outlets()

# Fetch an outlet by its name
outlet = dirigera_hub.get_outlet_by_name(outlet_name="kitchen outlet")

# Fetch an outlet by its ID
outlet = dirigera_hub.get_outlet_by_id(id_="1")

# Fetch all environment sensors registered in the hub
sensors = dirigera_hub.get_environment_sensors()

# Fetch an environment sensor by its ID
sensor = dirigera_hub.get_environment_sensor_by_id(id_="1")

# Fetch all motion sensors registered in the hub
sensors = dirigera_hub.get_motion_sensors()

# Fetch a motion sensor by its name
light = dirigera_hub.get_motion_sensor_by_name(motion_sensor_name="kitchen motion sensor")

# Fetch a motion sensor by its ID
sensor = dirigera_hub.get_motion_sensor_by_id(id_="1")

# Fetch all open/close sensors registered in the hub
sensors = dirigera_hub.get_open_close_sensors()

# Fetch an open/close sensor by its ID
sensor = dirigera_hub.get_open_close_by_id(id_="1")

# Fetch all blinds registered in the hub
blinds = dirigera_hub.get_blinds()

# Fetch a blind by its name
blind = dirigera_hub.get_blind_by_name(blind_name="living room blind")

# Fetch a blind by its ID
blind = dirigera_hub.get_blinds_by_id(id_="1")

# Fetch all controllers registered in the hub
controllers = dirigera_hub.get_controllers()

# Fetch a controller by its name
controller = dirigera_hub.get_controller_by_name(controller_name="remote control")

# Fetch a controller by its ID
controller = dirigera_hub.get_controller_by_id(id_="1")

# Fetch all scenes
scenes = dirigera_hub.get_scenes()

# Fetch a scene by its ID
scene = dirigera_hub.get_scene_by_id(scene_id="1")

# Fetch all water sensors registered in the hub
water_sensors = dirigera_hub.get_water_sensors()

# Fetch a water sensor by its ID
water_sensor = dirigera_hub.get_water_sensor_by_id(id_="1")

# Fetch all occupancy sensors registered in the hub
occupancy_sensors = dirigera_hub.get_occupancy_sensors()

# Fetch an occupancy sensor by its ID
occupancy_sensor = dirigera_hub.get_occupancy_sensor_by_id(id_="1")

# Fetch all light sensors registered in the hub
light_sensors = dirigera_hub.get_light_sensors()

# Fetch a light sensor by its ID
light_sensor = dirigera_hub.get_light_sensor_by_id(id_="1")

# Fetch all devices registered in the hub
devices = dirigera_hub.get_all_devices()

# Create a new scene
scene = dirigera_hub.create_scene(
    info=Info(name="New Scene", icon=Icon.SCENES_BOOK),
    scene_type=SceneType.USER_SCENE,
    triggers=[],
    actions=[]
)

# Delete a scene by its ID
dirigera_hub.delete_scene(scene_id="1")
```

</details>

# [Devices](./src/dirigera/devices/device.py)

All available devices (Light, Controller, Outlet, ...) consist of the core data defined in [device.py](./src/dirigera/devices/device.py):

### Core Device Data

```python
id: str
relation_id: Optional[str] = None
type: str
device_type: str
created_at: datetime.datetime
is_reachable: bool
last_seen: datetime.datetime
attributes: Attributes
capabilities: Capabilities
room: Optional[Room] = None
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
# Reload the light data from the hub
light.reload()

# Set the name of the light
light.set_name(name="kitchen light 1")

# Turn the light on or off
light.set_light(lamp_on=True)

# Set the light level (1-100)
light.set_light_level(light_level=90)

# Set the color temperature
light.set_color_temperature(color_temp=3000)

# Set the light color using hue (0-360) and saturation (0.0-1.0)
light.set_light_color(hue=128, saturation=0.5)

# Set the startup behavior of the light
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
startup_on_off: Optional[StartupEnum] = None
status_light: Optional[bool] = None
identify_period: Optional[int] = None
permitting_join: Optional[bool] = None
energy_consumed_at_last_reset: Optional[float] = None
current_active_power: Optional[float] = None
current_amps: Optional[float] = None
current_voltage: Optional[float] = None
total_energy_consumed: Optional[float] = None
total_energy_consumed_last_updated: Optional[datetime.datetime] = None
time_of_last_energy_reset: Optional[datetime.datetime] = None
```

Available methods for outlet are:

```python
# Reload the air outlet data from the hub
outlet.reload()

# Set the name of the outlet
outlet.set_name(name="kitchen socket 1")

# Turn the outlet on or off
outlet.set_on(outlet_on=True)

# Set the startup behavior of the outlet
outlet.set_startup_behaviour(behaviour=StartupEnum.START_OFF)
```

## [Controlling Air Purifier](./src/dirigera/devices/air_purifier.py)

To get information about the available air purifiers, you can use the `get_air_purifiers()` method:

```python
air_purifiers = dirigera_hub.get_air_purifiers()
```

The air purifier object has the following attributes (additional to the core attributes):

```python
fan_mode: FanModeEnum
fan_mode_sequence: str
motor_state: int
child_lock: bool
status_light: bool
motor_runtime: int
filter_alarm_status: bool
filter_elapsed_time: int
filter_lifetime: int
current_p_m25: int
```

Available methods for blinds are:

```python
# Reload the air purifier data from the hub
air_purifier.reload()

# Set the name of the air purifier
air_purifier.set_name(name="living room purifier")

# Set the fan mode of the air purifier
air_purifier.set_fan_mode(fan_mode=FanModeEnum.AUTO)

# Set the motor state of the air purifier (0-50)
air_purifier.set_motor_state(motor_state=42)

# Enable or disable the child lock
air_purifier.set_child_lock(child_lock=True)

# Turn the status light on or off
air_purifier.set_status_light(light_state=False)
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
battery_percentage: Optional[int] = None
```

Available methods for blinds are:

```python
# Reload the blind data from the hub
blind.reload()

# Set the name of the blind
blind.set_name(name="kitchen blind 1")

# Set the target level of the blind (0-100)
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
is_on: Optional[bool] = None
battery_percentage: Optional[int] = None
switch_label: Optional[str] = None
```

Available methods for controller are:

```python
# Reload the controller data from the hub
controller.reload()

# Set the name of the controller
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
current_temperature: Optional[float] = None
current_r_h: Optional[int] = None  # current humidity
current_p_m25: Optional[int] = None # current particulate matter 2.5
max_measured_p_m25: Optional[int] = None # maximum measurable particulate matter 2.5
min_measured_p_m25: Optional[int] = None # minimum measurable particulate matter 2.5
voc_index: Optional[int] = None # current volatile organic compound
```

Available methods for environment sensor are:

```python
# Reload the environment sensor data from the hub
sensor.reload()

# Set the name of the environment sensor
sensor.set_name(name="Bathroom Sensor")
```

# [Scene](./src/dirigera/devices/scene.py)

To get the scenes use:

```python
scenes = dirigera_hub.get_scenes()
```

The scene object has the following attributes:

```python
id: str
type: SceneType
info: Info
triggers: List[Trigger]
actions: List[Action]
created_at: datetime.datetime
last_completed: Optional[datetime.datetime] = None
last_triggered: Optional[datetime.datetime] = None
last_undo: Optional[datetime.datetime] = None
commands: List[str]
undo_allowed_duration: int
```

Details to the `Trigger`, `Action` and `Info` class can be found in [scene.py](./src/dirigera/devices/scene.py)

Available methods for scene are:

```python
scene.reload()
scene.trigger()
scene.undo()
```

### Creating a Scene

To create a scene use the `create_scene()` function.  
Example how to create an empty scene:

```python
scene = dirigera_hub.create_scene(
    info=Info(name="This is empty", icon=Icon.SCENES_BOOK),
)
```

Actions look like this:

```python
class Action(BaseIkeaModel):
    id: str
    type: str
    enabled: Optional[bool] = None
    attributes: Optional[ActionAttributes] = None
```

Example how create scene with action:

```python
from dirigera.devices.scene import Info, Icon, SceneType, Action, ActionAttributes

light = dirigera_hub.get_light_by_name("kitchen_lamp")

scene = dirigera_hub.create_scene(
    info=Info(name="Scene with action", icon=Icon.SCENES_BOOK),
    scene_type=SceneType.USER_SCENE,
    triggers=[],
    actions=[Action(id=light.id, type="device", enabled=True, attributes=ActionAttributes(is_on=False))],
)
```

Triggers look like this:

```python
class Trigger(BaseIkeaModel):
    id: Optional[str] = None
    type: str
    triggered_at: Optional[datetime.datetime] = None
    disabled: bool
    trigger: Optional[TriggerDetails] = None
```

Example how to create scene with trigger:

```python
from dirigera.devices.scene import Info, Icon, Trigger, SceneType, TriggerDetails, ControllerType, ClickPattern

scene = dirigera_hub.create_scene(
   info=Info(name="Scene with trigger", icon=Icon.SCENES_HEART),
   scene_type=SceneType.USER_SCENE,
   triggers=[
       Trigger(type="app", disabled=False),
       Trigger(type="controller", disabled=False,
               trigger=TriggerDetails(clickPattern=ClickPattern.SINGLE_PRESS, buttonIndex=0,
                                      deviceId="0000aaaa-0000-0000-aa00-0a0aa0a000a0_1",
                                      controllerType=ControllerType.SHORTCUT_CONTROLLER))])
```

All available icons can be found here: [Icons](./src/dirigera/devices/scene.py)

## [Motion Sensor](./src/dirigera/devices/motion_sensor.py)

To get information about the available motion sensors, you can use the `get_motion_sensors()` method:

```python
motions_sensors = dirigera_hub.get_motion_sensors()
```

The motion sensor object has the following attributes (additional to the core attributes):

```python
battery_percentage: Optional[int] = None
is_on: bool
light_level: Optional[float] = None
is_detected: Optional[bool] = False
```

Available methods for outlet are:

```python
# Reload the motion sensor data from the hub
motion_sensor.reload()

# Set the name of the motion sensor
motion_sensor.set_name(name="kitchen sensor 1")
```

## [Open Close Sensor](./src/dirigera/devices/open_close_sensor.py)

To get information about the available open/close sensors, you can use the `get_open_close_sensors()` method:

```python
open_close_sensors = dirigera_hub.get_open_close_sensors()
```

The open_close_sensor object has the following attributes (additional to the core attributes):

```python
is_open: bool
battery_percentage: Optional[int] = None
```

Available methods for outlet are:

```python
# Reload the open/close sensor data from the hub
open_close_sensor.reload()

# Set the name of the open/close sensor
open_close_sensor.set_name(name="window 1")
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
EDIT: This is now an exposed feature in the app.

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
