import customtkinter
import os
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
        self.information_list = LabelList(self)
        self.pulley_frame.place(relx=0.03, rely=0.45, anchor="w")
        self.information_list.place(relx=0.35, rely=0.45, anchor="w")


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


class LabelList(customtkinter.CTkFrame):
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

    def update_value(self, value: float, value_name: str):
        match value_name:
            case "length":
                self.length_data.configure(text=f"{value} dm")
            case "time":
                self.time_data.configure(text=f"{value} s")
            case "prep_length":
                self.prep_length_data.configure(text=f"{value} dm")
            case "prep_time":
                self.prep_time_data.configure(text=f"{value} s")
