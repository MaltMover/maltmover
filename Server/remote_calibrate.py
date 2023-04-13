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
        """
        Read config.json into self.config
        :return: New value for self.config
        """
        with open("config.json", "r") as f:
            self.config = json.load(f)
        return self.config

    def write_config(self) -> None:
        """
        Write contents of self.config into config.json
        :return: None
        """
        with open("config.json", "w") as f:
            json.dump(self.config, f, indent=4)

    def setup(self) -> None:
        """
        Setup the program, installing pretty and reading the config
        :return: None
        """
        self.read_config()
        pretty.install()

    def show_start_page(self) -> None:
        """
        Show the start page. Select a pulley.
        :return: None
        """
        self.console.clear()
        choice = IntPrompt.ask("Pulley number", choices=["0", "1", "2", "3"], console=self.console)
        self.show_target_page(choice)

    def show_target_page(self, pulley_num: int) -> None:
        """
        Show page where target length is selected.
        :pulley_num: Int value of which pulley is selected
        :return: None
        """
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

    def show_calibrate_page(self, pulley_num: int) -> None:
        """
        Show the calibration page and data on the selected pulley.
        :pulley_num: Int value of which pulley is selected
        :return: None
        """
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
        success = self.update_pulley(pulley_num, self.target_length, choice)
        if success:
            self.show_confirm(pulley_num)
        else:
            self.console.clear()
            self.console.rule("Connection Error")
            sleep(1)
            self.show_calibrate_page(pulley_num)

    def show_confirm(self, pulley_num: int) -> None:
        """
        Ask user to confirm length of pulley. If not perfect, keep going.
        :pulley_num: Int value of which pulley is selected, only used if not perfect.
        :return: None
        """
        self.console.rule()
        prompt = f"Is the pulley at {self.target_length} dm?"
        if Confirm.ask(prompt, default=False, console=self.console):
            self.write_config()
            self.update_pulley(pulley_num, 0.5)
            self.show_start_page()
        self.show_calibrate_page(pulley_num)

    def update_pulley(self, pulley_num: int, target_length: float, step_change=0.0) -> bool:
        """
        Connect to pulley and update values.
        :pulley_num: Int value of pulley to update.
        :target_length: Float value of length to set the pulley to.
        :step_change: Float value of amount to change the steps_pr_dm parameter on the selected pulley.
        Default is 0
        :return: True if successful connection, False otherwise
        """
        self.config["steps_pr_dm"][pulley_num] += step_change
        self.config["steps_pr_dm"][pulley_num] = round(self.config["steps_pr_dm"][pulley_num], 4)
        config_data = {"steps_pr_dm": self.config["steps_pr_dm"][pulley_num]}
        move_data = {"acceleration": 0.4, "speed": 0.8, "length": target_length}
        uri = "http://" + self.config["ips"][pulley_num]
        try:
            res1 = requests.post(uri, json=config_data, timeout=0.5).json()
            res2 = requests.post(uri, json=move_data, timeout=0.5).json()
            res3 = requests.post(uri, json={"run": True}, timeout=0.5).json()
        except requests.exceptions.ConnectTimeout:
            return False
        return True


if __name__ == "__main__":
    app = App()
    app.setup()
    try:
        app.show_start_page()
    except KeyboardInterrupt:
        app.console.print("Exiting...")
    app.write_config()
