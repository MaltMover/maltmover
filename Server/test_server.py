from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class TestHTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_POST(self) -> None:
        """
        Handles POST requests
        """
        content_length = int(self.headers["Content-Length"])  # Gets the size of data
        post_data = self.rfile.read(content_length)  # Gets the data itself
        post_data = json.loads(post_data.decode("utf-8"))  # Parse as json
        response = FP.get_response(post_data)
        print(FP)

        self._set_response()
        self.wfile.write(json.dumps(response).encode("utf-8"))  # Send response


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


def main():
    server_address = ("", 80)
    httpd = HTTPServer(server_address, TestHTTPHandler)
    print("Starting server")
    httpd.serve_forever()


if __name__ == '__main__':
    FP = FakePulley()
    main()
