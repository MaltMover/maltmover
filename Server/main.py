from point import Point
from pulley import Pulley
from space import Space
from request_handler import RequestsHandler

# All measurements are in decimeters (10 cm)
SIZE = [10, 10, 10]
ROPE_LENGTH = 15
MAX_SPEED = 10

# Ips of the pulley-systems
IPS = (
    "192.168.1.64",
    "192.168.172.2",
    "192.168.172.3",
    "192.168.172.4"
)


def main():
    space = Space(*SIZE)
    space.add_pulley(Pulley(Point(0, 0, SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], 0, SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(0, SIZE[1], SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], SIZE[1], SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    target = Point(10, 10, SIZE[2])
    space.update_lengths(target, 2)
    for pulley in space.pulleys:
        print(pulley.length)
    requests_handler = RequestsHandler(IPS)
    print(requests_handler.set_pulleys(space.pulleys, 2))


if __name__ == '__main__':
    main()
