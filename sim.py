import itertools

from entity import *
from world import *

FITNESS_FUNCTION = lambda e: not e.world.is_inside(e)


class Simulator:
    def __init__(self):
        self.world = World(WORLD_SIZE)
        self._entities = self.world.entities

        self.gen_time = 0
        self.gen_no = 0

    @property
    def entities(self):
        return filter(lambda e: e.alive, self._entities)

    def tick(self, step):
        self.gen_time -= step

        # new generation
        if self.gen_time < 0:
            # reset clock
            self.gen_time = TIME_PER_GENERATION

            self.gen_no += 1
            print("Creating generation {}".format(self.gen_no))

            # collect role models
            n_to_take = round(GENERATION_SIZE * TOP_PROPORTION_TO_TAKE)
            fittest_entities = itertools.islice(sorted(self.entities, key=FITNESS_FUNCTION, reverse=True), n_to_take)

            # extract their brains and throw away the rest
            fittest_brains = [e.brain for e in fittest_entities]
            self.world.reset()

            # mutate the juicy brains
            self._entities.clear()
            self._entities.extend(self.mutate_fittest(fittest_brains))

        # tick entities as normal
        self.world.tick(step)
        for e in self.entities:
            e.tick()

    def mutate_fittest(self, brains):
        """
        :param brains: List of brains
        :return: A generator of the new generation of Entities
        """

        def random_pos():
            return (
                np.random.randint(ENTITY_RADIUS, WORLD_SIZE[0] - ENTITY_RADIUS - ENTITY_RADIUS),
                np.random.randint(ENTITY_RADIUS, WORLD_SIZE[1] - ENTITY_RADIUS - ENTITY_RADIUS)
            )

        # none alive: random generation
        if not brains:
            print("Everyone died!")
            yield from iter(self.world.create_entity(pos=random_pos()) for _ in range(GENERATION_SIZE))

        cycle = itertools.cycle(brains)
        for _ in range(GENERATION_SIZE):
            src_brain = next(cycle)
            new_brain = src_brain.copy_and_mutate()
            yield self.world.create_entity(pos=random_pos(), brain=new_brain)
