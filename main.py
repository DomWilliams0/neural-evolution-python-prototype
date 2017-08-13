import pyglet

from entity import *
from world import *

WORLD_SIZE = (600, 600)
ENTITY_COUNT = 50
SPEED_SCALE = 1

# sim
world = World(WORLD_SIZE)
entities = [Entity(world) for _ in range(ENTITY_COUNT)]


def tick_sim(step):
    for x in range(SPEED_SCALE):
        world.tick(step)
        for e in entities:
            e.tick()


# renderer
TICKS_PER_SECOND = 20
SKIP_TICKS = 1 / TICKS_PER_SECOND
MAX_FRAMESKIP = 20


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

        # TODO use interpolation?
        for e in entities:
            e.render()

        self.flip()

    def on_key_press(self, symbol, mod):
        global SPEED_SCALE

        if symbol == pyglet.window.key.ESCAPE:
            self.running = False

        elif symbol == pyglet.window.key.K:
            SPEED_SCALE += 5
            print("Speed: ", SPEED_SCALE)
        elif symbol == pyglet.window.key.SPACE:
            SPEED_SCALE = 1
            print("Speed reset")


if __name__ == "__main__":
    Renderer().run()
