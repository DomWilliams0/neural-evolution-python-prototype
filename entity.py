import numpy as np
from pymunk.vec2d import Vec2d

import net


class Entity:
    RADIUS = 8
    MAX_FORCE = 60
    NEXT_ID = 1

    def __init__(self, world, weights=None):
        self.id = Entity.NEXT_ID
        Entity.NEXT_ID += 1

        self.alive = True

        self.world = world

        # random position
        dims = world.dims
        # padding = Entity.RADIUS * 5
        # self.pos = (
        #     padding + np.random.rand() * (dims[0] - padding * 2),
        #     padding + np.random.rand() * (dims[1] - padding * 2)
        # )
        self.pos = (dims[0] / 2, dims[1] / 2)
        self.velocity = Vec2d()

        # physics
        world.add_entity(self)

        # 2 inputs, 2 outputs
        self.brain = net.Network([2, 4, 5, 2], weights=weights)

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
        speed = outputs[0][0] * Entity.MAX_FORCE
        direction = outputs[1][0] * 360.0

        steer = Vec2d(0, -1)
        steer.angle_degrees = direction
        steer *= (speed, speed)

        # self.body.apply_impulse_at_local_point(steer)
        self.velocity = steer

        # print("{} | speed {:.4f} direction={:.4f}".format(self.id, speed, direction))

    def kill(self, remove_from_world=True):
        if self.alive:
            self.alive = False
            if remove_from_world:
                self.world.remove_entity(self)
