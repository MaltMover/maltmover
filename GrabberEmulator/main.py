from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import threading

from app import App
from fake_grabber import FakeGrabber


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
        print("Receive: ", post_data, "\n")
        response = FG.get_response(post_data)
        APP.update_values()

        self._set_response()
        self.wfile.write(json.dumps(response).encode("utf-8"))  # Send response


def run_server():
    global HTTPD
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    server_address = ("", port)
    HTTPD = HTTPServer(server_address, TestHTTPHandler)
    print("Starting server")
    HTTPD.serve_forever()


def start_server():
    global server_thread
    server_thread.start()


def main():
    global APP
    start_server()
    APP.mainloop()
    HTTPD.shutdown()
    server_thread.join(2)


if __name__ == "__main__":
    HTTPD: HTTPServer = None
    server_thread = threading.Thread(target=run_server)
    FG = FakeGrabber()
    APP = App(FG)
    main()
