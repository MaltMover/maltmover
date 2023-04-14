from grabber import Grabber
from point import Point, Waypoint
from pulley import Pulley

import json
from math import ceil


class Space:
    """
    Space class represents the space in which the robot can move.
    :param: size_x: The size of the space in the x direction.
    :param: size_y: The size of the space in the y direction.
    :param: size_z: The size of the space in the z direction.
    :param: edge_limit: The distance from the edge of the space in which the robot cannot move. Default is 0.
    :param: grabber: The grabber object, default is None.
    """

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
        self.edge_limit = round(float(edge_limit), 1)  # in decimeter (10 cm)
        self.grabber: Grabber | None = grabber  # Grabber object
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
            # Convert from json to list of lists, and parse to Waypoint constructor
            self.waypoints = Waypoint.waypoints_from_2d_list(json.load(f))

    def write_waypoints(self, path: str) -> None:
        """
        Writes waypoints to a file.
        :param path: Path to the file
        """
        with open(path, "w") as f:
            # Convert to list of lists, and write to file
            json.dump([waypoint.to_list() for waypoint in self.waypoints], f, indent=4)

    def is_in_space(self, point: Point | Waypoint, check_limit=True) -> bool:
        """
        Checks if the point is in the space.
        :param point: Point to check
        :param check_limit: If True, checks if the point is within the edge_limit
        :return: True if the point is in the space, False otherwise
        """
        # Set limit to 0 if check_limit is False
        limit = self.edge_limit if check_limit else 0

        if not limit <= point.x <= self.size_x - limit:  # Doesn't allow touching walls
            return False
        if not limit <= point.y <= self.size_y - limit:  # Doesn't allow touching walls
            return False
        if not 0 <= point.z <= self.size_z - limit:  # Allow touching floor but not ceiling
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
        # Create a temporary grabber object to check if the point is legal
        grabber = Grabber(corner_distance=self.grabber.corner_distance)
        # Set the location of the grabber to the point, so that the corners are calculated
        grabber.location = point
        for i, pulley in enumerate(self.pulleys):
            # Check if the distance to the corresponding corner is longer than the max_length
            if pulley.location.distance_to(grabber.corners[i]) > pulley.max_length:
                return False
        return True

    def add_pulley(self, pulley: Pulley) -> None:
        """
        Adds a pulley to the space and sorts the pulleys by their location.
        :param pulley: Pulley object to add
        :return: None
        """
        self.pulleys.append(pulley)
        self.pulleys = sorted(self.pulleys)

    def set_grabber(self, grabber: Grabber) -> None:
        """
        Sets the grabber of the space.
        :param grabber: New grabber object
        :return: None
        """
        self.grabber = grabber

    def move_grabber(self, target: Point | Waypoint, check_limit=True) -> float:
        """
        Updates the lengths of the ropes of the pulleys in the space.
        Raises ValueError if the target is not in the space.
        Raises ValueError if the time results in speed higher than a pulley max_speed.
        :return: Time to make the move in seconds
        """
        if not self.is_in_space(target, check_limit=check_limit):
            # If the target is not in the space, raise ValueError
            raise ValueError(f"{target} is not within limits of the {self}")

        min_time = self.calculate_min_move_time(target)

        self.grabber.location = target  # Updates the corner locations of the grabber
        for i, pulley in enumerate(self.pulleys):
            # Move pulley to respective corner of the grabber
            pulley.make_move(self.grabber.corners[i], min_time)

        print(self.grabber.location)
        return min_time

    def calculate_min_move_time(self, target: Point, three_point_move=False, origin=None) -> float:
        """
        Calculates the minimum time it takes to move the slowest pulley from current position (or another origin) to target point,
         using the max_speed and max_acceleration of the pulleys.
        :param target: Target point
        :param three_point_move: If True, calculates the time for a three-point move
        :param origin: Origin point for the move (default is the current location of the grabber)
        :return: time in seconds, rounded to 2 decimal places
        """
        with open("config.json", "r") as f:
            # Read config file
            config = json.load(f)
        current_point = self.grabber.location
        if three_point_move:
            delay = config["three_point_delay"]
            t1 = self.calculate_min_move_time(
                Point(current_point.x, current_point.y, self.size_z - self.edge_limit)
            )  # Ceiling above origin

            t2 = self.calculate_min_move_time(
                Point(target.x, target.y, self.size_z - self.edge_limit)
            )  # Ceiling above target

            t3 = self.calculate_min_move_time(target)  # Target
            time = t1 + t2 + t3 + (delay * 2)
            return ceil(time * 100) / 100  # Round up to 2 decimal places

        min_time = -1  # Any calculated time will be larger than this
        # Create grabber object for calculations
        grabber = Grabber(corner_distance=self.grabber.corner_distance)
        grabber.location = target  # Calculate corners of new target
        for i, pulley in enumerate(self.pulleys):
            # Length from pulley to the corresponding corner of the grabber
            end_length = pulley.location.distance_to(grabber.corners[i])
            if origin is None:
                # If no origin is given
                # pulley.length get offset subtracted, so we add it back
                start_length = pulley.length + config["length_offset"]
            else:
                # If origin is given, calculate the length from the origin to the pulley
                # This is done by creating a temporary grabber object at the origin
                origin_grabber = Grabber(corner_distance=self.grabber.corner_distance)
                origin_grabber.location = origin
                start_length = pulley.location.distance_to(origin_grabber.corners[i])

            move_size = abs(start_length - end_length)  # Abs value since direction doesn't matter
            # Calculate the time it takes to move the length
            pulley_time = self.calculate_move_time(move_size, pulley.max_speed, pulley.max_acceleration)
            if pulley_time > min_time:
                # Change min if the calculated time is larger
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
        distance_to_max_speed = 0.5 * acceleration * time_to_max_speed**2  # Distance travelled to reach max speed
        if distance_to_max_speed * 2 > move_length:  # If it is not possible to reach max speed
            return ((move_length / acceleration) ** 0.5) * 2  # Time formula (t = sqrt(2 * d / a))
        max_speed_distance = move_length - distance_to_max_speed * 2  # Distance travelled at max speed
        max_speed_move_time = max_speed_distance / speed  # Time spent at max speed
        return 2 * time_to_max_speed + max_speed_move_time  # Times two because it has to break as well


