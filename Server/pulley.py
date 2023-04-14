from point import Point

import json
from math import sqrt


class Pulley:
    """
    Pulley class is used to represent a pulley with a location in 3D space.
    :param location: The location of the pulley in 3D space.
    :param max_length: The length of the rope attached to the pulley.
    :param max_speed: The maximum velocity of the pulley.
    """

    def __init__(
        self,
        location: Point,
        max_length: int | float,
        max_speed: int | float,
        max_acceleration: int | float,
    ):
        self.location = location
        self.max_length = round(float(max_length), 2)  # in decimeters (10 cm)
        self.max_speed = round(float(max_speed), 2)  # in decimeters per second (10 cm/s)
        self.max_acceleration = round(
            float(max_acceleration), 2
        )  # in dm per second squared (10 cm/s^2)
        self._length = 0  # in decimeters (10 cm)
        self._speed = 0  # in decimeters per second (10 cm/s)
        self._acceleration = 0  # in decimeters per second squared (10 cm/s^2)

    def __repr__(self):
        return (
            f"Pulley(Location: ({self.location}), length: {self.length}, "
            f"Max speed: {self.max_speed} dm/s, Speed: {self._speed})"
        )

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
            # Error if the length is greater than the maximum length
            raise ValueError(f"Length cannot be greater than {self.max_length} dm.")
        self._length = round(float(length), 2)

    @speed.setter
    def speed(self, speed: int | float):
        """
        Sets the speed of the pulley.
        :param speed: The new speed of the pulley.
        """
        if speed > self.max_speed:
            # Error if the speed is greater than the maximum speed
            raise ValueError(f"Speed cannot be greater than {self.max_speed} dm/s.")
        self._speed = round(float(speed), 2)

    @acceleration.setter
    def acceleration(self, acceleration: int | float):
        """
        Sets the acceleration of the pulley.
        :param acceleration: The new acceleration of the pulley.
        """
        if acceleration > self.max_acceleration:
            # Error if the acceleration is greater than the maximum acceleration
            raise ValueError(f"Acceleration cannot be greater than {self.max_acceleration} dm/s^2.")
        self._acceleration = round(float(acceleration), 2)

    def make_move(self, target: Point, time: int | float) -> tuple:
        """
        Makes a move with the pulley, and calculates the new speed and acceleration,
        based on the input time.
        :param target: The target location of the pulley.
        :param time: The time it should take to reach the target location.
        :return: The new speed and acceleration of the pulley.
        """
        with open("config.json", "r") as f:
            # Load the length offset from the config file
            length_offset = json.load(f)["length_offset"]
        target_length = self.location.distance_to(target) - length_offset
        move_size = abs(target_length - self.length)  # Direction is not important
        if target_length > self.max_length:
            # Can't move if the target length is greater than the maximum length
            raise ValueError(f"Length cannot be greater than {self.max_length} dm.")
        if time <= 0 and move_size != 0:
            # It is impossible to move in 0 seconds.
            raise ValueError(f"Time must be greater than 0.")

        # Calculate the new speed with cool math
        self.speed = (
            -(sqrt(self.max_acceleration * (self.max_acceleration * time**2 - 4 * move_size)) - self.max_acceleration * time) / 2
        )
        # The acceleration is always the maximum acceleration
        self.acceleration = self.max_acceleration
        self.length = target_length  # Update length

        return self.speed, self.acceleration  # Return the new speed and acceleration
