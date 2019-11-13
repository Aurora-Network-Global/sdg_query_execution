import math

import numpy as np


class Point:

    def __init__(self, x, y):
        self._point = np.array([x, y])

    def to_string(self):
        return str(self._point[0]) + ', ' + str(self._point[1])

    def rotate(self, angle):
        rotation_matrix = np.array([[math.cos(angle), -1*math.sin(angle)], [math.sin(angle), math.cos(angle)]])
        self._point = rotation_matrix.dot(self._point)
        return self._point

    def polar_shift(self, angle, amount):
        shift_vector = amount * np.array([math.cos(angle), math.sin(angle)])
        self._point = self._point + shift_vector
        return self._point

    def cartesian_shift(self, delta_x, delta_y):
        self._point = self._point + np.array([delta_x, delta_y])
        return self._point

