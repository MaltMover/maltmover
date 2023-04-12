class FakePulley:
    def __init__(self):
        self.length = 0.0
        self.prep_length = -1
        self.speed = 0
        self.acceleration = 0

    def __str__(self):
        return f"FakePulley(length={self.length}, prep_length={self.prep_length})"

    def get_response(self, data: dict) -> dict:
        if "length" in data and "speed" in data and "acceleration" in data:
            if not data["speed"] or not data["acceleration"]:  # If speed or acceleration is 0
                return {"success": False}
            self.prep_length = data["length"]
            self.speed = data["speed"]
            self.acceleration = data["acceleration"]
        elif "run" in data:
            if self.prep_length == -1:  # If length is not set
                return {"success": False}
            if data["run"]:
                self.length = self.prep_length
                self.prep_length = -1
            else:
                self.prep_length = -1

        elif "get_length" in data:
            return {"success": True, "length": self.length}
        elif "steps_pr_dm" in data:
            print(f"Steps pr dm set to {data['steps_pr_dm']}")
            return {"success": True}
        else:
            return {"success": False}

        return {"success": True}
