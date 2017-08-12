

class World:
    def __init__(self, dims):
        self._dims = dims
        # TODO time and noise

    @property
    def dims(self):
        return self._dims
