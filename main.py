import pyglet

from entity import *
from world import *

WORLD_SIZE = (600, 600)
ENTITY_COUNT = 50

# sim
world = World(WORLD_SIZE)
entities = [Entity(world) for _ in range(ENTITY_COUNT)]


def tick_sim(step):
    world.tick(step)
    for e in entities:
        e.tick()


# renderer
TICKS_PER_SECOND = 20
SKIP_TICKS = 1 / TICKS_PER_SECOND
MAX_FRAMESKIP = 5


class Renderer(pyglet.window.Window):
    def __init__(self):
        super().__init__(*WORLD_SIZE)
        self.running = True

        # background colour
        pyglet.graphics.glClearColor(0.05, 0.05, 0.07, 1)

        self.total_ticks = 0
        self.get_tick_count()  # ticks clock

    def get_tick_count(self):
        self.total_ticks += pyglet.clock.tick()
        return self.total_ticks

    def run(self):
        next_tick = self.get_tick_count()

        while self.running:
            loops = 0
            while self.get_tick_count() > next_tick and loops < MAX_FRAMESKIP:
                tick_sim(SKIP_TICKS)

                next_tick += SKIP_TICKS
                loops += 1

            interpolation = float(self.get_tick_count() + SKIP_TICKS - next_tick) / SKIP_TICKS
            self.render(interpolation)
            self.dispatch_events()

    def render(self, interpolation):
        self.clear()

        for e in entities:
            e.render(interpolation)

        self.flip()

    def on_key_press(self, symbol, mod):
        if symbol == pyglet.window.key.ESCAPE:
            self.running = False


if __name__ == "__main__":
    Renderer().run()
