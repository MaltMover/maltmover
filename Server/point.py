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
        return f'Point({self.x}, {self.y}, {self.z})'

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


def main():
    p0 = Point(0, 0, 0)
    p1 = Point(1, 0, 0)
    p2 = Point(0, 1, 0)
    p3 = Point(1, 1, 0)
    print(sorted([p1, p3, p2, p0]))


if __name__ == '__main__':
    main()
