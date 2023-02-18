# Dirigera Python client

This repository provides an unofficial Python client for controlling the IKEA Dirigera Smart Home Hub. Currently, only light control is supported, but support for other features will be added in the future.

## Installation

Install the requirements with:

```bash
bash setup.sh
```

## Quickstart

1. Find out the ip-address of your Dirigera (check your router)
2. Copy the address and set the value of `DIRIGERA_IP_ADDRESS` in the `.env-template` file to the ip
3. Rename the `.env-template` file to `.env`
4. Run the authentication script:
   ```bash
   bash auth.sh
   ```
   When prompted, you must push the action button on Dirigera. After that hit ENTER and your `token` will be printed to the console.  
   Example:
   ```
    Press the action button on Dirigera then hit ENTER ...
    Your Token (put this into your .env file):
    mgwB.aXqwpzV89N0aUwBhZMJjD8a.UBPyzy2InGtqgwo2MO5.xX4ug7.uBcVJquwYzLnAijF7SdYKvNxTo0uzQKahV10A-3ZQOz-UAubGP6sHWt1CJx3QmWZyE7ZcMZKgODXjSzWL1lumKgGz5dUIwFi3rhNxgK-IsBGeGVhNXPt8vGrYEcZePwPvNAIg8RqmlH27L-JZPnkAtP2wHoOdW72Djot3yJsohtEsb0p9mJvoZFSavTlTr4LDuf584vuH5fha5xoR9QhhIvvgbAP-s4EHFqENNi6vrYLHKR.sdqnv4sYw6UH-l6oiPnnRLxinoqBPOlWhlcL9doFviXQE.tZ9X8WVqyBrd0NYHlo9iorEvUbnZuD02BEJrg4NLwgh3rZtyF0Mi46HenynzBohbPn4RnuSYYCiHt5EZnWedxBtDqc7mSTm1ZtyD
   ```
5. Copy your full token and set the value of `DIRIGERA_TOKEN` in the `.env` file
6. Run the example
    ```bash
    bash run-example.sh
    ```

## Dirigera Hub

Setting up the client works by providing the token and ip address that is read from your .env file by the `config.py`

```python
dirigera_hub = DirigeraHub(
    token=config.DIRIGERA_TOKEN,
    base_url=config.DIRIGERA_IP_ADDRESS
)
```

## [Controlling Lights](./models/light.py)

To get information about the available lights, you can use the `get_lights()` method:

```python
light = dirigera_hub.get_lights()
```

The light object has the following attributes:

```python
    lamp_id: str
    is_reachable: bool
    custom_name: str
    is_on: bool
    startup_on_off: StartupEnum
    light_level: int | None  # not all lights have a light level
    color_temp: int | None  # not all lights have a color temperature
    color_temp_min: int | None
    color_temp_max: int | None
    color_hue: int | None  # not all lights have a color hue
    color_saturation: float | None  # not all lights have a color saturation
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


## Contributing

Contributions are welcome! If you have an idea for a new feature or a bug fix, please submit a pull request.

## License

The MIT License (MIT)

Copyright (c) 2023 Leggin