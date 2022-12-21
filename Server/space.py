from point import Point
from pulley import Pulley

from math import sqrt


class Space:
    def __init__(self, size_x: int | float, size_y: int | float, size_z: int | float):
        self.size_x = round(float(size_x), 1)  # in decimeter (10 cm)
        self.size_y = round(float(size_y), 1)  # in decimeter (10 cm)
        self.size_z = round(float(size_z), 1)  # in decimeter (10 cm)
        self.pulleys = []  # List of pulleys in the space

    def __repr__(self):
        return f'Space(({self.size_x}, {self.size_y}, {self.size_z}), Pulleys: {len(self.pulleys)})'

    def add_pulley(self, pulley: Pulley):
        self.pulleys.append(pulley)
        self.pulleys = sorted(self.pulleys)

    def update_lengths(self, point: Point, time: int | float):
        for pulley in self.pulleys:
            new_length = sqrt((pulley.x - point.x) ** 2 + (pulley.y - point.y) ** 2 + (pulley.z - point.z) ** 2)
            pulley.set_length(new_length, time)
