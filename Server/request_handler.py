from pulley import Pulley
import json
import requests
import threading

from time import sleep

IPS = (
    "192.168.172.1",
    "192.168.172.2",
    "192.168.172.3",
    "192.168.172.4"
)


class RequestsHandler:
    def __init__(self, addresses: tuple[str, ...]):
        self.addresses = addresses
        self.threads = []
        self.response_count = 0
        self.success_count = 0

    def __repr__(self):
        return f"RequestsHandler{self.addresses}"

    def set_pulleys(self, pulleys: list[Pulley], time: int | float) -> bool:
        data = []
        # Set data for each pulley
        for pulley in pulleys:
            data.append(
                {
                    "length": pulley.length,
                    "time": time
                }
            )
        # Send first request to all pulleys
        if not self.send_requests(data):
            return False

        # If all succeeded, send second request to all pulleys
        self.send_requests([{"Run": True}] * len(self.addresses))

    def send_requests(self, data: list[dict]):
        self.response_count = 0
        self.success_count = 0

        # Create one thread for each client
        for address, d in zip(self.addresses, data):
            self.threads.append(threading.Thread(target=self.send_request, args=(address, d)))

        # Start all threads
        for thread in self.threads:
            thread.start()

        # Wait for all threads to finish
        while self.response_count < len(self.addresses):
            sleep(0.1)

        # Join all threads
        for thread in self.threads:
            thread.join()
        self.threads = []

        # Check if all requests were successful
        return self.success_count == self.response_count == len(self.addresses)

    def send_request(self, address: str, data: dict) -> bool:
        """
        Send request to one client, and return success as bool
        """
        try:
            response = requests.post(f"http://{address}/", json=data, timeout=3)
        except (requests.exceptions.InvalidSchema, requests.exceptions.ConnectTimeout):
            self.response_count += 1
            return False
        self.response_count += 1
        if response.status_code == 200:
            self.success_count += 1
            return True
        return False


if __name__ == "__main__":
    handler = RequestsHandler(IPS)
    print(handler)
