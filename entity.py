import numpy as np
import pymunk
from pymunk.vec2d import Vec2d

import net


class Entity:
    RADIUS = 8
    MAX_FORCE = 6
    NEXT_ID = 1

    def __init__(self, world):
        self.id = Entity.NEXT_ID
        Entity.NEXT_ID += 1

        self.world = world

        # random position
        dims = world.dims
        # padding = Entity.RADIUS * 5
        # pos = (
        #     padding + np.random.rand() * (dims[0] - padding * 2),
        #     padding + np.random.rand() * (dims[1] - padding * 2)
        # )
        pos = (dims[0] / 2, dims[1] / 2)

        # physics
        self.body = pymunk.Body(mass=1, moment=pymunk.moment_for_circle(1, 0, Entity.RADIUS))
        self.body.position = pos
        shape = pymunk.Circle(self.body, Entity.RADIUS)
        shape.friction = 0.9
        world.physics.add(self.body, shape)

        # 2 inputs, 2 outputs
        self.brain = net.Network([2, 2])

    @property
    def pos(self):
        return self.body.position

    @pos.setter
    def pos(self, pos):
        self.body.position = pos

    def tick(self):
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
        speed = outputs[0][0] * Entity.MAX_FORCE
        direction = outputs[1][0] * 360.0

        steer = Vec2d(0, -1)
        steer.angle_degrees = direction
        steer *= (Entity.MAX_FORCE * speed, Entity.MAX_FORCE * speed)

        # self.body.apply_impulse_at_local_point(steer)
        self.body.velocity = steer

        # print("{} | speed {:.4f} direction={:.4f}".format(self.id, speed, direction))
