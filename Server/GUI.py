import threading

from point import Point, Waypoint
from space import Space
from request_handler import RequestHandler

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
    "waypoint_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "waypoint_light.png")), size=(30, 30)),
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
        self.master = master
        self.waypoint_buttons = []
        self.configure(fg_color="transparent")

    def load(self):
        legal_waypoints = [w for w in self.master.space.waypoints if self.master.space.is_legal_point(w)]
        illegal_waypoints = [w for w in self.master.space.waypoints if w not in legal_waypoints]
        for i, waypoint in enumerate(legal_waypoints):
            time = self.master.space.calculate_min_time(waypoint)
            waypoint_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                      text=f"{waypoint.name}      x: {waypoint.x}   y: {waypoint.y}   z: {waypoint.z}   time: {time}",
                                                      fg_color="transparent", text_color="gray90", hover_color="gray30",
                                                      image=images["waypoint_image"], anchor="w", font=(customtkinter.CTkFont, 18),
                                                      command=lambda waypoint=waypoint, time=time: self.master.move_as_thread(waypoint, time))
            if self.master.space.current_point == waypoint:
                waypoint_button.configure(state="disabled")
            waypoint_button.grid(row=i, column=0, sticky="ew")
            self.waypoint_buttons.append(waypoint_button)
        print(self.master.space.current_point)


