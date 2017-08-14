import math

import Box2D
import numpy as np


def vec_from_degrees(deg, length):
    direction_rad = np.deg2rad(deg)
    return Box2D.b2Vec2(
        length * math.cos(direction_rad),
        length * math.sin(direction_rad)
    )
