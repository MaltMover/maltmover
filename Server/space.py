from point import Point
from pulley import Pulley

from math import sqrt, ceil


class Space:
    def __init__(self, size_x: int | float, size_y: int | float, size_z: int | float, edge_limit: int | float = 0):
        self.size_x = round(float(size_x), 1)  # in decimeter (10 cm)
        self.size_y = round(float(size_y), 1)  # in decimeter (10 cm)
        self.size_z = round(float(size_z), 1)  # in decimeter (10 cm)
        self.edge_limit = round(float(edge_limit), 1)  # in decimeter (10 cm)
        self.pulleys = []  # List of pulleys in the space

    def __repr__(self) -> str:
        return f'Space(({self.size_x}, {self.size_y}, {self.size_z}), Pulleys: {len(self.pulleys)})'

    def is_in_space(self, point: Point, check_limit=True) -> bool:
        """
        Checks if the point is in the space.
        :param point: Point to check
        :param check_limit: If True, checks if the point is within the edge_limit
        :return: True if the point is in the space, False otherwise
        """
        if check_limit:
            limit = self.edge_limit
        else:
            limit = 0

        if not limit < point.x < self.size_x - limit:
            return False
        if not limit < point.y < self.size_y - limit:
            return False
        if not limit < point.z < self.size_z - limit:
            return False
        return True

    def add_pulley(self, pulley: Pulley) -> None:
        self.pulleys.append(pulley)
        self.pulleys = sorted(self.pulleys)

    def update_lengths(self, point: Point, time: int | float) -> None:
        """
        Updates the lengths of the ropes of the pulleys in the space.
        Raises ValueError if the point is not in the space.
        Raises ValueError if the time results in speed higher than a pulley max_speed.
        """
        if not self.is_in_space(point):
            raise ValueError(f'{point} is not within limits of the {self}')
        for pulley in self.pulleys:
            new_length = sqrt((pulley.x - point.x) ** 2 + (pulley.y - point.y) ** 2 + (pulley.z - point.z) ** 2)
            pulley.set_length(new_length, time)

    def calculate_min_time(self, target: Point) -> float:
        """
        Calculates the minimum time it takes to move from current position to target point, given the max_speed of the pulleys.
        :return: time in seconds, rounded to 2 decimal places
        """
        min_time = -1
        for pulley in self.pulleys:
            end_length = sqrt((pulley.x - target.x) ** 2 + (pulley.y - target.y) ** 2 + (pulley.z - target.z) ** 2)
            pulley_time = abs(pulley.length - end_length) / pulley.max_speed
            if pulley_time > min_time:
                min_time = pulley_time

        return ceil(min_time * 100) / 100
