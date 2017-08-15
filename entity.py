from colorsys import hsv_to_rgb

import numpy as np
from Box2D import b2Vec2

import net
import util
from config import *
from world import EntityType


class Sensor:
    def __init__(self, angle, length, sensor_type):
        self.angle = angle
        self.length = length
        self.sensor_type = sensor_type

    def get_vertices(self, rel_angle=0):
        angle = self.angle + rel_angle
        sensor_direction = util.vec_from_degrees(angle)
        src = sensor_direction * ENTITY_RADIUS
        dst = sensor_direction * (ENTITY_RADIUS + self.length)
        return src, dst

class Entity:
    NEXT_ID = 1

    def __init__(self, world, brain=None):
        self.id = Entity.NEXT_ID
        Entity.NEXT_ID += 1

        self.alive = True
        self.colour = ENTITY_DEFAULT_COLOUR

        self.world = world
        self.body = None
        world.add_entity(self)

        self.sensors = []
        self._add_sensor(0.5, 0.25, EntityType.FOOD_SENSOR)  # 90 degrees on left

        dims = world.dims
        self.pos = (dims[0] / 2, dims[1] / 2)
        self.velocity = b2Vec2()

        # random position
        # padding = ENTITY_RADIUS * 5
        # self.pos = (
        #     padding + np.random.rand() * (dims[0] - padding * 2),
        #     padding + np.random.rand() * (dims[1] - padding * 2)
        # )

        if brain is None:
            self.brain = net.Network(NET_LAYERS)
        else:
            self.brain = brain

    @property
    def pos(self):
        return self.body.position

    @pos.setter
    def pos(self, val):
        self.body.position = val

    @property
    def velocity(self):
        return self.body.linearVelocity

    @velocity.setter
    def velocity(self, value):
        self.body.linearVelocity = value

    @property
    def angle(self):
        return np.rad2deg(self.body.angle)

    def tick(self):
        if not self.alive:
            return

        # get inputs
        temp = self.world.get_temperature(self.pos)
        time = self.world.get_time()

        # feed forward
        input_count = 2
        inputs = np.ndarray((input_count, 1))
        inputs[0] = temp
        inputs[1] = time
        outputs = self.brain.feed_forward(inputs)

        # convert outputs
        speed = outputs[0][0] * ENTITY_MAX_FORCE
        direction = outputs[1][0] * 360.0
        colour = hsv_to_rgb(outputs[2][0], 0.7, 0.7)

        self.velocity = util.vec_from_degrees(direction, speed)
        self.body.angle = np.deg2rad(direction)

        self.colour = colour

    def kill(self):
        if self.alive:
            self.alive = False
            self.world.remove_entity(self)

    def on_eat(self, food):
        # self.health += food.nutrition
        # TODO health
        print("{} ate {} food".format(self.id, food.nutrition))

    def _add_sensor(self, len_float, angle_float, sensor_type):
        length = np.interp(len_float, (0, 1), SENSOR_LENGTH_LIMITS)
        angle = (angle_float * 360)
        sensor = Sensor(angle, length, sensor_type)

        # TODO check rendering matches physical location
        vertices = sensor.get_vertices()
        self.world.create_entity_sensor(self, vertices, sensor_type)
        self.sensors.append(sensor)
