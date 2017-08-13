import noise
import numpy as np


class World:
    def __init__(self, dims):
        self._dims = dims
        self.time = 0
        self._noise_seed = np.random.randint(1000000)  # bah why not

        self.entities = {}

    def add_entity(self, e):
        self.entities[e.id] = e

    def remove_entity(self, e):
        del self.entities[e.id]

    def remove_all_entities(self):
        self.entities.clear()

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

        for e in self.entities:
            e.pos += e.velocity * dt
