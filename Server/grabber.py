from point import Point, Waypoint


class Grabber:
    def __init__(self, corner_distance=0.0):
        self.is_open = False
        self.corner_distance = corner_distance
        self._location: Point | Waypoint = Point(0, 0, 0)
        self.corners: list[Point, ...] = []

    def _update_corners(self):
        if self.location is None:
            self.corners = [None] * 4
            return
        self.corners = [
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
        self._location = value
        self._update_corners()
