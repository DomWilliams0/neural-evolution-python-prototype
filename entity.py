import math
from colorsys import hsv_to_rgb

import numpy as np
from Box2D import b2Vec2

import net
from config import *


class Entity:
    NEXT_ID = 1

    def __init__(self, world, weights=None, biases=None):
        self.id = Entity.NEXT_ID
        Entity.NEXT_ID += 1

        self.alive = True
        self.colour = ENTITY_DEFAULT_COLOUR

        self.world = world
        self.body = None
        world.add_entity(self)

        dims = world.dims
        self.pos = (dims[0] / 2, dims[1] / 2)
        self.velocity = b2Vec2()

        # random position
        # padding = ENTITY_RADIUS * 5
        # self.pos = (
        #     padding + np.random.rand() * (dims[0] - padding * 2),
        #     padding + np.random.rand() * (dims[1] - padding * 2)
        # )

        self.brain = net.Network(NET_LAYERS, weights=weights, biases=biases)

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

        direction_rad = np.deg2rad(direction)
        self.velocity = b2Vec2(
            speed * math.cos(direction_rad),
            speed * math.sin(direction_rad)
        )

        self.colour = colour

    def kill(self, remove_from_world=True):
        if self.alive:
            self.alive = False
            if remove_from_world:
                self.world.remove_entity(self)
