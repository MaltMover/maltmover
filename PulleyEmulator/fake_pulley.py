class FakePulley:
    def __init__(self):
        self.length = 0.0
        self.prep_length = 0.0
        self.speed = 0
        self.acceleration = 0

    def __str__(self):
        return f"FakePulley(length={self.length}, prep_length={self.prep_length})"

    def get_response(self, data: dict) -> dict:
        if "length" in data and "speed" in data and "acceleration" in data:
            self.prep_length = data["length"]
            self.speed = data["speed"]
            self.acceleration = data["acceleration"]
        elif "run" in data:
            if data["run"]:
                self.length = self.prep_length
            else:
                self.prep_length = self.length

        elif "get_length" in data:
            return {"success": True, "length": self.length}
        else:
            return {"success": False}

        return {"success": True}
