import itertools

from entity import *
from world import *

ENTITY_COUNT = 20
SPEED_SCALE = 1

TIME_PER_GENERATION = 5
TOP_PROPORTION_TO_TAKE = 0.2

MUTATE_NORMAL_MEAN = 0  # middle value
MUTATE_NORMAL_SD = 0.2  # variation
MUTATE_WEIGHT_CHANCE = 0.25
FITNESS_FUNCTION = lambda e: e.world.is_inside(e)


class Simulator:
    def __init__(self, world_size, generation_size):
        self.world = World(world_size)
        self._entities = []

        self.gen_size = generation_size
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

            # collect top fittest and kill everyone
            n_to_take = round(self.gen_size * TOP_PROPORTION_TO_TAKE)
            fittest = list(itertools.islice(sorted(self.entities, key=FITNESS_FUNCTION, reverse=True), n_to_take))
            self.world.remove_all_entities()

            # take the best brains and mutate them
            self._entities = self.mutate_fittest(fittest)

        # tick entities as normal
        self.world.tick(step)
        for e in self.entities:
            e.tick()

    def mutate_fittest(self, fittest):
        """
        :param fittest: List of living Entities
        :return: A new generation of Entities
        """

        def mutate(what):
            for (val, indices) in net.iterate_weights(what):
                if np.random.rand() < MUTATE_WEIGHT_CHANCE:
                    continue

                (list_ref, i) = net.get_from_indices(what, indices)

                # normal distribution from ~-0.6 - ~0.6
                change = np.random.normal(loc=MUTATE_NORMAL_MEAN, scale=MUTATE_NORMAL_SD)
                list_ref[i] += change

            return what

        # none alive: random generation
        if not fittest:
            print("Everyone died!")
            return [Entity(self.world) for _ in range(self.gen_size)]

        cycle = itertools.cycle(fittest)
        return [
            Entity(self.world, weights=mutate(next(cycle).brain.weights)) for _ in range(self.gen_size)
        ]
