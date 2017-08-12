import numpy as np

import net


class Entity:
    RADIUS = 2
    MAX_FORCE = 3

    def __init__(self, world):
        self.world = world

        # random position
        dims = world.dims
        self.pos = (
            np.random.rand() * (dims[0] - Entity.RADIUS),
            np.random.rand() * (dims[1] - Entity.RADIUS)
        )

        # 2 inputs, 2 outputs
        self.brain = net.Network([2, 2])

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

        print("speed={} direction={}".format(speed, direction))
