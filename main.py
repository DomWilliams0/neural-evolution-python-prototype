#!/usr/bin/python3

import math

import Box2D
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

        for e in simulator.entities:
            render_entity(e)

        simulator.world.world.DrawDebugData()

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

    # sensors
    for s in e.sensors:
        colour = (50, 140, 80)
        # TODO colour depends on type
        vertices = s.get_vertices(rel_angle=e.angle)
        vertices = (vertices[0] + e.pos, vertices[1] + e.pos)

        g.draw(2, g.GL_LINES,
               ("v2f", (*vertices[0], *vertices[1])),
               ("c3B", (*colour, *colour))
               )

    # debug draw velocity
    vel_end = inter_pos[0] + e.velocity[0], inter_pos[1] + e.velocity[1]
    g.draw(2, g.GL_LINES,
           ("v2f", (inter_pos[0], inter_pos[1], vel_end[0], vel_end[1])),
           ("c3B", (255, 255, 255, 255, 255, 255))
           )


def render_world():
    for food in simulator.world.food:
        render_circle(*food.pos, food.radius, food.colour)


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


class PhysicsDebugRenderer(Box2D.b2Draw):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.AppendFlags(self.e_shapeBit)

    def DrawSolidCircle(self, center, radius, axis, color):
        render_circle(center[0], center[1], radius, color)

    def DrawSegment(self, p1, p2, color):
        g.draw(2, g.GL_LINES,
               ("v2f", (*p1, *p2)),
               ("c3f", (*color, *color))
               )

    def DrawCircle(self, center, radius, color):
        print("DrawCircle")

    def DrawPolygon(self, vertices, vertexCount, color):
        print("DrawPolygon")

    def DrawSolidPolygon(self, vertices, vertexCount, color):
        print("DrawSolidPolygon")

    def DrawTransform(self, xf):
        print("DrawTransform")


if RENDER_DEBUG_PHYSICS:
    simulator.world.world.renderer = PhysicsDebugRenderer()


def main():
    Renderer().run()


if __name__ == "__main__":
    main()