class StatusPage(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(self, corner_radius=0, fg_color="transparent")
        self.pulley_0_image = customtkinter.CTkLabel(self, text="", image=images["red_pulley_image"])
        self.pulley_1_image = customtkinter.CTkLabel(self, text="", image=images["red_pulley_image"])
        self.pulley_2_image = customtkinter.CTkLabel(self, text="", image=images["red_pulley_image"])
        self.pulley_3_image = customtkinter.CTkLabel(self, text="", image=images["red_pulley_image"])
        self.pulley_0_id = customtkinter.CTkLabel(self, text="0", font=customtkinter.CTkFont(size=17, weight="bold"))
        self.pulley_1_id = customtkinter.CTkLabel(self, text="1", font=customtkinter.CTkFont(size=17, weight="bold"))
        self.pulley_2_id = customtkinter.CTkLabel(self, text="2", font=customtkinter.CTkFont(size=17, weight="bold"))
        self.pulley_3_id = customtkinter.CTkLabel(self, text="3", font=customtkinter.CTkFont(size=17, weight="bold"))
        self.pulley_0_length = customtkinter.CTkLabel(self, text="0.0 dm", font=customtkinter.CTkFont(size=17, weight="bold"))
        self.pulley_1_length = customtkinter.CTkLabel(self, text="0.0 dm", font=customtkinter.CTkFont(size=17, weight="bold"))
        self.pulley_2_length = customtkinter.CTkLabel(self, text="0.0 dm", font=customtkinter.CTkFont(size=17, weight="bold"))
        self.pulley_3_length = customtkinter.CTkLabel(self, text="0.0 dm", font=customtkinter.CTkFont(size=17, weight="bold"))
        self.pulley_0_image.place(relx=0.12, rely=0.78, anchor="center")
        self.pulley_1_image.place(relx=0.88, rely=0.78, anchor="center")
        self.pulley_2_image.place(relx=0.12, rely=0.18, anchor="center")
        self.pulley_3_image.place(relx=0.88, rely=0.18, anchor="center")
        self.pulley_0_id.place(relx=0.12, rely=0.63, anchor="center")
        self.pulley_1_id.place(relx=0.88, rely=0.63, anchor="center")
        self.pulley_2_id.place(relx=0.12, rely=0.03, anchor="center")
        self.pulley_3_id.place(relx=0.88, rely=0.03, anchor="center")
        self.pulley_0_length.place(relx=0.12, rely=0.93, anchor="center")
        self.pulley_1_length.place(relx=0.88, rely=0.93, anchor="center")
        self.pulley_2_length.place(relx=0.12, rely=0.33, anchor="center")
        self.pulley_3_length.place(relx=0.88, rely=0.33, anchor="center")

        with open("config.json", "r") as f:
            config = json.load(f)
            init_time = config["init_time"]
        self.test_connection_button = customtkinter.CTkButton(self, text="Test Connection", font=customtkinter.CTkFont(size=19, weight="bold"),
                                                              command=self.get_lengths)
        self.center_pulleys_button = customtkinter.CTkButton(self, text="Center Pulleys", font=customtkinter.CTkFont(size=19, weight="bold"),
                                                             command=lambda master=master: master.move_as_thread(master.space.center,
                                                                                                                 init_time))
        self.test_connection_button.place(relx=0.5, rely=0.5, anchor="center")
        self.center_pulleys_button.place(relx=0.5, rely=0.6, anchor="center")
        self.load_pulley_info()

    def load(self):
        for success, image in zip(self.master.request_handler.success_map[0],
                                  [self.pulley_0_image, self.pulley_1_image, self.pulley_2_image, self.pulley_3_image]):
            if success:
                image.configure(image=images["green_pulley_image"])
            else:
                image.configure(image=images["red_pulley_image"])
        self.load_pulley_info()

    def load_pulley_info(self):
        for pulley, label in zip(self.master.space.pulleys, [self.pulley_0_length, self.pulley_1_length, self.pulley_2_length, self.pulley_3_length]):
            label.configure(text=f"{pulley.length} dm")

    def get_lengths(self, timeout=3):
        lengths, success_map = self.master.request_handler.get_lengths(timeout=timeout)
        for success, image in zip(success_map, [self.pulley_0_image, self.pulley_1_image, self.pulley_2_image, self.pulley_3_image]):
            if success:
                image.configure(image=images["green_pulley_image"])
            else:
                image.configure(image=images["red_pulley_image"])

        for i, length in enumerate(lengths):
            self.master.space.pulleys[i].length = length
        self.load_pulley_info()


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
        self.size_unit_label.place(relx=0.69, rely=0.08, anchor="sw")
        # Rope Length
        self.rope_length_label = customtkinter.CTkLabel(self, text="Rope Length", font=big_font)
        self.rope_length_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.rope_length_unit_label = customtkinter.CTkLabel(self, text="[dm] (10 cm)", font=big_font)
        self.rope_length_label.place(relx=0.03, rely=0.18, anchor="sw")
        self.rope_length_entry.place(relx=0.65, rely=0.18, anchor="se")
        self.rope_length_unit_label.place(relx=0.69, rely=0.18, anchor="sw")
        # Max speed
        self.max_speed_label = customtkinter.CTkLabel(self, text="Max Speed", font=big_font)
        self.max_speed_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.max_speed_unit_label = customtkinter.CTkLabel(self, text="[dm/s] (10 cm/s)", font=big_font)
        self.max_speed_label.place(relx=0.03, rely=0.28, anchor="sw")
        self.max_speed_entry.place(relx=0.65, rely=0.28, anchor="se")
        self.max_speed_unit_label.place(relx=0.69, rely=0.28, anchor="sw")
        # Edge limit
        self.edge_limit_label = customtkinter.CTkLabel(self, text="Edge Limit", font=big_font)
        self.edge_limit_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.edge_limit_unit_label = customtkinter.CTkLabel(self, text="[dm] (10 cm)", font=big_font)
        self.edge_limit_label.place(relx=0.03, rely=0.38, anchor="sw")
        self.edge_limit_entry.place(relx=0.65, rely=0.38, anchor="se")
        self.edge_limit_unit_label.place(relx=0.69, rely=0.38, anchor="sw")
        # Separating line
        line = customtkinter.CTkCanvas(self, width=510, height=2, bg="gray25", highlightthickness=0)
        line.create_line(0, 0, 510, 0, fill="gray25", width=4)
        line.place(relx=0.03, rely=0.4, anchor="w")
        # IPS
        self.ips_label = customtkinter.CTkLabel(self, text="IP Addresses", font=big_font)
        self.ips_label.place(relx=0.03, rely=0.48, anchor="sw")
        self.pulley_0_label = customtkinter.CTkLabel(self, text="Pulley 0", font=small_font)
        self.pulley_0_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.pulley_1_label = customtkinter.CTkLabel(self, text="Pulley 1", font=small_font)
        self.pulley_1_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.pulley_2_label = customtkinter.CTkLabel(self, text="Pulley 2", font=small_font)
        self.pulley_2_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.pulley_3_label = customtkinter.CTkLabel(self, text="Pulley 3", font=small_font)
        self.pulley_3_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.pulley_0_label.place(relx=0.03, rely=0.55, anchor="sw")
        self.pulley_0_entry.place(relx=0.65, rely=0.55, anchor="se")
        self.pulley_1_label.place(relx=0.03, rely=0.65, anchor="sw")
        self.pulley_1_entry.place(relx=0.65, rely=0.65, anchor="se")
        self.pulley_2_label.place(relx=0.03, rely=0.75, anchor="sw")
        self.pulley_2_entry.place(relx=0.65, rely=0.75, anchor="se")
        self.pulley_3_label.place(relx=0.03, rely=0.85, anchor="sw")
        self.pulley_3_entry.place(relx=0.65, rely=0.85, anchor="se")

        self.read_config()
        self.save_button = customtkinter.CTkButton(self, text="Save Config", font=big_font, command=self.save_config)
        self.save_button.place(relx=0.5, rely=0.92, anchor="center")

    def load(self):
        self.read_config()

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
        # Max speed
        self.max_speed_entry.delete(0, customtkinter.END)
        self.max_speed_entry.insert(0, config["max_speed"])
        # Edge limit
        self.edge_limit_entry.delete(0, customtkinter.END)
        self.edge_limit_entry.insert(0, config["edge_limit"])
        # IPS
        self.pulley_0_entry.delete(0, customtkinter.END)
        self.pulley_0_entry.insert(0, config["ips"][0])
        self.pulley_1_entry.delete(0, customtkinter.END)
        self.pulley_1_entry.insert(0, config["ips"][1])
        self.pulley_2_entry.delete(0, customtkinter.END)
        self.pulley_2_entry.insert(0, config["ips"][2])
        self.pulley_3_entry.delete(0, customtkinter.END)
        self.pulley_3_entry.insert(0, config["ips"][3])

    def save_config(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)
        config["size"][0] = float(self.x_entry.get())
        config["size"][1] = float(self.y_entry.get())
        config["size"][2] = float(self.z_entry.get())
        config["rope_length"] = float(self.rope_length_entry.get())
        config["max_speed"] = float(self.max_speed_entry.get())
        config["edge_limit"] = float(self.edge_limit_entry.get())
        config["ips"][0] = self.pulley_0_entry.get()
        config["ips"][1] = self.pulley_1_entry.get()
        config["ips"][2] = self.pulley_2_entry.get()
        config["ips"][3] = self.pulley_3_entry.get()
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)


class App(customtkinter.CTk):
    def __init__(self, space: Space, request_handler: RequestHandler):
        super().__init__()
        self.space = space
        self.request_handler = request_handler
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
            self.home_frame.load()
        else:
            self.home_frame.grid_forget()
        if name == "pulleys":
            self.status_frame.grid(row=0, column=1, sticky="nsew")
            self.status_frame.load()
        else:
            self.status_frame.grid_forget()
        if name == "config":
            self.config_frame.grid(row=0, column=1, sticky="nsew")
            self.config_frame.load()
        else:
            self.config_frame.grid_forget()

    def move_system(self, target: Point | Waypoint, time: float):
        self.space.update_lengths(target, time)
        self.request_handler.set_pulleys(self.space.pulleys, time)
        self.status_frame.get_lengths(timeout=1)

    def move_as_thread(self, target: Point | Waypoint, time: float):
        thread = threading.Thread(target=self.move_system, args=(target, time))
        thread.start()
        self.select_frame_by_name("pulleys")


if __name__ == "__main__":
    app = App()
    app.mainloop()
