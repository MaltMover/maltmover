from pulley import Pulley
import requests
import threading

import json
from time import sleep

IPS = (
    "192.168.172.1",
    "192.168.172.2",
    "192.168.172.3",
    "192.168.172.4"
)


class RequestHandler:
    def __init__(self, addresses: tuple[str, ...] | list[str, ...]):
        self.addresses = addresses
        self.threads = []
        self.response_count = 0
        self.responses = [{}] * len(self.addresses)
        self.success_map = [  # Stores boolean map of success for each request
            [False for _ in range(len(self.addresses))],
            [False for _ in range(len(self.addresses))]
        ]

    def __repr__(self):
        return f"RequestsHandler{self.addresses}"

    def get_lengths(self, timeout=3) -> tuple[list[float], list[bool]]:
        data = [{"send_length": True} for _ in range(len(self.addresses))]
        self.send_requests(data, request_num=0, timeout=timeout)
        lengths = [i["length"] if i else 0.0 for i in self.responses]
        return lengths, self.success_map[0]

    def reset_pulley(self, pulley_id: int):
        threading.Thread(target=self.send_reset_request, args=(pulley_id,)).start()

    def send_reset_request(self, pulley_id: int):
        address = self.addresses[pulley_id]
        with open("config.json", "r") as f:
            config = json.load(f)
            time = config["init_time"]
        data = {"length": 0.0, "time": time}
        self.send_request(address, data, timeout=3, request_num=0, pulley_num=pulley_id)
        self.send_request(address, {"run": True}, timeout=3, request_num=0, pulley_num=pulley_id)

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
            self.send_requests([{"run": False}] * len(self.addresses), request_num=1)
            return self.success_map

        # If all succeeded, send second request to all pulleys
        self.send_requests([{"run": True}] * len(self.addresses), request_num=1)
        return self.success_map

    def send_requests(self, data: list[dict], timeout: int | float = 3, request_num=-1) -> bool:
        self.threads = []
        self.response_count = 0
        self.responses = [""] * len(self.addresses)
        # Reset success map, for current and future requests
        self.success_map[request_num] = [False for _ in range(len(self.addresses))]
        if request_num < 1:
            self.success_map[1] = [False for _ in range(len(self.addresses))]

        # Create one thread for each client
        for address, d, pulley_num in zip(self.addresses, data, range(len(self.addresses))):
            self.threads.append(threading.Thread(target=self.send_request, args=(address, d, timeout, request_num, pulley_num)))

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
            print(response.text)
            self.responses[pulley_num] = response.json()
        except (requests.exceptions.InvalidSchema,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.JSONDecodeError,
                requests.exceptions.ReadTimeout) as e:
            print(e)
            self.response_count += 1
            return False
        self.response_count += 1
        if response.status_code == 200:
            self.success_map[request_num][pulley_num] = True
            return True
        return False


def create_request_handler():
    with open("config.json", "r") as f:
        config = json.load(f)

    ips = config["ips"]
    return RequestHandler(ips)


if __name__ == "__main__":
    handler = RequestHandler(IPS)
    print(handler)
