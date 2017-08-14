import itertools

from config import *
from entity import *
from world import *

FITNESS_FUNCTION = lambda e: not e.world.is_inside(e)


class Simulator:
    def __init__(self):
        self.world = World(WORLD_SIZE)
        self._entities = []

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
            n_to_take = round(GENERATION_SIZE * TOP_PROPORTION_TO_TAKE)
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
        :return: A generator of the new generation of Entities
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
            return [Entity(self.world) for _ in range(GENERATION_SIZE)]

        cycle = itertools.cycle(fittest)
        new_gen = []
        for _ in range(GENERATION_SIZE):
            src_brain = next(cycle).brain
            new_weights = mutate(src_brain.weights)
            new_biases = mutate(src_brain.biases)
            entity = Entity(self.world, weights=new_weights, biases=new_biases)
            new_gen.append(entity)
        return new_gen
