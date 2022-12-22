from point import Point
from pulley import Pulley
from space import Space
from request_handler import RequestsHandler
import json

with open("config.json", "r") as f:
    config = json.loads(f.read())

# All measurements are in decimeters (10 cm)
SIZE = config["size"]
ROPE_LENGTH = config["rope_length"]
MAX_SPEED = config["max_speed"]

# Ips of the pulley-systems
IPS = config["ips"]


def main():
    space = Space(*SIZE)
    space.add_pulley(Pulley(Point(0, 0, SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], 0, SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(0, SIZE[1], SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], SIZE[1], SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    target = Point(10, 10, SIZE[2])
    time = space.calculate_min_time(target)
    print(f"Time: {time}s")
    space.update_lengths(target, time)
    for pulley in space.pulleys:
        print(pulley)
    requests_handler = RequestsHandler(IPS)
    print(requests_handler.set_pulleys(space.pulleys, time))


if __name__ == '__main__':
    main()
