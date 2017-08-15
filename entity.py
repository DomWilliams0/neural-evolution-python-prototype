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

    def __init__(self, world, body, pos=(0, 0), brain=None):
        """
        Shouldnt be used directly, use world.create_entity instead
        """
        self.id = Entity.NEXT_ID
        Entity.NEXT_ID += 1

        self.alive = True
        self.colour = ENTITY_DEFAULT_COLOUR

        self.world = world
        self.body = body
        self.pos = pos
        self.velocity = b2Vec2()

        self.sensors = []
        self._add_sensor(0.5, 0.25, EntityType.FOOD_SENSOR)  # 90 degrees on left

        self.total_food_eaten = 0
        self.cumulative_food = 0

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
        self.total_food_eaten += food.nutrition
        self.cumulative_food += food.nutrition
        print("{} ate {} food".format(self.id, food.nutrition))

        while self.cumulative_food > ENTITY_REPRODUCE_PER_N_FOOD:
            self.cumulative_food -= ENTITY_REPRODUCE_PER_N_FOOD

            child_brain = self.brain.copy_and_mutate()
            self.world.create_entity(instant=False, brain=child_brain, pos=self.pos)
            print("{} had a baby".format(self.id))

    def _add_sensor(self, len_float, angle_float, sensor_type):
        length = np.interp(len_float, (0, 1), SENSOR_LENGTH_LIMITS)
        angle = (angle_float * 360)
        sensor = Sensor(angle, length, sensor_type)

        vertices = sensor.get_vertices()
        self.world.create_entity_sensor(self, vertices, sensor_type)
        self.sensors.append(sensor)
