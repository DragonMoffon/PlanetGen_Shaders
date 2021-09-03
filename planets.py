from dataclasses import dataclass
from PIL import Image

from typing import Tuple

import constants as c


@dataclass()
class Planet:
    pos: Tuple[int, int]
    radius: int = c.EARTH_RADIUS
    mass: int = c.EARTH_MASS
    rotation: float = 0
    plate_map: Image = None
    plates: list = None

    @property
    def shader_data(self):
        return *self.pos, self.radius, self.rotation

    def on_update(self, delta_time: float = 1/60):
        self.rotation = (self.rotation - delta_time*60) % 1440

    def set_plates(self, plate_map, plates):
        self.plate_map = plate_map
        self.plates = plates


Earth = Planet((int(c.EARTH_RADIUS*1.0003), 0))

