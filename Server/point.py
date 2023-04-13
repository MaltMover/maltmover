from math import sqrt
class Point:
    """
    Point class is used to represent a point in 3D space.
    1 unit is equal to 10 cm.
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
        return abs(sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2))


class Waypoint(Point):
    def __init__(self, x: int | float, y: int | float, z: int | float, name: str):
        super().__init__(x, y, z)
        self.name = name

    def __repr__(self):
        return f"Waypoint({self.x}, {self.y}, {self.z}, {self.name})"

    def to_list(self) -> list:
        return [self.x, self.y, self.z, self.name]

    @classmethod
    def from_point(cls, point: Point, name: str):
        return cls(point.x, point.y, point.z, name)

    @classmethod
    def from_list(cls, lst: list):
        return cls(lst[0], lst[1], lst[2], lst[3])

    @classmethod
    def waypoints_from_2d_list(cls, list2d: list):
        return [cls.from_list(lst) for lst in list2d]


def main():
    import json
    p0 = Point(0, 0, 0)
    p1 = Point(1, 0, 0)
    p2 = Point(0, 1, 0)
    p3 = Point(1, 1, 0)
    print(sorted([p1, p3, p2, p0]))
    w0 = Waypoint.from_point(p0, "Start")
    w1 = Waypoint.from_list([4.0, 13.0, 12.0, "Den gode"])
    w2 = Waypoint(1, 2, 3, "End")
    print(w0)
    print(w1)
    print(w2)
    with open("waypoints.json", "r") as f:
        waypoints = Waypoint.waypoints_from_2d_list(json.load(f))
    print(waypoints)
    print(json.dumps([w.to_list() for w in waypoints], indent=4))


if __name__ == "__main__":
    main()
