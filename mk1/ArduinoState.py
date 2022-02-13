from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ArduinoState:
    state: str = None | "startup" | "calibrating" | "ready" | "moving" | "error"
    x_pos: int = None
    y_pos: int = None
    z_pos: int = None
    grabber_state: str = None | "open" | "closed"
