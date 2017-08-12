class World:
    def __init__(self, dims):
        self._dims = dims
        self._time = 0
        # TODO time and noise

    @property
    def dims(self):
        return self._dims

    def get_temperature(self, pos):
        # TODO noise
        import numpy
        return numpy.random.rand()

    def get_time(self):
        return (self._time % 100) / 100.0

    def tick(self):
        self._time += 1
