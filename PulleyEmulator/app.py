import customtkinter
import os
import re
import threading
import time
from PIL import Image
from fake_pulley import FakePulley

# load images with light and dark mode image
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
images = {
    "logo_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "crane.png")), size=(26, 26)),
    "white_pulley_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "whitepulley.png")), size=(300, 300)),
    "green_pulley_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "greenpulley.png")), size=(300, 300)),
    "red_pulley_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "redpulley.png")), size=(300, 300)),
}


class App(customtkinter.CTk):
    def __init__(self, fp: FakePulley):
        super().__init__()
        self.fp = fp
        self.title("Pulley Emulator")
        self.geometry("960x540")
        self.iconbitmap(os.path.join(image_path, "crane.ico"))
        self.pulley_frame = PulleyDisplay(self)
        self.data_list = DataList(self)
        self.pulley_frame.place(relx=0.03, rely=0.45, anchor="w")
        self.data_list.place(relx=0.35, rely=0.45, anchor="w")
        self.update_thread = None
        self.alive = True

    def update_values(self):
        self.update_length()
        self.data_list.update_value("prep_length", self.fp.prep_length)
        self.data_list.update_value("speed", self.fp.speed)
        self.data_list.update_value("acceleration", self.fp.acceleration)

    def update_length(self):
        self.update_thread = threading.Thread(target=self.fade_length)
        self.update_thread.start()

    def fade_length(self):
        start_time = time.time()
        start_length = float(re.match(r"[\d.]*", self.data_list.length_data.cget("text")).group(0))
        end_length = self.fp.length
        print(start_length, end_length)
        if start_length == end_length:
            return
        diff = end_length - start_length
        try:
            speed = float(re.match(r"[\d.]*", self.data_list.speed_data.cget("text")).group(0))
            acceleration = float(re.match(r"[\d.]*", self.data_list.acceleration_data.cget("text")).group(0))
            move_time = calc_move_time(move_length=abs(diff), speed=speed, acceleration=acceleration)
        except ValueError:
            return
        self.pulley_frame.run()
        while time.time() - start_time < move_time and self.alive:
            move_size = calc_current_length(move_length=abs(diff), speed=speed, acceleration=acceleration, current_time=time.time() - start_time)
            if diff < 0:
                move_size = -move_size
            self.data_list.update_value("length", start_length + move_size)
            self.data_list.update_value("time", abs(move_time - (time.time() - start_time)))
        self.pulley_frame.stop()

    def kill(self):
        self.alive = False
        try:
            self.update_thread.join()
        except AttributeError:
            pass


class PulleyDisplay(customtkinter.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master)
        self.configure(height=300, width=300, fg_color="transparent")
        self.pulley_image_label = customtkinter.CTkLabel(self, image=images["white_pulley_image"], text="")
        self.pulley_image_label.pack(fill="both", expand=True)

    def run(self):
        self.pulley_image_label.configure(image=images["green_pulley_image"])

    def stop(self):
        self.pulley_image_label.configure(image=images["white_pulley_image"])


class DataList(customtkinter.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master)
        self.configure(height=300, width=500, fg_color="transparent")
        self.font = ("Arial", 35)
        self.length_label = customtkinter.CTkLabel(self, text="Length:", font=self.font)
        self.time_label = customtkinter.CTkLabel(self, text="Time:", font=self.font)
        self.prep_length_label = customtkinter.CTkLabel(self, text="Prep Length:", font=self.font)
        self.speed_label = customtkinter.CTkLabel(self, text="Speed:", font=self.font)
        self.acceleration_label = customtkinter.CTkLabel(self, text="Acceleration:", font=self.font)
        self.length_label.place(relx=0.1, rely=0.1, anchor="w")
        self.time_label.place(relx=0.1, rely=0.3, anchor="w")
        self.prep_length_label.place(relx=0.1, rely=0.5, anchor="w")
        self.speed_label.place(relx=0.1, rely=0.7, anchor="w")
        self.acceleration_label.place(relx=0.1, rely=0.9, anchor="w")

        self.length_data = customtkinter.CTkLabel(self, text="0.0 dm", font=self.font)
        self.time_data = customtkinter.CTkLabel(self, text="0.0 s", font=self.font)
        self.prep_length_data = customtkinter.CTkLabel(self, text="0.0 dm", font=self.font)
        self.speed_data = customtkinter.CTkLabel(self, text="0.0 dm/s", font=self.font)
        self.acceleration_data = customtkinter.CTkLabel(self, text="0.0 dm/s²", font=self.font)
        self.length_data.place(relx=0.9, rely=0.1, anchor="e")
        self.time_data.place(relx=0.9, rely=0.3, anchor="e")
        self.prep_length_data.place(relx=0.9, rely=0.5, anchor="e")
        self.speed_data.place(relx=0.9, rely=0.7, anchor="e")
        self.acceleration_data.place(relx=0.9, rely=0.9, anchor="e")

    def update_value(self, value_name: str, value: float):
        value = round(value, 1)
        match value_name:
            case "length":
                self.length_data.configure(text=f"{value} dm")
            case "time":
                self.time_data.configure(text=f"{value} s")
            case "prep_length":
                if value == -1:
                    self.prep_length_data.configure(text=f"N/A")
                    return
                self.prep_length_data.configure(text=f"{value} dm")
            case "speed":
                self.speed_data.configure(text=f"{value} dm/s")
            case "acceleration":
                self.acceleration_data.configure(text=f"{value} dm/s²")


