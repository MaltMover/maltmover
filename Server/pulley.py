from point import Point


class Pulley:
    """
    Pulley class is used to represent a pulley with a location in 3D space.
    """

    def __init__(self, location: Point, max_length: int | float, max_speed: int | float, acceleration: int | float):
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
        self.acceleration = round(float(acceleration), 2)  # in decimeters per second squared (10 cm/s^2)
        self.speed = 0  # in decimeters per second (10 cm/s)
        self.length = 0  # in decimeters (10 cm)

    def __repr__(self):
        return f'Pulley(Location: ({self.x}, {self.y}, {self.z}), length: {self.length},' \
               f' Max length: {self.max_length} dm, Max speed: {self.max_speed} dm/s)'

    def __lt__(self, other):
        return self.location < other.location

    def set_length(self, length: int | float) -> float:
        """
        Sets the length of the rope attached to the pulley.
        :param length: The new length of the rope attached to the pulley.
        :return: The minimum time needed to change the length of the rope.
        """
        if length > self.max_length:
            raise ValueError(f'Length cannot be greater than {self.max_length} dm.')
        time = abs(self.length - length) / self.max_speed
        self.length = round(float(length), 2)
        return time

    def set_speed(self, speed: int | float):
        """
        Sets the speed of the pulley.
        :param speed: The new speed of the pulley.
        """
        if speed > self.max_speed:
            raise ValueError(f'Speed cannot be greater than {self.max_speed} dm/s.')
        self.speed = round(float(speed), 2)

    def set_time(self, time: int | float):
        """
        Sets the speed of the pulley, given the time to move.
        :param time: The new time of the pulley.
        """


def main():
    pulley = Pulley(Point(0, 0, 0), 10, 10)
    print(pulley)


if __name__ == '__main__':
    main()
