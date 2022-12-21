from point import Point


class Pulley:
    """
    Pulley class is used to represent a pulley with a location in 3D space.
    """

    def __init__(self, location: Point, max_length: int | float, max_speed: int | float):
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

    def __repr__(self):
        return f'Pulley(Location: ({self.x}, {self.y}, {self.z}), Max length: {self.max_length} dm, Max speed: {self.max_speed} dm/s)'

    def __lt__(self, other):
        return self.location < other.location


def main():
    pulley = Pulley(Point(0, 0, 0), 10, 10)
    print(pulley)


if __name__ == '__main__':
    main()
