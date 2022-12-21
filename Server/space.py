from pulley import Pulley


class Space:
    def __init__(self, size_x: int | float, size_y: int | float, size_z: int | float):
        self.size_x = round(float(size_x), 1)  # in decimeter (10 cm)
        self.size_y = round(float(size_y), 1)  # in decimeter (10 cm)
        self.size_z = round(float(size_z), 1)  # in decimeter (10 cm)
        self.pulleys = []  # List of pulleys in the space

    def __repr__(self):
        return f'Space(({self.size_x}, {self.size_y}, {self.size_z}), Pulleys: {len(self.pulleys)})'

    def add_pulley(self, pulley: Pulley):
        self.pulleys.append(pulley)
        self.pulleys = sorted(self.pulleys)