def calc_current_length(move_length: float, speed: float, acceleration: float, current_time: float) -> float:
    if move_length <= 0:
        raise ValueError("Move length must be greater than 0")
    time_to_max_speed = speed / acceleration  # Time to reach max speed
    distance_to_max_speed = 0.5 * acceleration * time_to_max_speed ** 2  # Distance travelled to reach max speed

    if distance_to_max_speed * 2 > move_length:  # If it is not possible to reach max speed
        total_time = calc_move_time(move_length, speed, acceleration)  # Time to complete move
        if current_time <= total_time / 2:  # If it hasn't started breaking yet
            return 0.5 * acceleration * current_time ** 2
        breaking_time = current_time - (total_time / 2)  # Time spent breaking
        max_speed = total_time/2 * acceleration  # Max speed reached
        return move_length/2 + max_speed * breaking_time + 0.5 * -acceleration * breaking_time ** 2

    if current_time <= time_to_max_speed:  # If max speed has not been reached
        return 0.5 * acceleration * current_time ** 2

    time_at_max_speed = (move_length - (distance_to_max_speed * 2)) / speed  # Time spent at max speed
    if current_time <= time_to_max_speed + time_at_max_speed:  # If max speed has been reached
        return distance_to_max_speed + (current_time - time_to_max_speed) * speed
    distance_at_max_speed = time_at_max_speed * speed  # Distance travelled at max speed
    if current_time <= time_to_max_speed * 2 + time_at_max_speed:  # If max speed has been reached and is being lowered
        breaking_time = current_time - time_to_max_speed - time_at_max_speed  # Time spent breaking
        return distance_to_max_speed + distance_at_max_speed + speed * breaking_time - 0.5 * acceleration * breaking_time ** 2
    return move_length


def calc_move_time(move_length: float, speed: float, acceleration: float) -> float:
    """
    Calculates the time it takes to move a certain distance at a certain speed with a certain acceleration
    :param move_length: The length to move
    :param speed: The speed to move at
    :param acceleration: The acceleration to use
    :return: The time it takes to move the length
    """
    time_to_max_speed = speed / acceleration  # Time to reach max speed
    distance_to_max_speed = 0.5 * acceleration * time_to_max_speed ** 2  # Distance travelled to reach max speed
    if distance_to_max_speed * 2 > move_length:  # If it is not possible to reach max speed
        return ((move_length / acceleration) ** 0.5) * 2  # Time formula (t = sqrt(2 * d / a))
    max_speed_move_time = (move_length - distance_to_max_speed * 2) / speed  # Time spent at max speed
    return 2 * time_to_max_speed + max_speed_move_time  # Times two because it has to break as well


def _draw_graph(move_length: float, speed: float, acceleration: float):
    from matplotlib import pyplot as plt
    t = calc_move_time(move_length=move_length, speed=speed, acceleration=acceleration)
    print(t)
    data = []
    for i in range(int(t * 100)):
        data.append(calc_current_length(move_length=move_length, speed=speed, acceleration=acceleration, current_time=i / 100))

    plt.plot(data)
    plt.show()


if __name__ == '__main__':
    _draw_graph(move_length=50, speed=5, acceleration=0.2)
