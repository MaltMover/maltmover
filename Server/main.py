from point import Point
from pulley import Pulley
from space import Space
from request_handler import RequestHandler
from GUI import App
import json

with open("config.json", "r") as f:
    config = json.loads(f.read())

# All measurements are in decimeters (10 cm)
SIZE = config["size"]
ROPE_LENGTH = config["rope_length"]
MAX_SPEED = config["max_speed"]
EDGE_LIMIT = config["edge_limit"]  # How close to the edge of the space, the object can be

# Ips of the pulley-systems
IPS = config["ips"]


def main():
    space = Space(*SIZE, edge_limit=EDGE_LIMIT)
    space.read_waypoints("waypoints.json")
    space.add_pulley(Pulley(Point(0, 0, SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], 0, SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(0, SIZE[1], SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    space.add_pulley(Pulley(Point(SIZE[0], SIZE[1], SIZE[2]), ROPE_LENGTH, MAX_SPEED))
    request_handler = RequestHandler(IPS)
    app = App(space, request_handler)
    app.mainloop()
    space.write_waypoints("waypoints.json")


if __name__ == '__main__':
    main()
