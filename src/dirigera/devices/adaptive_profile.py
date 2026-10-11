from __future__ import annotations
from typing import List, Optional
from pydantic import Field
from .base_ikea_model import BaseIkeaModel


class AdaptiveScheduleEntry(BaseIkeaModel):
    start_time: str  # "HH:MM"
    light_level: Optional[int] = None
    color_temperature: Optional[int] = None


class AdaptiveProfile(BaseIkeaModel):
    id: str
    name: Optional[str] = None
    adaptive_schedule: List[AdaptiveScheduleEntry] = Field(default_factory=list)


class AdaptiveProfileState(BaseIkeaModel):
    """The adaptive profile state of a light, empty if the light is not in adaptive mode"""

    id: Optional[str] = None
    active: Optional[bool] = None
