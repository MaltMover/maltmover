import tkinter
import json

import customtkinter
import os
from PIL import Image

# load images with light and dark mode image
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
images = {
    "logo_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "crane.png")), size=(26, 26)),
    "large_test_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150)),
    "image_icon_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20)),
    "home_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20)),
    "cog_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "cog_light.png")), size=(20, 20)),
    "white_pulley_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "whitepulley.png")), size=(25, 25)),
    "green_pulley_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "greenpulley.png")), size=(100, 100)),
    "red_pulley_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "redpulley.png")), size=(100, 100)),
}


class NavigationBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(
            corner_radius=0,
        )
        self.nav_label = customtkinter.CTkLabel(self, text="  Malt Mover", image=images["logo_image"],
                                                compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.nav_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=images["home_image"], anchor="w",
                                                   command=lambda: master.select_frame_by_name("home"))
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.pulley_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=5, text="Pulley status",
                                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                     image=images["white_pulley_image"], anchor="w",
                                                     command=lambda: master.select_frame_by_name("pulleys"))
        self.pulley_button.grid(row=2, column=0, sticky="ew")

        self.config_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Config",
                                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                     image=images["cog_image"], anchor="w",
                                                     command=lambda: master.select_frame_by_name("config"))
        self.config_button.grid(row=3, column=0, sticky="ew")


class HomePage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.home_frame_large_image_label = customtkinter.CTkLabel(self, text="", image=images["large_test_image"])
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self, text="", image=images["image_icon_image"])
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_2 = customtkinter.CTkButton(self, text="CTkButton", image=images["image_icon_image"], compound="right")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = customtkinter.CTkButton(self, text="CTkButton", image=images["image_icon_image"], compound="top")
        self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.home_frame_button_4 = customtkinter.CTkButton(self, text="CTkButton", image=images["image_icon_image"], compound="bottom",
                                                           anchor="w")
        self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)


class StatusPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(self, corner_radius=0, fg_color="transparent")
        self.pulley_0_label = customtkinter.CTkLabel(self, text="", image=images["green_pulley_image"])
        self.pulley_1_label = customtkinter.CTkLabel(self, text="", image=images["green_pulley_image"])
        self.pulley_2_label = customtkinter.CTkLabel(self, text="", image=images["green_pulley_image"])
        self.pulley_3_label = customtkinter.CTkLabel(self, text="", image=images["green_pulley_image"])
        self.pulley_0_label.place(relx=0.2, rely=0.8, anchor="center")
        self.pulley_1_label.place(relx=0.8, rely=0.2, anchor="center")
        self.pulley_2_label.place(relx=0.2, rely=0.2, anchor="center")
        self.pulley_3_label.place(relx=0.8, rely=0.8, anchor="center")
        self.pulley_test_button = customtkinter.CTkButton(self, text="Test Pulleys", command=lambda: print("wow"))
        self.pulley_test_button.place(relx=0.5, rely=0.5, anchor="center")


class ConfigPage(customtkinter.CTkFrame):
    def __init__(self, master, config_path: str):
        super().__init__(master)
        self.config_path = config_path
        small_font = customtkinter.CTkFont(size=15)
        big_font = customtkinter.CTkFont(size=20, weight="bold")
        self.configure(self, corner_radius=0, fg_color="transparent")
        # Room Size
        self.size_label = customtkinter.CTkLabel(self, text="Room Size", font=big_font)
        self.x_label = customtkinter.CTkLabel(self, text="x", font=small_font)
        self.x_entry = customtkinter.CTkEntry(self, width=45, font=small_font)
        self.y_label = customtkinter.CTkLabel(self, text="y", font=small_font)
        self.y_entry = customtkinter.CTkEntry(self, width=45, font=small_font)
        self.z_label = customtkinter.CTkLabel(self, text="z", font=small_font)
        self.z_entry = customtkinter.CTkEntry(self, width=45, font=small_font)
        self.size_unit_label = customtkinter.CTkLabel(self, text="[dm] (10 cm)", font=big_font)
        self.size_label.place(relx=0.03, rely=0.08, anchor="sw")
        self.x_label.place(relx=0.31, rely=0.08, anchor="sw")
        self.x_entry.place(relx=0.33, rely=0.08, anchor="sw")
        self.y_label.place(relx=0.43, rely=0.08, anchor="sw")
        self.y_entry.place(relx=0.45, rely=0.08, anchor="sw")
        self.z_label.place(relx=0.55, rely=0.08, anchor="sw")
        self.z_entry.place(relx=0.65, rely=0.08, anchor="se")
        self.size_unit_label.place(relx=0.70, rely=0.08, anchor="sw")
        # Rope Length
        self.rope_length_label = customtkinter.CTkLabel(self, text="Rope Length", font=big_font)
        self.rope_length_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.rope_length_unit_label = customtkinter.CTkLabel(self, text="[dm] (10 cm)", font=big_font)
        self.rope_length_label.place(relx=0.03, rely=0.18, anchor="sw")
        self.rope_length_entry.place(relx=0.65, rely=0.18, anchor="se")
        self.rope_length_unit_label.place(relx=0.70, rely=0.18, anchor="sw")

        self.read_config()
        self.save_button = customtkinter.CTkButton(self, text="Save Config", font=big_font, command=self.save_config)
        self.save_button.place(relx=0.5, rely=0.9, anchor="center")

    def read_config(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)
        # Room Size
        self.x_entry.delete(0, customtkinter.END)
        self.x_entry.insert(0, config["size"][0])
        self.y_entry.delete(0, customtkinter.END)
        self.y_entry.insert(0, config["size"][1])
        self.z_entry.delete(0, customtkinter.END)
        self.z_entry.insert(0, config["size"][2])
        # Rope Length
        self.rope_length_entry.delete(0, customtkinter.END)
        self.rope_length_entry.insert(0, config["rope_length"])

    def save_config(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)
        config["size"][0] = float(self.x_entry.get())
        config["size"][1] = float(self.y_entry.get())
        config["size"][2] = float(self.z_entry.get())
        config["rope_length"] = float(self.rope_length_entry.get())
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Malt Mover")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = NavigationBar(self)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # create home frame
        self.home_frame = HomePage(self)
        self.home_frame.grid_columnconfigure(0, weight=1)

        # create second frame
        self.status_frame = StatusPage(self)

        # create third frame
        self.config_frame = ConfigPage(self, "config.json")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.navigation_frame.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.navigation_frame.pulley_button.configure(fg_color=("gray75", "gray25") if name == "pulleys" else "transparent")
        self.navigation_frame.config_button.configure(fg_color=("gray75", "gray25") if name == "config" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "pulleys":
            self.status_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.status_frame.grid_forget()
        if name == "config":
            self.config_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.config_frame.grid_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()
