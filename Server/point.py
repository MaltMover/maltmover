class Point:
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
