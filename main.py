import math

import pyglet
import pyglet.graphics as g

from sim import Simulator

WORLD_SIZE = (600, 600)
ENTITY_COUNT = 10
SPEED_SCALE = 1

simulator = Simulator(WORLD_SIZE, ENTITY_COUNT)

# renderer
TICKS_PER_SECOND = 20
SKIP_TICKS = 1 / TICKS_PER_SECOND
MAX_FRAMESKIP = 20

# beware, very slow
RENDER_TEMPERATURE = False


class Renderer(pyglet.window.Window):
    def __init__(self):
        super().__init__(*WORLD_SIZE)
        self.running = True

        # background colour
        pyglet.graphics.glClearColor(0.05, 0.05, 0.07, 1)
        if RENDER_TEMPERATURE:
            self.world_temp_backdrop = render_world_temp()

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
                simulator.tick(SKIP_TICKS, SPEED_SCALE)

                next_tick += SKIP_TICKS
                loops += 1

            interpolation = float(self.get_tick_count() + SKIP_TICKS - next_tick) / SKIP_TICKS
            self.render(interpolation)
            self.dispatch_events()

    def render(self, interpolation):
        self.clear()

        if RENDER_TEMPERATURE:
            self.world_temp_backdrop.draw()

        # TODO use interpolation?
        for e in simulator.entities:
            render_entity(e)

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


def render_circle(x, y, radius):
    """https://gist.github.com/tsterker/1396796"""
    iterations = int(2 * radius * math.pi)
    s = math.sin(2 * math.pi / iterations)
    c = math.cos(2 * math.pi / iterations)

    dx, dy = radius, 0

    g.glBegin(g.GL_TRIANGLE_FAN)
    g.glColor3f(0.4, 0.6, 0.9)
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
    render_circle(*inter_pos, e.RADIUS)

    # debug draw velocity
    vel_end = inter_pos[0] + e.velocity[0], inter_pos[1] + e.velocity[1]
    g.draw(2, g.GL_LINES,
           ("v2f", (inter_pos[0], inter_pos[1], vel_end[0], vel_end[1])),
           ("c3B", (255, 255, 255, 255, 255, 255))
           )


def render_world_temp():
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
    # while simulator.gen_no < 1000:
    #     simulator.tick(10, 1)

    Renderer().run()

if __name__ == "__main__":
    main()
