class FakePulley:
    def __init__(self):
        self.length = 0.0
        self.prep_length = 0.0
        self.prep_time = -1

    def __str__(self):
        return f"FakePulley(length={self.length}, prep_length={self.prep_length}, prep_time={self.prep_time})"

    def get_response(self, data: dict) -> dict:
        if "length" in data and "time" in data:
            self.prep_length = data["length"]
            self.prep_time = data["time"]
            return {"success": True}
        elif "run" in data:
            if data["run"]:
                self.length = self.prep_length
                self.prep_length = 0.0
                self.prep_time = -1
                return {"success": True}
        elif "send_length" in data:
            return {"success": True, "length": self.length}
        return {"success": False}
