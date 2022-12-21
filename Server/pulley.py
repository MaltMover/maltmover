from point import Point


class Pulley:
    """
    Pulley class is used to represent a pulley with a location in 3D space.
    """

    def __init__(self, location: Point, length: int | float, max_speed: int | float):
        """
        :param location: The location of the pulley in 3D space.
        :param length: The length of the rope attached to the pulley.
        :param max_speed: The maximum velocity of the pulley.
        """
        self.location = location
        self.x = location.x
        self.y = location.y
        self.z = location.z
        self.length = round(float(length), 2)  # in decimeters (10 cm)
        self.max_speed = round(float(max_speed), 2)  # in decimeters per second (10 cm/s)


def main():
    pulley = Pulley(Point(0, 0, 0), 10, 10)
    print(pulley.location)
    print(pulley.length)
    print(pulley.max_speed)


if __name__ == '__main__':
    main()
