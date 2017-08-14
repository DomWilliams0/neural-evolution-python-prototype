import math

import pyglet
import pyglet.graphics as g

from sim import Simulator
from config import *

# TODO add toggle for fast forward

simulator = Simulator()

class Renderer(pyglet.window.Window):
    def __init__(self):
        super().__init__(*WORLD_SIZE)
        self.running = True

        # background colour
        pyglet.graphics.glClearColor(0.05, 0.05, 0.07, 1)
        if RENDER_TEMPERATURE:
            self.world_temp_backdrop = prerender_world_temp()

        self.total_ticks = 0
        self.get_tick_count()  # ticks clock

    def get_tick_count(self):
        self.total_ticks += pyglet.clock.tick()
        return self.total_ticks

    def run(self):
        while self.running:
            # TODO improve this (in a way that actually works)
            #   i.e. render up to a maximum frame rate and tick multiple times before rendering
            dt = pyglet.clock.tick()
            simulator.tick(dt * SPEED_SCALE)
            self.render()

            self.dispatch_events()

    def render(self):
        self.clear()

        if RENDER_TEMPERATURE:
            self.world_temp_backdrop.draw()

        render_world()

        # TODO use interpolation?
        for e in simulator.entities:
            render_entity(e)

        self.flip()

    def on_key_press(self, symbol, mod):
        global SPEED_SCALE

        if symbol == pyglet.window.key.ESCAPE:
            self.running = False

        # TODO improve this mess
        elif symbol == pyglet.window.key.K:
            SPEED_SCALE += 1
            print("Speed:", SPEED_SCALE)
        elif symbol == pyglet.window.key.J:
            SPEED_SCALE -= 1
            print("Speed:", SPEED_SCALE)
        elif symbol == pyglet.window.key.SPACE:
            SPEED_SCALE = 1
            print("Speed reset")


def render_circle(x, y, radius, colour):
    """https://gist.github.com/tsterker/1396796"""
    iterations = int(2 * radius * math.pi)
    s = math.sin(2 * math.pi / iterations)
    c = math.cos(2 * math.pi / iterations)

    dx, dy = radius, 0

    g.glBegin(g.GL_TRIANGLE_FAN)
    g.glColor3f(*colour)
    g.glVertex2f(x, y)
    for i in range(iterations + 1):
        g.glVertex2f(x + dx, y + dy)
        dx, dy = (dx * c - dy * s), (dy * c + dx * s)
    g.glEnd()


def render_entity(e):
    # inter_pos = (
    #     self.pos[0] + self.body.velocity[0] * interpolation,
    #     self.pos[1] + self.body.velocity[1] * interpolation
    # )
    inter_pos = e.pos
    render_circle(*inter_pos, e.RADIUS, e.colour)

    # debug draw velocity
    vel_end = inter_pos[0] + e.velocity[0], inter_pos[1] + e.velocity[1]
    g.draw(2, g.GL_LINES,
           ("v2f", (inter_pos[0], inter_pos[1], vel_end[0], vel_end[1])),
           ("c3B", (255, 255, 255, 255, 255, 255))
           )


def render_world():
    colour = (0.8, 0.3, 0.2)
    for (dz_centre, dz_radius) in simulator.world.death_zones:
        render_circle(dz_centre[0], dz_centre[1], dz_radius, colour)


def prerender_world_temp():
    world = simulator.world
    dims = world.dims
    batch = pyglet.graphics.Batch()
    print("Rendering temperature texture")
    for y in range(dims[1]):
        for x in range(dims[0]):
            val = world.get_temperature((x, y))
            colour = (val, val, val)
            batch.add(1, pyglet.gl.GL_POINTS, None, ("v2i", (x, y)), ("c3f", colour))

    return batch


def main():
    Renderer().run()


if __name__ == "__main__":
    main()
