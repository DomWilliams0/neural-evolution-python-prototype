import pymunk

class World:
    def __init__(self, dims):
        self._dims = dims
        self.time = 0
        # TODO time and noise

        self.physics = pymunk.Space()
        self.physics.gravity = (0, 0)

    @property
    def dims(self):
        return self._dims

    def get_temperature(self, pos):
        # TODO noise
        import numpy
        return numpy.random.rand()

    def get_time(self):
        return (self.time % 100) / 100.0

    def tick(self, dt):
        self.time += 1
        self.physics.step(dt)
