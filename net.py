import copy

import numpy as np
from config import *


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


class Network:
    def __init__(self, sizes, weights=None, biases=None):
        self.num_layers = len(sizes)
        self.sizes = sizes

        if biases is None:
            self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        else:
            self.biases = copy.deepcopy(biases)

        if weights is None:
            self.weights = [np.random.randn(y, x)
                            for x, y in zip(sizes[:-1], sizes[1:])]
        else:
            self.weights = copy.deepcopy(weights)

    def feed_forward(self, inputs):
        outputs = inputs
        for b, w in zip(self.biases, self.weights):
            outputs = sigmoid(np.dot(w, outputs) + b)
        return outputs


    def copy_and_mutate(self):
        """
        :return: New mutated copy
        """
        new_weights = _mutate_array(self.weights)
        new_biases = _mutate_array(self.biases)
        return Network(self.sizes, weights=new_weights, biases=new_biases)


def _mutate_array(what):
    for (val, indices) in iterate_weights(what):
        if np.random.rand() < MUTATE_WEIGHT_CHANCE:
            continue

        (list_ref, i) = get_from_indices(what, indices)

        # normal distribution from ~-0.6 - ~0.6
        change = np.random.normal(loc=MUTATE_NORMAL_MEAN, scale=MUTATE_NORMAL_SD)
        list_ref[i] += change

    return what


def get_from_indices(x, indices):
    for i in indices[:-1]:
        x = x[i]
    return x, indices[-1]


def iterate_weights(layers):
    def recurse(weights, index):
        if len(weights.shape) == 1:
            for (i, x) in enumerate(weights):
                yield (x, index + [i])
        else:
            for (i, w) in enumerate(weights):
                yield from recurse(w, index + [i])

    for (i, weights) in enumerate(layers):
        yield from recurse(weights, [i])
