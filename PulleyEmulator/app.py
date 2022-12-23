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
        self.data_list.update_value("prep_time", self.fp.prep_time)

    def update_length(self):
        self.update_thread = threading.Thread(target=self.fade_length)
        self.update_thread.start()

    def fade_length(self):
        start_time = time.time()
        start_length = float(re.match(r"[\d.]*", self.data_list.length_data.cget("text")).group(0))
        end_length = self.fp.length
        if start_length == end_length:
            return
        diff = end_length - start_length
        try:
            prep_time = float(re.match(r"[\d.]*", self.data_list.prep_time_data.cget("text")).group(0))
        except ValueError:
            return
        self.pulley_frame.run()
        while time.time() - start_time < prep_time and self.alive:
            self.data_list.update_value("length", abs(start_length + diff * ((time.time() - start_time) / prep_time)))
            self.data_list.update_value("time", abs(prep_time - (time.time() - start_time)))
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
        self.prep_time_label = customtkinter.CTkLabel(self, text="Prep Time:", font=self.font)
        self.length_label.place(relx=0.1, rely=0.1, anchor="w")
        self.time_label.place(relx=0.1, rely=0.3, anchor="w")
        self.prep_length_label.place(relx=0.1, rely=0.5, anchor="w")
        self.prep_time_label.place(relx=0.1, rely=0.7, anchor="w")

        self.length_data = customtkinter.CTkLabel(self, text="0.0 dm", font=self.font)
        self.time_data = customtkinter.CTkLabel(self, text="0.0 s", font=self.font)
        self.prep_length_data = customtkinter.CTkLabel(self, text="0.0 dm", font=self.font)
        self.prep_time_data = customtkinter.CTkLabel(self, text="0.0 s", font=self.font)
        self.length_data.place(relx=0.9, rely=0.1, anchor="e")
        self.time_data.place(relx=0.9, rely=0.3, anchor="e")
        self.prep_length_data.place(relx=0.9, rely=0.5, anchor="e")
        self.prep_time_data.place(relx=0.9, rely=0.7, anchor="e")

    def update_value(self, value_name: str, value: float):
        value = round(value, 1)
        match value_name:
            case "length":
                self.length_data.configure(text=f"{value} dm")
            case "time":
                self.time_data.configure(text=f"{value} s")
            case "prep_length":
                self.prep_length_data.configure(text=f"{value} dm")
            case "prep_time":
                self.prep_time_data.configure(text=f"{value} s")
