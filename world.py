import noise
import numpy as np


class World:
    def __init__(self, dims):
        self._dims = dims
        self.time = 0
        self._noise_seed = np.random.randint(1000000)  # bah why not
        self.entities = {}

        # arbitrary for testing
        radiuss = np.random.randint(60, 120, size=3)
        self.death_zones = [
            ((radiuss[0], radiuss[0]), radiuss[0]),
            ((dims[0] - radiuss[1], dims[1] - radiuss[1]), radiuss[1]),
            ((dims[0]/2 - radiuss[2], dims[1]/2 - radiuss[2]), radiuss[2])
        ]

    def is_in_death_zone(self, e):
        pos = e.pos
        for (zone_centre, zone_radius) in self.death_zones:
            dx = zone_centre[0] - pos[0]
            dy = zone_centre[1] - pos[1]
            dist_sqrd = (dx * dx) + (dy * dy)
            if dist_sqrd <= zone_radius * zone_radius:
                return True

        return False

    def is_inside(self, e):
        pos = e.pos
        rad = e.RADIUS / 2
        return rad <= pos[0] < self.dims[0] - rad and rad <= pos[1] < self.dims[1] - rad


    def add_entity(self, e):
        self.entities[e.id] = e

    def remove_entity(self, e):
        self.entities.pop(e.id, None)

    def remove_all_entities(self):
        self.entities = {}

    @property
    def dims(self):
        return self._dims

    def get_temperature(self, pos):
        return noise.snoise2(*pos, base=self._noise_seed, octaves=2)

    def get_time(self):
        return self.time / 1000

    def tick(self, dt):
        # TODO dt doesnt affect time
        self.time = (self.time + 1) % 1000

        for e in self.entities.values():
            e.pos += e.velocity * dt
