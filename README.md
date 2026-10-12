# dirigera

[![Tests](https://github.com/Leggin/dirigera/actions/workflows/tests.yml/badge.svg)](https://github.com/Leggin/dirigera/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/dirigera)](https://pypi.org/project/dirigera/)
[![Python versions](https://img.shields.io/pypi/pyversions/dirigera)](https://pypi.org/project/dirigera/)
[![Downloads](https://static.pepy.tech/badge/dirigera/month)](https://pepy.tech/project/dirigera)

A Python client for the IKEA DIRIGERA smart home hub. Control lights, outlets, blinds, air purifiers and scenes, read sensors, and react to events, all through the hub's local API without the IKEA cloud.

```python
import dirigera

dirigera_hub = dirigera.Hub(token="<your token>", ip_address="192.168.1.20")

lamp = dirigera_hub.get_light_by_name(lamp_name="Desk lamp")
lamp.set_light(lamp_on=True)
lamp.set_light_level(light_level=60)

for sensor in dirigera_hub.get_environment_sensors():
    print(sensor.attributes.custom_name, sensor.attributes.current_temperature)
```

This is an unofficial project and not affiliated with IKEA. It is based on the hub's undocumented local API, so firmware updates can change its behaviour.

## Contents

- [Installation](#installation)
- [Getting started](#getting-started)
- [Supported devices](#supported-devices)
- [Usage](#usage)
  - [Finding devices](#finding-devices)
  - [Working with devices](#working-with-devices)
  - [Lights](#lights)
  - [Outlets](#outlets)
  - [Electrical sensors](#electrical-sensors)
  - [Blinds](#blinds)
  - [Air purifiers](#air-purifiers)
  - [Controllers](#controllers)
  - [Sensors](#sensors)
  - [Scenes](#scenes)
  - [Listening to events](#listening-to-events)
  - [Raw API access](#raw-api-access)
- [Troubleshooting](#troubleshooting)
- [Related projects](#related-projects)
- [Contributing](#contributing)
- [License](#license)

## Installation

```bash
pip install dirigera
```

The library is tested on Python 3.8 to 3.14.

## Getting started

1. **Find the IP address of your hub**, for example in your router's list of connected devices. The hub also announces itself on the local network as `gw2-<id>.local`.

2. **Generate a token.** The package installs a `generate-token` command:

   ```bash
   generate-token 192.168.1.20
   ```

   When asked, press the action button on the bottom of the hub, then press ENTER. The token is printed to the console. You only need to do this once.

3. **Connect to the hub** with the token and IP address:

   ```python
   import dirigera

   dirigera_hub = dirigera.Hub(token="<your token>", ip_address="192.168.1.20")

   for light in dirigera_hub.get_lights():
       print(light.attributes.custom_name, light.attributes.is_on)
   ```

The token gives full control over your hub, so keep it out of your source code, for example by reading it from an environment variable.

## Supported devices

| Device type | Fetch with | Known to work with |
| --- | --- | --- |
| Lights | `get_lights()` | TRADFRI bulbs, KAJPLATS, ORMANAS LED strip |
| Outlets | `get_outlets()` | TRADFRI control outlet, TRETAKT, INSPELNING, GRILLPLATS |
| Electrical sensors | `get_electrical_sensors()` | GRILLPLATS |
| Blinds | `get_blinds()` | FYRTUR |
| Air purifiers | `get_air_purifiers()` | STARKVIND |
| Controllers | `get_controllers()` | STYRBAR, RODRET, SOMRIG, TRADFRI on/off switch |
| Environment sensors | `get_environment_sensors()` | VINDSTYRKA, ALPSTUGA |
| Motion sensors | `get_motion_sensors()` | TRADFRI motion sensor, VALLHORN |
| Light sensors | `get_light_sensors()` | MYGGSPRAY, VALLHORN |
| Occupancy sensors | `get_occupancy_sensors()` | MYGGSPRAY |
| Open/close sensors | `get_open_close_sensors()` | – |
| Water sensors | `get_water_sensors()` | BADRING |

Devices from other manufacturers that are paired with the hub often work as well, as long as the hub reports them as one of these device types. If a device is missing or fails to load, please [open an issue](https://github.com/Leggin/dirigera/issues) and include its data from `dirigera_hub.get("/devices")`.

## Usage

All examples assume a connected hub:

```python
import dirigera

dirigera_hub = dirigera.Hub(token="<your token>", ip_address="192.168.1.20")
```

### Finding devices

Every device type can be fetched as a list, by its name from the IKEA app, or by its id:

```python
lights = dirigera_hub.get_lights()
light = dirigera_hub.get_light_by_name(lamp_name="Desk lamp")
light = dirigera_hub.get_light_by_id(id_=light.id)

devices = dirigera_hub.get_all_devices()  # all supported devices
```

The hub doesn't return devices in a fixed order, so look devices up by name or id rather than by their position in a list. Lookups by name raise an `AssertionError` if no device has that name. Lookups by id raise a `ValueError` if the id doesn't exist or belongs to another device type.

<details>
<summary>All getters</summary>

| Device type | All | By name | By id |
| --- | --- | --- | --- |
| Lights | `get_lights()` | `get_light_by_name(lamp_name=...)` | `get_light_by_id(id_=...)` |
| Outlets | `get_outlets()` | `get_outlet_by_name(outlet_name=...)` | `get_outlet_by_id(id_=...)` |
| Electrical sensors | `get_electrical_sensors()` | – | `get_electrical_sensor_by_id(id_=...)` |
| Blinds | `get_blinds()` | `get_blind_by_name(blind_name=...)` | `get_blinds_by_id(id_=...)` |
| Air purifiers | `get_air_purifiers()` | `get_air_purifier_by_name(air_purifier_name=...)` | `get_air_purifier_by_id(id_=...)` |
| Controllers | `get_controllers()` | `get_controller_by_name(controller_name=...)` | `get_controller_by_id(id_=...)` |
| Environment sensors | `get_environment_sensors()` | `get_environment_sensor_by_name(environment_sensor_name=...)` | `get_environment_sensor_by_id(id_=...)` |
| Motion sensors | `get_motion_sensors()` | `get_motion_sensor_by_name(motion_sensor_name=...)` | `get_motion_sensor_by_id(id_=...)` |
| Light sensors | `get_light_sensors()` | `get_light_sensor_by_name(light_sensor_name=...)` | `get_light_sensor_by_id(id_=...)` |
| Occupancy sensors | `get_occupancy_sensors()` | `get_occupancy_sensor_by_name(occupancy_sensor_name=...)` | `get_occupancy_sensor_by_id(id_=...)` |
| Open/close sensors | `get_open_close_sensors()` | `get_open_close_sensor_by_name(open_close_sensor_name=...)` | `get_open_close_by_id(id_=...)` |
| Water sensors | `get_water_sensors()` | `get_water_sensor_by_name(water_sensor_name=...)` | `get_water_sensor_by_id(id_=...)` |
| Scenes | `get_scenes()` | `get_scene_by_name(scene_name=...)` | `get_scene_by_id(scene_id=...)` |
| Adaptive profiles | `get_adaptive_profiles()` | – | – |
| All devices | `get_all_devices()` | – | – |

</details>

### Working with devices

Each device is a Python object with these fields:

| Field | Description |
| --- | --- |
| `id` | Unique id of the device |
| `relation_id` | Shared by devices that belong to the same physical product (see below) |
| `type`, `device_type` | Device type as reported by the hub, e.g. `"light"` |
| `is_reachable` | Whether the hub can currently reach the device |
| `last_seen`, `created_at` | Timestamps |
| `room` | Room from the IKEA app (`id`, `name`, `color`, `icon`), if assigned |
| `capabilities` | `can_send` and `can_receive`: the attributes the device sends or accepts |
| `attributes` | The device state, e.g. `is_on` or `current_temperature` (listed per device type below), plus `custom_name`, `model`, `manufacturer`, `firmware_version`, `hardware_version`, `serial_number`, `product_code` and firmware update (`ota_*`) fields |

Attribute names are the hub's names in snake_case: the hub's `lightLevel` is `light_level`.

The setter methods send the change to the hub and update the object. Most of them first check the device's capabilities and the allowed value range, and raise an `AssertionError` or `ValueError` without sending anything if the change isn't supported. To get the latest state from the hub, call `reload()`. It updates the object in place:

```python
light = dirigera_hub.get_light_by_name(lamp_name="Desk lamp")
light.reload()
print(light.attributes.is_on)
```

Some products appear as several devices that share the same `relation_id`. The VALLHORN, for example, is a motion sensor and a light sensor, and the GRILLPLATS plug is an outlet and an electrical sensor.

### Lights

| Attribute | Description |
| --- | --- |
| `is_on` | Whether the light is on |
| `light_level` | Brightness, 1–100 |
| `color_temperature` | Color temperature in Kelvin |
| `color_temperature_min`, `color_temperature_max` | Supported color temperature range, as reported by the bulb |
| `color_hue`, `color_saturation` | Color, hue 0–360 and saturation 0–1 |
| `startup_on_off` | Behaviour after a power outage (`StartupEnum`) |

```python
from dirigera.devices.device import StartupEnum

light = dirigera_hub.get_light_by_name(lamp_name="Desk lamp")

light.set_light(lamp_on=True)
light.set_light_level(light_level=60)
light.set_color_temperature(color_temp=2700)  # Kelvin
light.set_light_color(hue=30, saturation=0.8)
light.set_startup_behaviour(behaviour=StartupEnum.START_PREVIOUS)
light.set_name(name="Reading lamp")
```

`set_color_temperature()` checks the value against the range the bulb reports. Some bulbs report this range in mireds instead of Kelvin; the library converts it, so always pass Kelvin.

`StartupEnum` controls what happens when power returns after an outage: `START_ON`, `START_OFF`, `START_PREVIOUS` (restore the previous state) or `START_TOGGLE` (switching the power off and on again toggles the light).

#### Adaptive lighting

Adaptive profiles are created in the IKEA app and define light levels and color temperatures over the day. A light that follows a profile is adjusted by the hub automatically, which interpolates between the entries of the schedule.

```python
profile = dirigera_hub.get_adaptive_profiles()[0]
for entry in profile.adaptive_schedule:
    print(entry.start_time, entry.light_level, entry.color_temperature)

light.activate_adaptive_profile(profile_id=profile.id)
```

Changing a light manually, for example by setting its light level, takes it out of adaptive mode. `light.adaptive_profile.active` shows whether a light currently follows a profile (call `light.reload()` first to get the current state).

### Outlets

| Attribute | Description |
| --- | --- |
| `is_on` | Whether the outlet is switched on |
| `startup_on_off` | Behaviour after a power outage (`StartupEnum`) |
| `status_light` | Whether the status light is on |
| `current_active_power` | Current power in W |
| `current_amps`, `current_voltage` | Current in A and voltage in V |
| `total_energy_consumed` | Total energy in kWh |
| `energy_consumed_at_last_reset`, `time_of_last_energy_reset`, `total_energy_consumed_last_updated` | Energy counter details |

The energy values are only available on outlets with energy metering, such as INSPELNING.

```python
from dirigera.devices.device import StartupEnum

outlet = dirigera_hub.get_outlet_by_name(outlet_name="Coffee machine")

outlet.set_on(outlet_on=True)
outlet.set_startup_behaviour(behaviour=StartupEnum.START_OFF)
outlet.set_name(name="Espresso machine")
```

### Electrical sensors

Some plugs, such as GRILLPLATS, report their energy values as a separate electrical sensor instead of on the outlet. It has the same energy attributes as outlets (`current_active_power`, `current_amps`, `current_voltage`, `total_energy_consumed`, ...). The sensor and the outlet share the same `relation_id`:

```python
outlet = dirigera_hub.get_outlet_by_name(outlet_name="Grill")
electrical_sensor = next(
    sensor
    for sensor in dirigera_hub.get_electrical_sensors()
    if sensor.relation_id == outlet.relation_id
)
print(electrical_sensor.attributes.current_active_power)
```

### Blinds

| Attribute | Description |
| --- | --- |
| `blinds_current_level` | Current position, 0–100 |
| `blinds_target_level` | Position the blind is moving to, 0–100 |
| `blinds_state` | `"up"`, `"down"` or `"stopped"` |
| `battery_percentage` | Battery level |

```python
from dirigera.devices.blinds import BlindsStateEnum

blind = dirigera_hub.get_blind_by_name(blind_name="Bedroom blind")

blind.set_target_level(target_level=50)
blind.set_state(state=BlindsStateEnum.STOPPED)  # or UP / DOWN
blind.set_name(name="Window blind")
```

### Air purifiers

| Attribute | Description |
| --- | --- |
| `fan_mode` | `FanModeEnum`: `OFF`, `ON`, `LOW`, `MEDIUM`, `HIGH` or `AUTO` |
| `motor_state` | Fan speed, 0–50 |
| `current_p_m25` | Particulate matter (PM2.5) |
| `child_lock`, `status_light` | Whether the child lock and status light are on |
| `filter_alarm_status`, `filter_elapsed_time`, `filter_lifetime` | Filter state |
| `motor_runtime`, `fan_mode_sequence` | Further fan details |

```python
from dirigera.devices.air_purifier import FanModeEnum

air_purifier = dirigera_hub.get_air_purifier_by_name(air_purifier_name="Living room purifier")

air_purifier.set_fan_mode(fan_mode=FanModeEnum.AUTO)
air_purifier.set_motor_state(motor_state=30)  # 0 = off, 1 = auto, up to 50
air_purifier.set_child_lock(child_lock=True)
air_purifier.set_status_light(light_state=False)
air_purifier.set_name(name="Bedroom purifier")
```

### Controllers

Remotes (`device_type` `"lightController"`) and shortcut buttons such as SOMRIG (`"shortcutController"`) have the attributes `battery_percentage`, `is_on` and `switch_label`, and support `reload()` and `set_name()`.

Button presses are not stored as device state. To react to them, use the [event listener](#listening-to-events) or create a [scene](#scenes) with a controller trigger.

### Sensors

All sensors support `reload()` and `set_name(name=...)`. Battery powered sensors have a `battery_percentage` attribute.

| Sensor | Fetch with | Attributes |
| --- | --- | --- |
| Environment sensor | `get_environment_sensors()` | `current_temperature` (°C), `current_r_h` (relative humidity in %), `current_p_m25`, `max_measured_p_m25`, `min_measured_p_m25`, `voc_index` (VINDSTYRKA), `current_c_o2` (ppm, ALPSTUGA) |
| Motion sensor | `get_motion_sensors()` | `is_detected`, `is_on`, `light_level` |
| Light sensor | `get_light_sensors()` | `illuminance`, `min_illuminance`, `max_illuminance` |
| Occupancy sensor | `get_occupancy_sensors()` | `is_detected` |
| Open/close sensor | `get_open_close_sensors()` | `is_open` |
| Water sensor | `get_water_sensors()` | `water_leak_detected` |

```python
door = dirigera_hub.get_open_close_sensor_by_name(open_close_sensor_name="Front door")
print("open" if door.attributes.is_open else "closed")

for sensor in dirigera_hub.get_water_sensors():
    if sensor.attributes.water_leak_detected:
        print(f"Leak at {sensor.attributes.custom_name}!")
```

### Scenes

```python
scene = dirigera_hub.get_scene_by_name(scene_name="Movie night")

scene.trigger()  # run the scene
scene.undo()     # undo it again shortly afterwards
dirigera_hub.delete_scene(scene_id=scene.id)
```

A scene has an `info` (`name` and `icon`), a list of `triggers` that start it and a list of `actions` it performs.

#### Creating scenes

`create_scene()` creates a scene and returns it. Without triggers, the scene can be run from the app or with `scene.trigger()`.

The scene models use the hub's camelCase names when you create them, for example `clickPattern=...`, while their fields are read in snake_case, for example `trigger.click_pattern`.

A scene that turns a light off:

```python
from dirigera.devices.scene import Action, ActionAttributes, Icon, Info

light = dirigera_hub.get_light_by_name(lamp_name="Desk lamp")

scene = dirigera_hub.create_scene(
    info=Info(name="Desk lamp off", icon=Icon.SCENES_BOOK),
    actions=[
        Action(id=light.id, type="device", enabled=True, attributes=ActionAttributes(is_on=False)),
    ],
)
```

A scene that runs when a shortcut button is pressed:

```python
from dirigera.devices.scene import ClickPattern, ControllerType, Icon, Info, Trigger, TriggerDetails

button = dirigera_hub.get_controller_by_name(controller_name="Shortcut button")

scene = dirigera_hub.create_scene(
    info=Info(name="Button scene", icon=Icon.SCENES_HEART),
    triggers=[
        Trigger(
            type="controller",
            disabled=False,
            trigger=TriggerDetails(
                controllerType=ControllerType.SHORTCUT_CONTROLLER,
                clickPattern=ClickPattern.SINGLE_PRESS,
                buttonIndex=0,
                deviceId=button.id,
            ),
        ),
    ],
)
```

A scene that runs every evening at 22:00 and ends after one hour:

```python
from dirigera.devices.scene import EndTriggerEvent, Icon, Info, Trigger, TriggerDetails

scene = dirigera_hub.create_scene(
    info=Info(name="Evening", icon=Icon.SCENES_MOON),
    triggers=[
        Trigger(
            type="time",
            disabled=False,
            trigger=TriggerDetails(days=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], time="22:00"),
            endTriggerEvent=EndTriggerEvent(type="duration", trigger=TriggerDetails(duration=3600)),
        ),
    ],
)
```

All icons are listed in the [`Icon` enum](https://github.com/Leggin/dirigera/blob/main/src/dirigera/devices/scene.py).

### Listening to events

The hub publishes an event whenever something changes, for example when a light is switched or a sensor detects motion. `create_event_listener()` connects to the hub and calls your functions for each event. Each message is a JSON string with the event `type` (for example `deviceStateChanged`, `sceneCreated`, `sceneUpdated` or `sceneDeleted`) and its `data`, which includes the `id` of the device or scene:

```python
import json

light = dirigera_hub.get_light_by_name(lamp_name="Desk lamp")

def on_message(ws, message: str):
    event = json.loads(message)
    if event["data"].get("id") == light.id:
        print(event["type"], event["data"].get("attributes"))

def on_error(ws, error):
    print(error)

dirigera_hub.create_event_listener(on_message=on_message, on_error=on_error)
```

```
deviceStateChanged {'isOn': False}
```

`create_event_listener()` blocks until the connection is closed. Call `dirigera_hub.stop_event_listener()`, for example from another thread, to close it. It also accepts `on_open`, `on_close` and the other callbacks of [websocket-client's `WebSocketApp`](https://websocket-client.readthedocs.io/en/latest/app.html).

#### Reconnecting

The hub sometimes closes the connection on its own (status 1000, "disconnected due to inactivity."), and `create_event_listener()` then returns. The `reconnect` argument doesn't cover this, as it only reconnects after connection errors. To keep listening, call it in a loop:

```python
import time

running = True

def stop_listening():
    # create_event_listener() blocks, so call this from another thread
    global running
    running = False
    dirigera_hub.stop_event_listener()

while running:
    dirigera_hub.create_event_listener(on_message=on_message, on_error=on_error)
    time.sleep(5)  # short pause before listening again
```

Events that happen while the listener reconnects are missed. If you need the current state, fetch it again after reconnecting, for example in `on_open`.

### Raw API access

For anything the library doesn't cover yet, you can send requests to the hub's API directly. The hub responds with the raw JSON data:

```python
devices = dirigera_hub.get("/devices")

light = dirigera_hub.get_light_by_name(lamp_name="Desk lamp")
dirigera_hub.patch(route=f"/devices/{light.id}", data=[{"attributes": {"lightLevel": 30}}])
```

`post()` and `delete()` work the same way.

## Troubleshooting

<details>
<summary><code>generate-token</code> times out</summary>

Check the MTU of the network interface that connects to the hub. A mismatch, such as jumbo frames (MTU 9000) on your computer while the hub uses 1500, makes the connection time out. Setting the interface to an MTU of 1500 fixes it.

</details>

<details>
<summary>The token stopped working</summary>

Generate a new token with `generate-token`, for example after a factory reset of the hub.

</details>

<details>
<summary>Loading devices fails with a <code>ValidationError</code>, or a device is missing</summary>

The device reports data that the library doesn't expect yet, or its device type isn't supported. Please [open an issue](https://github.com/Leggin/dirigera/issues) with the device's data, which you get with `dirigera_hub.get("/devices")`. Remove the serial number if you like.

</details>

<details>
<summary>A setter raises <code>AssertionError: ... does not support ...</code></summary>

The device doesn't accept this attribute. `device.capabilities.can_receive` lists what it does accept.

</details>

<details>
<summary>The event listener stops after a while</summary>

The hub closes idle connections on its own. See [Reconnecting](#reconnecting).

</details>

<details>
<summary>Why is the hub's certificate not verified?</summary>

The hub uses a self-signed certificate, so the library connects without verifying it.

</details>

## Related projects

- [dirigera_platform](https://github.com/sanjoyg/dirigera_platform): Home Assistant integration built on this library
- [lpgera/dirigera](https://github.com/lpgera/dirigera): TypeScript client for the DIRIGERA hub

## Contributing

Contributions are welcome: [open an issue](https://github.com/Leggin/dirigera/issues) for bugs and device support, or send a pull request.

To set up a development environment, run `setup.sh`. It creates a virtual environment and installs `requirements.txt` and `dev-requirements.txt`. Then:

- `run-test.sh` or `pytest` runs the tests
- `run-pylint.sh` runs the linter
- `run-mypy.sh` runs the type checks
- `run-python-versions-test.sh` runs the tests on all supported Python versions (requires Docker)

The same checks run automatically on every pull request.

## License

[MIT](https://github.com/Leggin/dirigera/blob/main/LICENSE)
