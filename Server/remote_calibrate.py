from rich import pretty
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt, IntPrompt, Confirm
from time import sleep
import json
import requests


class App:
    def __init__(self):
        self.console = Console()
        self.config: dict = {}
        self.target_length = -1

    def read_config(self) -> dict:
        with open("config.json", "r") as f:
            self.config = json.load(f)
        return self.config

    def write_config(self) -> None:
        with open("config.json", "w") as f:
            json.dump(self.config, f, indent=4)

    def setup(self) -> None:
        self.read_config()
        pretty.install()

    def show_start_page(self):
        self.console.clear()
        choice = IntPrompt.ask("Pulley number", choices=["0", "1", "2", "3"], console=self.console)
        self.show_target_page(choice)

    def show_target_page(self, pulley_num: int):
        head = f"""
        Pulley {pulley_num}
        IP: {self.config["ips"][pulley_num]}
        steps_pr_dm: {self.config["steps_pr_dm"][pulley_num]}
        """
        self.console.clear()
        self.console.rule()
        self.console.print(head)
        self.console.rule()
        self.target_length = FloatPrompt.ask("Target length \[dm]", console=self.console)
        self.show_calibrate_page(pulley_num)

    def show_calibrate_page(self, pulley_num: int):
        head = f"""
        Pulley {pulley_num}
        IP: {self.config["ips"][pulley_num]}
        steps_pr_dm: {self.config["steps_pr_dm"][pulley_num]}
        Target length: {self.target_length} dm
        """
        self.console.clear()
        self.console.rule()
        self.console.print(head)
        self.console.rule()
        choice = FloatPrompt.ask("Change by how much?", default=0.1, console=self.console)
        self.update_pulley(pulley_num, self.target_length, choice)
        self.show_confirm(pulley_num)

    def show_confirm(self, pulley_num: int):
        self.console.rule()
        prompt = f"Is the pulley at {self.target_length} dm?"
        if Confirm.ask(prompt, default=False, console=self.console):
            self.update_pulley(pulley_num, 0)
            self.show_start_page()
        self.show_calibrate_page(pulley_num)

    def update_pulley(self, pulley_num: int, target_length: float, step_change=0.0):
        self.config["steps_pr_dm"][pulley_num] += step_change
        self.config["steps_pr_dm"][pulley_num] = round(self.config["steps_pr_dm"][pulley_num], 4)
        data = {"acceleration": 0.4, "speed": 0.8, "length": target_length}
        uri = "http://" + self.config["ips"][pulley_num]
        res1 = requests.post(uri, json={"steps_pr_dm": self.config["steps_pr_dm"][pulley_num]})
        res2 = requests.post(uri, json=data)
        res3 = requests.post(uri, json={"run": True})


if __name__ == "__main__":
    app = App()
    app.setup()
    try:
        app.show_start_page()
    except KeyboardInterrupt:
        app.console.print("Exiting...")
    app.write_config()
