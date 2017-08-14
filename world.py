from collections import namedtuple
from enum import Enum

import noise
import numpy as np
from Box2D import *

from config import *


class EntityType(Enum):
    ENTITY = 1 << 1
    FOOD = 1 << 2
    FOOD_SENSOR = 1 << 3  # TODO generalise sensor type?


# handy
_ENTITY_AND_FOOD = EntityType.ENTITY.value | EntityType.FOOD.value
_FOOD_SENSOR = EntityType.FOOD.value | EntityType.FOOD_SENSOR.value

UserData = namedtuple("UserData", "entity type")


class Food:
    NEXT_ID = 0

    def __init__(self, world, pos):
        self.id = Food.NEXT_ID
        Food.NEXT_ID += 1

        # TODO move constants to config when final
        self.nutrition = np.random.randint(1, 4)
        self.colour = (0.1, 0.8, 0.4)

        self.world = world
        self.fixture = world.food_static_body.CreateCircleFixture(radius=self.nutrition * 2,
                                                                  pos=pos,
                                                                  isSensor=True,
                                                                  userData=UserData(self, EntityType.FOOD))

    def on_eat(self, _entity):
        # entity takes nutrition itself
        self.world.remove_food(self)

    @property
    def pos(self):
        return self.fixture.shape.pos

    @property
    def radius(self):
        return self.fixture.shape.radius


class FoodContactListener(b2ContactListener):
    def BeginContact(self, contact):
        a = contact.fixtureA.userData
        b = contact.fixtureB.userData

        # or the types together
        col_type = a.type.value | b.type.value

        # entity eating food
        if col_type == _ENTITY_AND_FOOD:
            a.entity.on_eat(b.entity)
            b.entity.on_eat(a.entity)


class World:
    def __init__(self, dims):
        self._dims = dims
        self.time = 0
        self._noise_seed = np.random.randint(1000000)  # bah why not

        self._world = b2World(gravity=(0, 0), contactListener=FoodContactListener())
        self.food_static_body = self._world.CreateStaticBody()
        self._dead_food = []
        self._food = {}
        self.last_food = 0

        self.reset()

    def _add_random_food(self):
        pos = (
            np.random.randint(self._dims[0]),
            np.random.randint(self._dims[1])
        )
        f = Food(self, pos)
        self._food[f.id] = f

    def remove_food(self, food):
        # check not already eaten
        if food.fixture is not None:
            self._dead_food.append(food.fixture)
            food.fixture = None
            self._food.pop(food.id, None)

    def is_inside(self, e):
        pos = e.pos
        rad = ENTITY_RADIUS / 2
        return rad <= pos[0] < self.dims[0] - rad and rad <= pos[1] < self.dims[1] - rad

    def add_entity(self, e):
        e.body = self._world.CreateDynamicBody()
        e.body.CreateCircleFixture(radius=ENTITY_RADIUS, userData=UserData(e, EntityType.ENTITY))

    def remove_entity(self, e):
        if e.body:
            self._world.DestroyBody(e.body)
            e.body = None

    def reset(self):
        # remove all dynamic bodies
        for b in self._world.bodies:
            if b.type == b2_dynamicBody:
                self._world.DestroyBody(b)

        # remove all food
        for food in self.food:
            self.food_static_body.DestroyFixture(food.fixture)
        self._food.clear()

        # reset food timers
        self.last_food = INITIAL_FOOD_SIMULATION

    def create_entity_sensor(self, e, vertices, sensor_type):
        e.body.CreateEdgeFixture(vertices=vertices, isSensor=False, userData=UserData(e, sensor_type))

    @property
    def dims(self):
        return self._dims

    @property
    def food(self):
        return self._food.values()

    def get_temperature(self, pos):
        return noise.snoise2(pos[0] / WORLD_TEMP_NOISE_SCALE, pos[1] / WORLD_TEMP_NOISE_SCALE,
                             base=self._noise_seed,
                             octaves=2)

    def get_time(self):
        return self.time / 100

    def tick(self, dt):
        self.time += dt
        self.time = int(self.time) % 100

        # TODO iterations depend on fast forward?
        self._world.Step(dt, 2, 1)

        # remove all dead food that couldn't be removed in callback
        # TODO and dead entities? only when they're killed in a collision callback
        for f in self._dead_food:
            self.food_static_body.DestroyFixture(f)
        self._dead_food.clear()

        # add new food
        if KEEP_SPAWNING_FOOD:
            self.last_food += dt
        while self.last_food >= FOOD_RATE:
            self.last_food -= FOOD_RATE
            self._add_random_food()
