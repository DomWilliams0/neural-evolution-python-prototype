import noise
import numpy as np
import pymunk


class World:
    def __init__(self, dims):
        self._dims = dims
        self.time = 0
        self._noise_seed = np.random.randint(1000000)  # bah why not

        self.physics = pymunk.Space()
        self.physics.gravity = (0, 0)

    @property
    def dims(self):
        return self._dims

    def get_temperature(self, pos):
        return noise.snoise2(*pos, base=self._noise_seed, octaves=2)

    def get_time(self):
        return self.time / 1000

    def tick(self, dt):
        self.time = (self.time + 1) % 1000
        self.physics.step(dt)
