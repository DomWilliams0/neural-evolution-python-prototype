import numpy.random as rand

class Entity:
    RADIUS = 2
    MAX_FORCE = 3

    def __init__(self, world):
        self.world = world

        # random position
        dims = world.dims
        self.pos = (
            rand.rand() * (dims[0] - Entity.RADIUS),
            rand.rand() * (dims[1] - Entity.RADIUS)
        )

        # 2 outputs
        self.outputs = rand.rand(2)

    def tick(self):
        # random on off input
        if rand.rand() < 0.5:
            outputs = self.outputs
        else:
            outputs = (0, 0)


        # convert outputs
        speed = outputs[0] * Entity.MAX_FORCE
        direction = outputs[1] * 360.0

        print("{} {}".format(speed, direction))
