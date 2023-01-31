class FakePulley:
    def __init__(self):
        self.length = 0.0
        self.prep_length = 0.0
        self.prep_time = -1

    def __str__(self):
        return f"FakePulley(length={self.length}, prep_length={self.prep_length}, prep_time={self.prep_time})"

    def get_response(self, data: dict) -> dict:
        if "length" in data and "speed" in data:
            self.prep_length = data["length"]
            self.prep_time = round(self.prep_length / data["speed"], 2)
        elif "run" in data:
            if data["run"]:
                self.length = self.prep_length
                self.prep_length = 0.0
                self.prep_time = -1
            else:
                self.prep_length = self.length
                self.prep_time = -1
        elif "send_length" in data:
            return {"success": True, "length": self.length}
        else:
            return {"success": False}

        return {"success": True}
