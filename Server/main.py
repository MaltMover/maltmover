from point import Point
from pulley import Pulley
from space import Space

SIZE = [10, 10, 10]
MAX_SPEED = 10


def main():
    space = Space(10, 10, 10)
    space.add_pulley(Pulley(Point(0, 0, SIZE[2]), 10, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], 0, SIZE[2]), 10, MAX_SPEED))
    space.add_pulley(Pulley(Point(0, SIZE[1], SIZE[2]), 10, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], SIZE[1], SIZE[2]), 10, MAX_SPEED))
    print(space.pulleys)


if __name__ == '__main__':
    main()
