from grabber import Grabber
from point import Point, Waypoint
from pulley import Pulley

import json
from math import sqrt, ceil


class Space:
    def __init__(
            self,
            size_x: int | float,
            size_y: int | float,
            size_z: int | float,
            edge_limit: int | float = 0,
            grabber: Grabber = None,
    ):
        self.size_x = round(float(size_x), 1)  # in decimeter (10 cm)
        self.size_y = round(float(size_y), 1)  # in decimeter (10 cm)
        self.size_z = round(float(size_z), 1)  # in decimeter (10 cm)
        self.center = Point(self.size_x / 2, self.size_y / 2, self.size_z / 2)
        self.current_point = Point(0, 0, 0)
        self.edge_limit = round(float(edge_limit), 1)  # in decimeter (10 cm)
        self.grabber = None  # Grabber object
        self.pulleys = []  # List of pulleys in the space
        self.waypoints = []  # List of waypoints in the space

    def __repr__(self) -> str:
        return f"Space(({self.size_x}, {self.size_y}, {self.size_z}), Pulleys: {len(self.pulleys)})"

    def read_waypoints(self, path: str) -> None:
        """
        Reads waypoints from a file.
        :param path: Path to the file
        """
        with open(path, "r") as f:
            self.waypoints = Waypoint.waypoints_from_2d_list(json.load(f))

    def write_waypoints(self, path: str) -> None:
        """
        Writes waypoints to a file.
        :param path: Path to the file
        """
        with open(path, "w") as f:
            json.dump([waypoint.to_list() for waypoint in self.waypoints], f, indent=2)

    def is_in_space(self, point: Point | Waypoint, check_limit=True) -> bool:
        """
        Checks if the point is in the space.
        :param point: Point to check
        :param check_limit: If True, checks if the point is within the edge_limit
        :return: True if the point is in the space, False otherwise
        """
        if check_limit:
            limit = self.edge_limit
        else:
            limit = 0

        if not limit <= point.x <= self.size_x - limit:
            return False
        if not limit <= point.y <= self.size_y - limit:
            return False
        if not limit <= point.z <= self.size_z - limit:
            return False
        return True

    def is_legal_point(self, point: Point | Waypoint) -> bool:
        """
        Checks if the point is in space, and doesn't require a longer rope than possible.
        :param point: Point to check
        :return: True if the point is legal, False otherwise
        """
        if not self.is_in_space(point):
            return False
        for pulley in self.pulleys:
            new_length = sqrt((pulley.x - point.x) ** 2 + (pulley.y - point.y) ** 2 + (pulley.z - point.z) ** 2)
            if new_length > pulley.max_length:
                return False
        return True

    def add_pulley(self, pulley: Pulley) -> None:
        self.pulleys.append(pulley)
        self.pulleys = sorted(self.pulleys)

    def set_grabber(self, grabber: Grabber) -> None:
        self.grabber = grabber

    def update_lengths(self, point: Point | Waypoint, check_limit=True) -> None:
        """
        Updates the lengths of the ropes of the pulleys in the space.
        Raises ValueError if the point is not in the space.
        Raises ValueError if the time results in speed higher than a pulley max_speed.
        """
        if not self.is_in_space(point, check_limit=check_limit):
            raise ValueError(f"{point} is not within limits of the {self}")
        times = []
        for pulley in self.pulleys:
            new_length = sqrt((pulley.x - point.x) ** 2 + (pulley.y - point.y) ** 2 + (pulley.z - point.z) ** 2)
            times.append(pulley.set_length(new_length))
        slow_time = max(times)  # Time of the slowest pulley

        self.current_point = point
        print(self.current_point)

    def calculate_min_move_time(self, target: Point, three_point_move=False) -> float:
        """
        Calculates the minimum time it takes to move from current position to target point, given the max_speed of the pulleys.
        :param target: Target point
        :param three_point_move: If True, calculates the time for a three-point move
        :return: time in seconds, rounded to 2 decimal places
        """
        with open("config.json", "r") as f:
            config = json.load(f)
        if three_point_move:
            delay = config["three_point_delay"]
            t1 = self.calculate_min_move_time(
                Point(self.current_point.x, self.current_point.y, self.size_z - self.edge_limit)
            )
            t2 = self.calculate_min_move_time(Point(target.x, target.y, self.size_z - self.edge_limit))
            t3 = self.calculate_min_move_time(Point(target.x, target.y, target.z))
            time = t1 + t2 + t3 + (delay * 2)
            return ceil(time * 100) / 100  # Round up to 2 decimal places
        min_time = -1
        for pulley in self.pulleys:
            end_length = sqrt((pulley.x - target.x) ** 2 + (pulley.y - target.y) ** 2 + (pulley.z - target.z) ** 2)
            move_size = abs(pulley.length - end_length)
            pulley_time = self.calculate_move_time(move_size, pulley.max_speed, pulley.max_acceleration)
            if pulley_time > min_time:
                min_time = pulley_time

        return ceil(min_time * 100) / 100  # Round up to 2 decimal places

    @staticmethod
    def calculate_move_time(move_length: float, speed: float, acceleration: float) -> float:
        """
        Calculates the time it takes to move a certain distance at a certain speed with a certain acceleration
        :param move_length: The length to move
        :param speed: The speed to move at
        :param acceleration: The acceleration to use
        :return: The time it takes to move the length
        """
        time_to_max_speed = speed / acceleration  # Time to reach max speed
        distance_to_max_speed = 0.5 * acceleration * time_to_max_speed ** 2  # Distance travelled to reach max speed
        if distance_to_max_speed * 2 > move_length:  # If it is not possible to reach max speed
            return ((move_length / acceleration) ** 0.5) * 2  # Time formula (t = sqrt(2 * d / a))
        max_speed_move_time = (move_length - distance_to_max_speed * 2) / speed  # Time spent at max speed
        return 2 * time_to_max_speed + max_speed_move_time  # Times two because it has to break as well


def create_space(current_point: Point = None):
    with open("config.json", "r") as f:
        config = json.load(f)

    size = config["size"]
    rope_length = config["rope_length"]
    max_speed = config["max_speed"]
    max_acceleration = config["max_acceleration"]
    edge_limit = config[
        "edge_limit"
    ]  # How close to the edge of the space, the object can be

    space = Space(*size, edge_limit=edge_limit)
    space.read_waypoints("waypoints.json")
    space.add_pulley(Pulley(Point(0, 0, size[2]), rope_length, max_speed, max_acceleration))
    space.add_pulley(Pulley(Point(size[0], 0, size[2]), rope_length, max_speed, max_acceleration))
    space.add_pulley(Pulley(Point(0, size[1], size[2]), rope_length, max_speed, max_acceleration))
    space.add_pulley(Pulley(Point(size[0], size[1], size[2]), rope_length, max_speed, max_acceleration))
    grabber = Grabber()
    space.set_grabber(grabber)
    if current_point:
        space.update_lengths(current_point, check_limit=False)
    return space
