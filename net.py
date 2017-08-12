import numpy as np


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


class Network:
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feed_forward(self, inputs):
        outputs = inputs
        for b, w in zip(self.biases, self.weights):
            outputs = sigmoid(np.dot(w, outputs) + b)
        return outputs
