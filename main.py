import math

import pyglet
import pyglet.graphics as g

from config import *
from sim import Simulator

# TODO add toggle for fast forward

simulator = Simulator()


class Renderer(pyglet.window.Window):
    def __init__(self):
        super().__init__(*WINDOW_SIZE)
        self.running = True

        self.current_generation = None
        self.generation_label = pyglet.text.Label()

        self.ticker = None
        self.toggle_fast_forward()  # sets ticker

        # background colour
        pyglet.graphics.glClearColor(0.05, 0.05, 0.07, 1)
        if RENDER_TEMPERATURE:
            self.world_temp_backdrop = prerender_world_temp()

    def update_generation_label(self):
        cur = simulator.gen_no
        if cur != self.current_generation:
            self.current_generation = cur
            self.generation_label.text = "Generation {:04}".format(simulator.gen_no)

    def _tick(self, mult=1):
        dt = pyglet.clock.tick()
        simulator.tick(dt * mult)
        self.update_generation_label()

    def tick_and_render(self):
        self._tick()
        self.render_simulator()

    def tick_only(self):
        self._tick(mult=FAST_FORWARD_SCALE)
        self.render_fast_forwarding()

    def toggle_fast_forward(self):
        if self.ticker == self.tick_and_render:
            self.ticker = self.tick_only
            self.generation_label.x = WINDOW_SIZE[0] / 2
            self.generation_label.y = WINDOW_SIZE[1] / 2
            self.generation_label.font_size = 16
            self.generation_label.anchor_x = "center"
            self.generation_label.anchor_y = "center"
        else:
            self.ticker = self.tick_and_render
            self.generation_label.x = 5
            self.generation_label.y = 5
            self.generation_label.font_size = 10
            self.generation_label.anchor_x = "left"
            self.generation_label.anchor_y = "bottom"

    def run(self):
        while self.running:
            self.ticker()
            self.dispatch_events()

    def render_simulator(self):
        self.clear()

        if RENDER_TEMPERATURE:
            self.world_temp_backdrop.draw()

        render_world()

        # TODO use interpolation?
        for e in simulator.entities:
            render_entity(e)

        self.generation_label.draw()

        self.flip()

    def render_fast_forwarding(self):
        self.clear()
        self.generation_label.draw()
        self.flip()

    def on_key_press(self, symbol, mod):
        if symbol == pyglet.window.key.ESCAPE:
            self.running = False

        elif symbol == pyglet.window.key.SPACE:
            self.toggle_fast_forward()


_CIRCLE_ITERATIONS = 10
_CIRCLE_S = math.sin(2 * math.pi / _CIRCLE_ITERATIONS)
_CIRCLE_C = math.cos(2 * math.pi / _CIRCLE_ITERATIONS)


def render_circle(x, y, radius, colour):
    """https://gist.github.com/tsterker/1396796"""

    dx, dy = radius, 0

    g.glBegin(g.GL_TRIANGLE_FAN)
    g.glColor3f(*colour)
    g.glVertex2f(x, y)
    for i in range(_CIRCLE_ITERATIONS + 1):
        g.glVertex2f(x + dx, y + dy)
        dx, dy = (dx * _CIRCLE_C - dy * _CIRCLE_S), (dy * _CIRCLE_C + dx * _CIRCLE_S)
    g.glEnd()


def render_entity(e):
    # inter_pos = (
    #     self.pos[0] + self.body.velocity[0] * interpolation,
    #     self.pos[1] + self.body.velocity[1] * interpolation
    # )
    inter_pos = e.pos
    render_circle(*inter_pos, ENTITY_RADIUS, e.colour)

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
