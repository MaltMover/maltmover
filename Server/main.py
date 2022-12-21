from point import Point
from pulley import Pulley
from space import Space

SIZE = [10, 10, 10]
MAX_SPEED = 10
ROPE_LENGTH = 10


def main():
    space = Space(*SIZE)
    space.add_pulley(Pulley(Point(0, 0, SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], 0, SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(0, SIZE[1], SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], SIZE[1], SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    print(space.pulleys)
    space.pulleys[0].set_length(50, 1)
    print(space.pulleys[0].length)


if __name__ == '__main__':
    main()
