from point import Point, Waypoint


class Grabber:
    """
    Grabber class represent a grabber, with a location in space.
    :param corner_distance: Perpendicular distance from the center of the grabber
     to the corners (see README.md).
    """
    def __init__(self, corner_distance=0.0):
        self.is_open = False  # True if the grabber is open, False if it is closed
        self.corner_distance = corner_distance
        self.corners: list[Point, ...] = []  # The corners of the grabber
        self.location: Point | Waypoint = Point(0, 0, 0)  # The location of the grabber

    def _update_corners(self):
        """
        Updates the corner locations based on the location of the grabber.
        """
        if self.location is None:
            # If the location is None, set the corners to None
            self.corners = [None] * 4
            return
        self.corners = [  # Offset the corners based on their position relative to the center
            Point(self.location.x - self.corner_distance, self.location.y - self.corner_distance, self.location.z),
            Point(self.location.x + self.corner_distance, self.location.y - self.corner_distance, self.location.z),
            Point(self.location.x - self.corner_distance, self.location.y + self.corner_distance, self.location.z),
            Point(self.location.x + self.corner_distance, self.location.y + self.corner_distance, self.location.z)
        ]

    @property
    def location(self) -> Point | None:
        return self._location

    @location.setter
    def location(self, value: Point | None) -> None:
        """
        Sets the location of the grabber, and updates the corners.
        """
        self._location = value
        self._update_corners()
