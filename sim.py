from entity import *
from world import *

ENTITY_COUNT = 50
SPEED_SCALE = 1


class Simulator:
    def __init__(self, world_size, entity_count):
        self.world = World(world_size)
        self.entities = [Entity(self.world) for _ in range(entity_count)]

    def tick(self, step, speed_scale):
        for _ in range(speed_scale):
            self.world.tick(step)
            for e in self.entities:
                e.tick()
