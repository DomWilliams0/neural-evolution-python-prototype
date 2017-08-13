import pyglet
from math import pi, cos, sin

from entity import *
from world import *

# sim
world = World((10, 10))
entities = [Entity(world) for _ in range(2)]

# renderer
window = pyglet.window.Window(600, 600)


def tick(dt):
    world.tick()
    for e in entities:
        e.tick(dt)


@window.event
def on_draw():
    def circle(x, y, radius):
        """https://gist.github.com/tsterker/1396796"""
        iterations = int(2*radius*pi)
        s = sin(2*pi / iterations)
        c = cos(2*pi / iterations)

        dx, dy = radius, 0

        pyglet.graphics.glBegin(pyglet.graphics.GL_TRIANGLE_FAN)
        pyglet.graphics.glVertex2f(x, y)
        for i in range(iterations+1):
            pyglet.graphics.glVertex2f(x+dx, y+dy)
            dx, dy = (dx*c - dy*s), (dy*c + dx*s)
        pyglet.graphics.glEnd()

    window.clear()

    for e in entities:
        circle(e.pos[0], e.pos[1], Entity.RADIUS)


def main():
    # schedule update
    pyglet.clock.schedule_interval(tick, 1 / 20)

    pyglet.app.run()


if __name__ == "__main__":
    main()
