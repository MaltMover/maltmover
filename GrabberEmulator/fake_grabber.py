class FakeGrabber:
    def __init__(self):
        self.is_open = False

    def __str__(self):
        return f"FakeGrabber(open={self.is_open})"

    def get_response(self, data: dict) -> dict:
        if "set_open" in data:
            self.is_open = bool(data["set_open"])
            return {"success": True, "is_open": self.is_open}
        elif "get_state" in data:
            return {"success": True, "is_open": self.is_open}
        else:
            return {"success": False}