def create_space(current_point: Point = None) -> Space:
    """
    Creates a space object from the config file
    :param current_point: The current location of the grabber, defaults to None
    :return: Space object
    """
    with open("config.json", "r") as f:
        config = json.load(f)

    # Read values from config
    size = config["size"]
    rope_length = config["rope_length"]
    max_speed = config["max_speed"]
    max_acceleration = config["max_acceleration"]
    edge_limit = config["edge_limit"]  # How close to the edge of the space, the object can be

    space = Space(*size, edge_limit=edge_limit)  # Create space object
    space.read_waypoints("waypoints.json")  # Read waypoints from file
    # Add pulleys to the corners of the space
    space.add_pulley(Pulley(Point(0, 0, size[2]), rope_length, max_speed, max_acceleration))
    space.add_pulley(Pulley(Point(size[0], 0, size[2]), rope_length, max_speed, max_acceleration))
    space.add_pulley(Pulley(Point(0, size[1], size[2]), rope_length, max_speed, max_acceleration))
    space.add_pulley(Pulley(Point(size[0], size[1], size[2]), rope_length, max_speed, max_acceleration))
    grabber = Grabber(corner_distance=config["grabber_corner_distance"])  # Create grabber object
    space.set_grabber(grabber)  # Set grabber to space
    if current_point:
        # If a current point is given, move the grabber to that point
        space.move_grabber(current_point, check_limit=False)
    return space
