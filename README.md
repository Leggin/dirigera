# Dirigera Python client

This repository provides an unofficial Python client for controlling the IKEA Dirigera Smart Home Hub. Currently, only light control is supported, but support for other features will be added in the future.

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

## Dirigera Hub

Setting up the client works by providing the token and ip address that is read from your .env file by the `config.py`

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


## Event Listener
The event listener allows you to listen to events that are published by your Dirigera hub. This is useful if you want to automate tasks based on events such as when a light is turned on or off, or when the color temperature of a light is changed.

```python

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

Contributions are welcome! If you have an idea for a new feature or a bug fix, please submit a pull request.

## License

The MIT License (MIT)

Copyright (c) 2023 Leggin