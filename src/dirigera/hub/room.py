from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class Color(Enum):
    IKEA_BEIGE_1 = "ikea_beige_1"
    IKEA_BEIGE_NO_3 = "ikea_beige_no_3"
    IKEA_BEIGE_NO_4 = "ikea_beige_no_4"
    IKEA_BLUE_NO_52 = "ikea_blue_no_52"
    IKEA_BLUE_NO_58 = "ikea_blue_no_58"
    IKEA_BLUE_NO_60 = "ikea_blue_no_60"
    IKEA_BLUE_NO_63 = "ikea_blue_no_63"
    IKEA_BROWN_NO_41 = "ikea_brown_no_41"
    IKEA_GREEN_NO_63 = "ikea_green_no_63"
    IKEA_GREEN_NO_65 = "ikea_green_no_65"
    IKEA_GREEN_NO_66 = "ikea_green_no_66"
    IKEA_LILAC_NO_3 = "ikea_lilac_no_3"
    IKEA_ORANGE_NO_11 = "ikea_orange_no_11"
    IKEA_PINK_NO_4 = "ikea_pink_no_4"
    IKEA_PINK_NO_6 = "ikea_pink_no_6"
    IKEA_PINK_NO_8 = "ikea_pink_no_8"
    IKEA_RED_NO_39 = "ikea_red_no_39"
    IKEA_TURQUOISE_5 = "ikea_turquoise_5"
    IKEA_WHITE_NO_20 = "ikea_white_no_20"
    IKEA_YELLOW_NO_24 = "ikea_yellow_no_24"
    IKEA_YELLOW_NO_27 = "ikea_yellow_no_27"
    IKEA_YELLOW_NO_28 = "ikea_yellow_no_28"
    IKEA_YELLOW_NO_30 = "ikea_yellow_no_30"
    IKEA_YELLOW_NO_31 = "ikea_yellow_no_31"
    NCS_S_1020_R10B = "ncs_s_1020_r10b"
    NCS_S_4010_G10Y = "ncs_s_4010_g10y"
    PANTONE_15_0522_TCX = "pantone_15_0522_tcx"
    PANTONE_16_0230_TCX = "pantone_16_0230_tcx"
    PANTONE_16_0940_TCX = "pantone_16_0940_tcx"


@dataclass
class Room:
    room_id: str
    name: str
    color: Color
    icon: str


def dict_to_room(data: Dict[str, Any]):
    return Room(
        room_id=data["id"],
        name=data["name"],
        color=Color(data["color"]),
        icon=data["icon"],
    )
