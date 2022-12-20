import json
import requests
import threading

IPS = ["192.168.1.64"]
ports = ["80"]
count = min(len(IPS), len(ports))  # Amount of clients to connect to

addresses = [f"{IPS[i]}:{ports[i]}" for i in range(min(len(IPS), len(ports)))]  # Create address based on ip and port


def send_request(address: str, subpage: str) -> bool:
    """
    Send request to one client, and return success as bool
    """
    try:
        response = requests.get("http://"+address+"/"+subpage).text
        print(response)
        print(json.loads(response))
    except requests.exceptions.InvalidSchema:
        raise
        return False
    return response.get("success", False)  # Return false if value is missing


if __name__ == "__main__":
    for address in addresses:
        print(send_request(address, "on"))
