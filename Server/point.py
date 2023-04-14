from math import sqrt
class Point:
    """
    Point class is used to represent a point in 3D space.
    1 unit is equal to 10 cm.
    :param x: The x coordinate of the point.
    :param y: The y coordinate of the point.
    :param z: The z coordinate of the point.
    """

    def __init__(self, x: int | float, y: int | float, z: int | float):
        self.x = round(float(x), 1)
        self.y = round(float(y), 1)
        self.z = round(float(z), 1)

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

    def distance_to(self, other) -> float:
        """
        Calculates the distance between this point and another point.
        :param other: Point to calculate distance to.
        :return: The distance between the two points.
        """
        return abs(sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2))


class Waypoint(Point):
    """
    Waypoint class is used to represent a waypoint in 3D space.
    1 unit is equal to 10 cm.
    :param x: The x coordinate of the waypoint.
    :param y: The y coordinate of the waypoint.
    :param z: The z coordinate of the waypoint.
    :param name: The name of the waypoint.
    """

    def __init__(self, x: int | float, y: int | float, z: int | float, name: str):
        super().__init__(x, y, z)
        self.name = name

    def __repr__(self):
        return f"Waypoint({self.x}, {self.y}, {self.z}, {self.name})"

    def to_list(self) -> list:
        """
        Converts the waypoint to a list of its attributes.
        """
        return [self.x, self.y, self.z, self.name]

    @classmethod
    def from_point(cls, point: Point, name: str):
        """
        Creates a waypoint from a point and a name.
        :param point: The point to create the waypoint from.
        :param name: The name of the waypoint.
        """
        return cls(point.x, point.y, point.z, name)

    @classmethod
    def from_list(cls, lst: list):
        """
        Creates a waypoint from a list of its attributes.
        :param lst: The list of attributes.
        """
        return cls(*lst)

    @classmethod
    def waypoints_from_2d_list(cls, list2d: list):
        """
        Creates a list of waypoints from a 2D list of their attributes.
        :param list2d: The 2D list of attributes.
        """
        return [cls.from_list(lst) for lst in list2d]
