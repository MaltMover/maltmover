import json
import requests
import threading

from time import sleep

IPS = ["10.203.30.33", "10.203.30.30"]
ports = ["80", "80"]
count = min(len(IPS), len(ports))  # Amount of clients to connect to

addresses = [f"{IPS[i]}:{ports[i]}" for i in range(min(len(IPS), len(ports)))]  # Create address based on ip and port


def send_request(address: str, subpage: str) -> bool:
    """
    Send request to one client, and return success as bool
    """
    try:
        response = requests.get("http://"+address+"/"+subpage, timeout=1).text
        print(response)
        return response
        print(json.loads(response))
    except (requests.exceptions.InvalidSchema, requests.exceptions.ConnectTimeout):
        return False
    return response.get("success", False)  # Return false if value is missing


def send_requests(addresses: list, on: bool):
    threads = []
    for address in addresses:
        threads.append(threading.Thread(target=send_request, args=(address, "on" if on else "off")))
    for thread in threads:
        thread.start()
    sleep(1)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    while True:
        send_requests(addresses, True)
        sleep(1)
        send_requests(addresses, False)
        sleep(1)
