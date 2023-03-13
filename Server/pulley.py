from point import Point

import json
from math import sqrt


class Pulley:
    """
    Pulley class is used to represent a pulley with a location in 3D space.
    """

    def __init__(self, location: Point, max_length: int | float, max_speed: int | float, max_acceleration: int | float):
        """
        :param location: The location of the pulley in 3D space.
        :param max_length: The length of the rope attached to the pulley.
        :param max_speed: The maximum velocity of the pulley.
        """
        self.location = location
        self.x = location.x
        self.y = location.y
        self.z = location.z
        self.max_length = round(float(max_length), 2)  # in decimeters (10 cm)
        self.max_speed = round(float(max_speed), 2)  # in decimeters per second (10 cm/s)
        self.max_acceleration = round(float(max_acceleration), 2)  # in decimeters per second squared (10 cm/s^2)
        self._length = 0  # in decimeters (10 cm)
        self._speed = 0  # in decimeters per second (10 cm/s)
        self._acceleration = 0  # in decimeters per second squared (10 cm/s^2)

    def __repr__(self):
        return f'Pulley(Location: ({self.x}, {self.y}, {self.z}), length: {self.length},' \
               f' Max length: {self.max_length} dm, Max speed: {self.max_speed} dm/s)'

    def __lt__(self, other):
        return self.location < other.location

    @property
    def length(self) -> float:
        return self._length

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def acceleration(self) -> float:
        return self._acceleration

    @length.setter
    def length(self, length: int | float):
        """
        Sets the length of the rope attached to the pulley.
        :param length: The new length of the rope attached to the pulley.
        """
        if length > self.max_length:
            raise ValueError(f'Length cannot be greater than {self.max_length} dm.')
        self._length = round(float(length), 2)

    @speed.setter
    def speed(self, speed: int | float):
        """
        Sets the speed of the pulley.
        :param speed: The new speed of the pulley.
        """
        if speed > self.max_speed:
            raise ValueError(f'Speed cannot be greater than {self.max_speed} dm/s.')
        self._speed = round(float(speed), 2)

    @acceleration.setter
    def acceleration(self, acceleration: int | float):
        """
        Sets the acceleration of the pulley.
        :param acceleration: The new acceleration of the pulley.
        """
        if acceleration > self.max_acceleration:
            raise ValueError(f'Acceleration cannot be greater than {self.max_acceleration} dm/s^2.')
        self._acceleration = round(float(acceleration), 2)

    def make_move(self, target: Point, time: int | float) -> tuple:
        """
        Makes a move with the pulley, and calculates the new speed and acceleration.
        :param target: The new rope length.
        :param time: The time to move.
        """
        with open("config.json", "r") as f:
            config = json.load(f)
            length_offset = config["length_offset"]
        new_length = self.location.distance_to(target) - length_offset
        move_size = abs(new_length - self.length)
        if new_length > self.max_length:
            raise ValueError(f'Length cannot be greater than {self.max_length} dm.')
        if time <= 0 and move_size != 0:
            raise ValueError(f'Time must be greater than 0.')

        # Calculate the new speed with cool math
        self.speed = -(sqrt(self.max_acceleration * (self.max_acceleration * time ** 2 - 4 * move_size)) - self.max_acceleration * time) / 2
        self.acceleration = self.max_acceleration
        self.length = new_length

        return self.speed, self.acceleration


def main():
    pulley = Pulley(Point(0, 0, 0), max_length=50, max_speed=10, max_acceleration=2)
    print(pulley)
    print(pulley.make_move(50, 12.5))
    print(pulley.make_move(50, 10))
    print(pulley.make_move(50, 20))
    print(pulley.make_move(12.5, 5))


if __name__ == '__main__':
    main()
