import pyglet

from entity import *
from world import *

# sim
world = World((600, 600))
entities = [Entity(world) for _ in range(50)]

# renderer
window = pyglet.window.Window(*world.dims)


def tick(dt):
    world.tick(dt)
    for e in entities:
        e.tick(dt)


@window.event
def on_draw():
    window.clear()

    for e in entities:
        e.render()


def main():
    # schedule update
    pyglet.clock.schedule_interval(tick, 1 / 20)

    # background colour
    pyglet.graphics.glClearColor(0.05, 0.05, 0.07, 1)

    pyglet.app.run()


if __name__ == "__main__":
    main()
