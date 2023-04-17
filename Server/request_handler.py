from pulley import Pulley
import requests
import threading

import json
from time import sleep


class PulleyRequestHandler:
    """
    Handles requests to the pulleys.
    Uses multiple threads to send requests at the same time.
    :param addresses: Tuple of addresses of the pulleys.
    """
    def __init__(self, addresses: tuple[str, ...] | list[str, ...]):
        self.addresses = addresses  # Tuple of addresses of the pulleys
        self.threads = []  # List of currently running threads
        self.response_count = 0  # Number of responses received
        self.responses = [{}] * len(self.addresses)  # Stores responses from each request
        self.success_map = [  # Stores boolean map of success for each request
            [False for _ in range(len(self.addresses))],
            [False for _ in range(len(self.addresses))],
        ]

    def __repr__(self):
        return f"PulleyRequestsHandler{self.addresses}"

    def get_lengths(self, timeout=3) -> tuple[list[float], list[bool]]:
        """
        Gets the lengths of the ropes attached to the pulleys.
        :param timeout: The max time to wait for a response.
        :return:  A tuple containing a list of the lengths and a success map.
        """
        # Create data for each request
        data = [{"get_length": True} for _ in range(len(self.addresses))]
        # Send requests in parallel
        self.send_requests(data, request_num=0, timeout=timeout)
        # Set length 0 if no response
        lengths = [i["length"] if i else 0.0 for i in self.responses]
        return lengths, self.success_map[0]

    def set_steps_pr_dm(self, timeout=3) -> list[bool]:
        """
        Remotely sets the steps_pr_dm parameter for each pulley.
        :param timeout: Max time to wait for a response.
        :return: Success map.
        """
        with open("config.json", "r") as f:
            steps_pr_dm = json.load(f)["steps_pr_dm"]
        # Create data for each request
        data = [{"steps_pr_dm": steps} for steps in steps_pr_dm]
        # Send requests in parallel
        self.send_requests(data, request_num=0, timeout=timeout)
        return self.success_map[0]

    def reset_pulley(self, pulley_id: int) -> None:
        """
        Resets the pulley with the given id.
        :param pulley_id: The id of the pulley to reset.
        :return: None
        """
        threading.Thread(target=self.send_reset_request, args=(pulley_id,)).start()

    def send_reset_request(self, pulley_id: int) -> None:
        """
        Sends a reset request to the pulley with the given id.
        :param pulley_id: Pulley id to reset.
        :return: None
        """
        address = self.addresses[pulley_id]  # Get address of pulley
        with open("config.json", "r") as f:
            # Get speed and acceleration from config
            config = json.load(f)
            speed = config["init"]["speed"]
            acceleration = config["init"]["acceleration"]

        # Set the pulley to 5cm and configured speeds
        data = {"length": 0.5, "speed": speed, "acceleration": acceleration}
        # Send request, no need to check response
        self.send_request(address, data, timeout=3, request_num=0, pulley_num=pulley_id)
        self.send_request(address, {"run": True}, timeout=3, request_num=0, pulley_num=pulley_id)

    def set_pulleys(self, pulleys: list[Pulley]) -> list[list[bool]]:
        """
        Sets the pulleys to the given lengths, speeds and accelerations.
        :param pulleys: List of Pulley objects.
        :return: Success map.
        """
        if len(pulleys) != len(self.addresses):
            raise ValueError("Number of pulleys must equal number of addresses")
        data = []
        # Set data for each pulley
        for pulley in pulleys:
            data.append(
                {
                    "length": pulley.length,
                    "speed": pulley.speed,
                    "acceleration": pulley.acceleration,
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
        """
        Sends requests to all pulleys in parallel.
        :param data: List of dicts containing data for each request.
        :param timeout: Max time to wait for a response.
        :param request_num: 0 or 1, used to keep track of success map.
        :return: True if all requests succeeded, False otherwise.
        """
        self.threads = []
        self.response_count = 0
        self.responses = [""] * len(self.addresses)
        # Reset success map, for current and future requests
        self.success_map[request_num] = [False for _ in range(len(self.addresses))]
        if request_num < 1:
            # Reset success map for next request
            self.success_map[1] = [False for _ in range(len(self.addresses))]

        # Create one thread for each client
        for address, d, pulley_num in zip(self.addresses, data, range(len(self.addresses))):
            self.threads.append(
                threading.Thread(
                    target=self.send_request,
                    args=(address, d, timeout, request_num, pulley_num),
                )
            )

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

    def send_request(
            self,
            address: str,
            data: dict,
            timeout: int | float,
            request_num,
            pulley_num
    ) -> bool:
        """
        Send request to one client, and return success as bool
        :param address: Address of client.
        :param data: Data to send.
        :param timeout: Max time to wait for a response.
        :param request_num: 0 or 1, used to keep track of success map.
        :param pulley_num: Pulley number, used to keep track of success map.
        :return: True if request succeeded, False otherwise.
        """
        try:
            response = requests.post(f"http://{address}/", json=data, timeout=timeout)
            print(response.text)
            self.responses[pulley_num] = response.json()
        except (
            requests.exceptions.InvalidSchema,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.JSONDecodeError,
            requests.exceptions.ReadTimeout,
        ) as e:
            print(e)
            self.response_count += 1
            return False
        self.response_count += 1
        if response.status_code == 200:
            # Set success map
            self.success_map[request_num][pulley_num] = self.responses[pulley_num]["success"]
            return True
        return False


class GrabberRequestHandler:
    """
    Handles requests to the grabber.
    :param address: Address of grabber.
    """
    def __init__(self, address: str):
        self.address = address
        self.success = False
        self.response = {}

    def __repr__(self):
        return f"GrabberRequestHandler({self.address})"

    def get_state(self, timeout=3) -> bool:
        """
        Get the state of the grabber.
        :param timeout: Max time to wait for a response.
        :return: True if open, False if closed.
        """
        self.send_request({"get_state": True}, timeout=timeout)
        if self.success:
            return self.response["is_open"]

    def set_state(self, set_open: bool) -> None:
        """
        Set the state of the grabber.
        :param set_open: True to open, False to close.
        :return: None
        """
        self.send_request({"set_open": set_open})

    def send_request(self, data: dict, timeout=3) -> bool:
        """
        Send request to grabber.
        :param data: data to send.
        :param timeout: Max time to wait for a response.
        :return: True if request succeeded, False otherwise.
        """
        self.success = False
        try:
            response = requests.post(f"http://{self.address}/", json=data, timeout=timeout)
            self.response = response.json()
        except (
            requests.exceptions.InvalidSchema,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.JSONDecodeError,
            requests.exceptions.ReadTimeout,
        ) as e:
            print(e)
            return False
        if response.status_code == 200:
            self.success = True
            return True
        return False


def create_request_handler() -> PulleyRequestHandler:
    """
    Reads config and creates a PulleyRequestHandler.
    :return: PulleyRequestHandler object.
    """
    with open("config.json", "r") as f:
        config = json.load(f)

    ips = config["ips"]
    return PulleyRequestHandler(ips)


def create_grabber_handler() -> GrabberRequestHandler:
    """
    Reads config and creates a GrabberRequestHandler.
    :return: GrabberRequestHandler object.
    """
    with open("config.json", "r") as f:
        config = json.load(f)

    ip = config["grabber_ip"]
    return GrabberRequestHandler(ip)
