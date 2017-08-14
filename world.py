import noise
import numpy as np
from Box2D import *

from config import *


class World:
    def __init__(self, dims):
        self._dims = dims
        self.time = 0
        self._noise_seed = np.random.randint(1000000)  # bah why not

        self._world = b2World(gravity=(0, 0))

    def is_inside(self, e):
        pos = e.pos
        rad = ENTITY_RADIUS / 2
        return rad <= pos[0] < self.dims[0] - rad and rad <= pos[1] < self.dims[1] - rad

    def add_entity(self, e):
        e.body = self._world.CreateDynamicBody(userData=e)
        e.body.CreateCircleFixture(radius=ENTITY_RADIUS)

    def remove_entity(self, e):
        if e.body:
            self._world.DestroyBody(e.body)
            e.body = None

    def remove_all_entities(self):
        for b in self._world.bodies:
            b.userData.body = None
            self._world.DestroyBody(b)

    @property
    def dims(self):
        return self._dims

    def get_temperature(self, pos):
        return noise.snoise2(pos[0] / WORLD_TEMP_NOISE_SCALE, pos[1] / WORLD_TEMP_NOISE_SCALE, base=self._noise_seed,
                             octaves=2)

    def get_time(self):
        return self.time / 100

    def tick(self, dt):
        self.time += dt
        self.time = int(self.time) % 100

        # TODO iterations depend on fast forward?
        self._world.Step(dt, 2, 1)
