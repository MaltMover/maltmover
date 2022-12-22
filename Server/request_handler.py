from pulley import Pulley
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
    def __init__(self, addresses: tuple[str, ...] | list[str, ...]):
        self.addresses = addresses
        self.threads = []
        self.response_count = 0
        self.success_map = [  # Stores boolean map of success for each request
            [False for _ in range(len(self.addresses))],
            [False for _ in range(len(self.addresses))]
        ]

    def __repr__(self):
        return f"RequestsHandler{self.addresses}"

    def set_pulleys(self, pulleys: list[Pulley], time: int | float) -> list[list[bool]]:
        if len(pulleys) != len(self.addresses):
            raise ValueError("Number of pulleys must equal number of addresses")
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
        if not self.send_requests(data, request_num=0):
            return self.success_map

        # If all succeeded, send second request to all pulleys
        self.send_requests([{"Run": True}] * len(self.addresses), request_num=1)
        return self.success_map

    def send_requests(self, data: list[dict], timeout: int | float = 3, request_num=-1) -> bool:
        self.response_count = 0
        # Reset success map, all False
        self.success_map = [
            [False for _ in range(len(self.addresses))],
            [False for _ in range(len(self.addresses))]
        ]

        # Create one thread for each client
        pulley_num = 0
        for address, d in zip(self.addresses, data):
            self.threads.append(threading.Thread(target=self.send_request, args=(address, d, timeout, request_num, pulley_num)))
            pulley_num += 1

        # Start all threads
        for thread in self.threads:
            thread.start()

        # Wait for all threads to finish
        while not self.response_count == len(self.addresses):
            sleep(0.1)

        # Join all threads
        for thread in self.threads:
            thread.join()
        self.threads = []

        # Check if all requests were successful
        return all(self.success_map[request_num])

    def send_request(self, address: str, data: dict, timeout: int | float, request_num, pulley_num) -> bool:
        """
        Send request to one client, and return success as bool
        """
        try:
            response = requests.post(f"http://{address}/", json=data, timeout=timeout)
        except (requests.exceptions.InvalidSchema, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            self.response_count += 1
            return False
        self.response_count += 1
        if response.status_code == 200:
            self.success_map[request_num][pulley_num] = True
            return True
        return False


if __name__ == "__main__":
    handler = RequestsHandler(IPS)
    print(handler)
