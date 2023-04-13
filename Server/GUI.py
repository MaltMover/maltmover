from point import Point, Waypoint
from space import Space, create_space
from request_handler import PulleyRequestHandler, GrabberRequestHandler, create_request_handler, create_grabber_handler

import customtkinter
import json
import os
import threading
from PIL import Image
from time import sleep

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
    "grabber_or": customtkinter.CTkImage(Image.open(os.path.join(image_path, "grabber_or.png")), size=(100, 100)),
    "grabber_cr": customtkinter.CTkImage(Image.open(os.path.join(image_path, "grabber_cr.png")), size=(100, 100)),
    "grabber_og": customtkinter.CTkImage(Image.open(os.path.join(image_path, "grabber_og.png")), size=(100, 100)),
    "grabber_cg": customtkinter.CTkImage(Image.open(os.path.join(image_path, "grabber_cg.png")), size=(100, 100)),
}


class App(customtkinter.CTk):
    def __init__(self, space: Space, request_handler: PulleyRequestHandler, grabber_handler: GrabberRequestHandler):
        super().__init__()
        self.space = space
        self.request_handler = request_handler
        self.grabber_handler = grabber_handler
        self.connection_threads = []  # List of all threads with connections to pulleys
        self.title("Malt Mover")
        self.iconbitmap(os.path.join(image_path, "crane.ico"))
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = NavigationBar(self)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        # create home frame
        self.home_frame = HomePage(self)
        self.home_frame.grid_columnconfigure(0, weight=1)

        # create frame for status page
        self.status_frame = StatusPage(self)

        # create frame for config page
        self.config_frame = ConfigPage(self, "config.json")

        # create frame for waypoint page
        self.waypoint_frame = WaypointPage(self)

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
        if name == "waypoints":
            self.waypoint_frame.grid(row=0, column=1, sticky="nsew")
            self.waypoint_frame.load()
        else:
            self.waypoint_frame.grid_forget()

    def join_connection_threads(self):
        for thread in self.connection_threads:
            thread.join()
        self.connection_threads = []

    def toggle_grabber(self):
        new_state = not self.space.grabber.is_open
        self.grabber_handler.set_state(new_state)
        if self.grabber_handler.success:
            is_open = "o" if new_state else "c"
            self.status_frame.grabber_image.configure(image=images[f"grabber_{is_open}g"])
        self.status_frame.get_mechanical_states(grabber_only=True)

    def toggle_grabber_threaded(self):
        toggle_thread = threading.Thread(target=self.toggle_grabber)
        toggle_thread.start()

    def center_system(self):
        with open("config.json", "r") as f:
            config = json.load(f)
        self.space.move_grabber(self.space.center)
        speed = config["init"]["speed"]
        acceleration = config["init"]["acceleration"]
        for i, pulley in enumerate(self.space.pulleys):
            pulley.speed = speed
            pulley.acceleration = acceleration
            self.space.pulleys[i] = pulley

        print(self.space.pulleys)
        self.request_handler.set_pulleys(self.space.pulleys)
        print(self.request_handler.success_map)

    def move_system(self, target: Point | Waypoint):
        move_time = self.space.move_grabber(target)
        self.request_handler.set_pulleys(self.space.pulleys)
        print(self.request_handler.success_map)
        sleep(move_time)  # Wait for the system to move
        if all(all(self.request_handler.success_map[i]) for i in [0, 1]):
            # If everything is successful, read the current values
            self.status_frame.get_mechanical_states(timeout=4)

    def move_system_three_point(self, target: Point | Waypoint):
        with open("config.json", "r") as f:
            config = json.load(f)
        delay = config["three_point_delay"]
        targets = [
            Point(self.space.grabber.location.x, self.space.grabber.location.y, self.space.size_z - self.space.edge_limit),
            Point(target.x, target.y, self.space.size_z - self.space.edge_limit),
            target
        ]
        times = [
            self.space.calculate_min_move_time(targets[0]),
            self.space.calculate_min_move_time(targets[1], origin=targets[0]),
            self.space.calculate_min_move_time(targets[2], origin=targets[1])
        ]

        for rtarget, rtime in zip(targets, times):
            self.space.move_grabber(rtarget, rtime)
            success_map = self.request_handler.set_pulleys(self.space.pulleys)
            sleep(rtime + delay)
            if not (all(success_map[0]) and all(success_map[1])):
                return
        self.status_frame.get_mechanical_states(timeout=4)

    def move_as_thread(self, target: Point | Waypoint, three_point=False, center=False):
        self.join_connection_threads()  # Join any previous threads
        if center:
            thread = threading.Thread(target=self.center_system)
        elif three_point:
            thread = threading.Thread(target=self.move_system_three_point, args=(target,))
        else:
            thread = threading.Thread(target=self.move_system, args=(target,))
        thread.start()
        self.connection_threads.append(thread)
        self.select_frame_by_name("pulleys")


class NavigationBar(customtkinter.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master)
        self.configure(
            corner_radius=0,
        )
        self.grid_rowconfigure(5, weight=1)
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

        self.waypoint_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Waypoints",
                                                       fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       image=images["waypoint_image"], anchor="w",
                                                       command=lambda: master.select_frame_by_name("waypoints"))
        self.waypoint_button.grid(row=3, column=0, sticky="ew")

        self.config_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Config",
                                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                     image=images["cog_image"], anchor="w",
                                                     command=lambda: master.select_frame_by_name("config"))
        self.config_button.grid(row=4, column=0, sticky="ew")


class HomePage(customtkinter.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master: App = master
        self.waypoint_buttons = []
        self.configure(fg_color="transparent")

    def load(self):
        for button in self.waypoint_buttons:
            button.destroy()
        self.waypoint_buttons = []
        legal_waypoints = [w for w in self.master.space.waypoints if self.master.space.is_legal_point(w)]
        illegal_waypoints = [w for w in self.master.space.waypoints if w not in legal_waypoints]
        with open("config.json", "r") as f:
            config = json.load(f)
        three_point = config["three_point_move"]
        for i, waypoint in enumerate(legal_waypoints + illegal_waypoints):
            time = self.master.space.calculate_min_move_time(waypoint, three_point)
            waypoint_button = customtkinter.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                                      text=f"{waypoint.name}      x: {waypoint.x}   y: {waypoint.y}   z: {waypoint.z}   time: {time}",
                                                      fg_color="transparent", text_color="gray90", hover_color="gray30",
                                                      image=images["waypoint_image"], anchor="w", font=(customtkinter.CTkFont, 18),
                                                      command=lambda waypoint=waypoint, time=time: self.master.move_as_thread(waypoint, three_point))
            if self.master.space.grabber.location == waypoint:
                waypoint_button.configure(state="disabled")
            waypoint_button.grid(row=i, column=0, sticky="ew")
            self.waypoint_buttons.append(waypoint_button)
        for i in range(len(legal_waypoints), len(self.waypoint_buttons)):
            self.waypoint_buttons[i].configure(state="disabled")
        print(self.master.space.grabber.location)


class StatusPage(customtkinter.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master: App = master
        self.configure(self, corner_radius=0, fg_color="transparent")
        self.pulley_0_image = customtkinter.CTkLabel(self, text="", image=images["red_pulley_image"])
        self.pulley_1_image = customtkinter.CTkLabel(self, text="", image=images["red_pulley_image"])
        self.pulley_2_image = customtkinter.CTkLabel(self, text="", image=images["red_pulley_image"])
        self.pulley_3_image = customtkinter.CTkLabel(self, text="", image=images["red_pulley_image"])
        self.pulley_0_image.bind("<Button-3>", lambda event: self.show_reset_dialog(0))
        self.pulley_1_image.bind("<Button-3>", lambda event: self.show_reset_dialog(1))
        self.pulley_2_image.bind("<Button-3>", lambda event: self.show_reset_dialog(2))
        self.pulley_3_image.bind("<Button-3>", lambda event: self.show_reset_dialog(3))

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

        self.grabber_image = customtkinter.CTkLabel(self, text="", image=images["grabber_or"])
        self.grabber_image.place(relx=0.5, rely=0.3, anchor="center")
        self.grabber_image.bind("<Button-1>", lambda event: self.master.toggle_grabber_threaded())

        self.test_connection_button = customtkinter.CTkButton(self, text="Test Connection", font=customtkinter.CTkFont(size=19, weight="bold"),
                                                              command=self.get_mechanical_states)
        self.center_pulleys_button = customtkinter.CTkButton(self, text="Center Pulleys", font=customtkinter.CTkFont(size=19, weight="bold"),
                                                             command=lambda master=master: master.move_as_thread(master.space.center, False, True))
        self.set_steps_button = customtkinter.CTkButton(self, text="Set steps pr dm", font=customtkinter.CTkFont(size=19, weight="bold"),
                                                             command=lambda master=master: master.request_handler.set_steps_pr_dm())
        self.test_connection_button.place(relx=0.5, rely=0.6, anchor="center")
        self.center_pulleys_button.place(relx=0.5, rely=0.7, anchor="center")
        self.set_steps_button.place(relx=0.5, rely=0.8, anchor="center")
        self.load_mechanical_info()

    def load(self):
        for success, image in zip(self.master.request_handler.success_map[0],
                                  [self.pulley_0_image, self.pulley_1_image, self.pulley_2_image, self.pulley_3_image]):
            if success:
                image.configure(image=images["green_pulley_image"])
            else:
                image.configure(image=images["red_pulley_image"])
        self.load_mechanical_info()

    def load_mechanical_info(self):
        # Load the lengths of the pulleys
        for pulley, label in zip(self.master.space.pulleys, [self.pulley_0_length, self.pulley_1_length, self.pulley_2_length, self.pulley_3_length]):
            label.configure(text=f"{pulley.length} dm")
        # Load the state of the grabber
        is_open = "o" if self.master.space.grabber.is_open else "c"
        color = "g" if self.master.grabber_handler.success else "r"
        self.grabber_image.configure(image=images[f"grabber_{is_open}{color}"])

    def get_mechanical_states(self, timeout=3, grabber_only=False):
        """
        Get the states of the mechanical system and update the GUI accordingly
        """
        threads = [threading.Thread(target=self.get_grabber_state, args=(timeout,))]
        if not grabber_only:
            threads.append(threading.Thread(target=self.get_pulley_states, args=(timeout,)))

        for thread in threads:
            thread.start()

    def get_grabber_state(self, timeout: float):
        self.master.space.grabber.is_open = self.master.grabber_handler.get_state(timeout=timeout)  # Get state of grabber
        self.load_mechanical_info()  # Reload the state of the grabber

    def get_pulley_states(self, timeout: float):
        lengths, success_map = self.master.request_handler.get_lengths(timeout=timeout)  # Get the lengths of the pulleys
        # Update the images of the pulleys
        for success, image in zip(success_map, [self.pulley_0_image, self.pulley_1_image, self.pulley_2_image, self.pulley_3_image]):
            if success:
                # Green if the pulley is connected
                image.configure(image=images["green_pulley_image"])
            else:
                # Red if the pulley is not connected
                image.configure(image=images["red_pulley_image"])

        # Update the lengths of the pulleys
        for i, length in enumerate(lengths):
            self.master.space.pulleys[i].length = length

        # Reload the lengths of the pulleys
        self.load_mechanical_info()

    def show_reset_dialog(self, pulley_id=0):
        toplevel = customtkinter.CTkToplevel()
        toplevel.title(f"Reset Pulley {pulley_id}")
        toplevel.geometry("300x200")
        toplevel.resizable(False, False)
        toplevel.grab_set()
        toplevel.focus_set()
        customtkinter.CTkLabel(toplevel, text=f"Reset length of pulley {pulley_id}?", font=customtkinter.CTkFont(size=17, weight="bold")).place(
            relx=0.5, rely=0.3, anchor="center")
        customtkinter.CTkButton(toplevel, text="Cancel", font=customtkinter.CTkFont(size=14, weight="bold"), fg_color="#b52802",
                                width=15, command=toplevel.destroy).place(relx=0.3, rely=0.7, anchor="center")
        customtkinter.CTkButton(toplevel, text="Confirm", font=customtkinter.CTkFont(size=14, weight="bold"), fg_color="#0a8c02",
                                width=15, command=lambda: self.reset_pulley(pulley_id, toplevel)).place(relx=0.7, rely=0.7, anchor="center")

    def reset_pulley(self, pulley_id, toplevel):
        self.master.request_handler.reset_pulley(pulley_id)
        toplevel.destroy()


class ConfigPage(customtkinter.CTkFrame):
    def __init__(self, master: App, config_path: str):
        super().__init__(master)
        self.config_path = config_path
        small_font = customtkinter.CTkFont(size=15)
        big_font = customtkinter.CTkFont(size=20, weight="bold")
        self.configure(self, corner_radius=0, fg_color="transparent")
        # Room Size
        self.acceleration_label = customtkinter.CTkLabel(self, text="Acceleration", font=big_font)
        self.acceleration_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.acceleration_unit_label = customtkinter.CTkLabel(self, text="[dm/s²] (10 cm/s/s)", font=small_font)
        self.acceleration_label.place(relx=0.03, rely=0.08, anchor="sw")
        self.acceleration_entry.place(relx=0.65, rely=0.08, anchor="se")
        self.acceleration_unit_label.place(relx=0.69, rely=0.08, anchor="sw")
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
        self.grabber_label = customtkinter.CTkLabel(self, text="Grabber", font=small_font)
        self.grabber_entry = customtkinter.CTkEntry(self, width=150, justify="right", font=small_font)
        self.pulley_0_label.place(relx=0.03, rely=0.54, anchor="sw")
        self.pulley_0_entry.place(relx=0.65, rely=0.53, anchor="se")
        self.pulley_1_label.place(relx=0.03, rely=0.62, anchor="sw")
        self.pulley_1_entry.place(relx=0.65, rely=0.61, anchor="se")
        self.pulley_2_label.place(relx=0.03, rely=0.70, anchor="sw")
        self.pulley_2_entry.place(relx=0.65, rely=0.69, anchor="se")
        self.pulley_3_label.place(relx=0.03, rely=0.78, anchor="sw")
        self.pulley_3_entry.place(relx=0.65, rely=0.77, anchor="se")
        self.grabber_label.place(relx=0.03, rely=0.86, anchor="sw")
        self.grabber_entry.place(relx=0.65, rely=0.85, anchor="se")
        # 3-point move toggle
        self.three_point_move_label = customtkinter.CTkLabel(self, text="3-point Move", font=big_font)
        self.three_point_move_toggle = customtkinter.CTkButton(self, width=150, height=50, font=small_font, text="OFF", fg_color="#b52802",
                                                               text_color="white", hover_color="#cc1608",
                                                               command=self.toggle_3_point)
        self.three_point_move_label.place(relx=.72, rely=0.48, anchor="sw")
        self.three_point_move_toggle.place(relx=0.98, rely=0.60, anchor="se")

        self.read_config()
        self.save_button = customtkinter.CTkButton(self, text="Save Config", font=big_font, command=self.save_config)
        self.save_button.place(relx=0.5, rely=0.92, anchor="center")

    def load(self):
        self.read_config()

    def toggle_3_point(self):
        if self.three_point_move_toggle.cget("text") == "OFF":
            self.three_point_move_toggle.configure(text="ON", fg_color="#1f6aa5", text_color="white", hover_color="#144870")
        else:
            self.three_point_move_toggle.configure(text="OFF", fg_color="#b52802", text_color="white", hover_color="#cc1608")

    def read_config(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)
        # Acceleration
        self.acceleration_entry.delete(0, customtkinter.END)
        self.acceleration_entry.insert(0, config["max_acceleration"])
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
        self.grabber_entry.delete(0, customtkinter.END)
        self.grabber_entry.insert(0, config["grabber_ip"])
        if config["three_point_move"]:
            self.three_point_move_toggle.configure(text="ON", fg_color="#1f6aa5", text_color="white", hover_color="#144870")
        else:
            self.three_point_move_toggle.configure(text="OFF", fg_color="#b52802", text_color="white", hover_color="#cc1608")

    def save_config(self):
        with open(self.config_path, "r") as f:
            config = json.load(f)
        config["max_acceleration"] = float(self.acceleration_entry.get())
        config["rope_length"] = float(self.rope_length_entry.get())
        config["max_speed"] = float(self.max_speed_entry.get())
        config["edge_limit"] = float(self.edge_limit_entry.get())
        config["ips"][0] = self.pulley_0_entry.get()
        config["ips"][1] = self.pulley_1_entry.get()
        config["ips"][2] = self.pulley_2_entry.get()
        config["ips"][3] = self.pulley_3_entry.get()
        config["grabber_ip"] = self.grabber_entry.get()
        config["three_point_move"] = self.three_point_move_toggle.cget("text") == "ON"
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
        self.master.space.write_waypoints("waypoints.json")
        space = create_space(self.master.space.grabber.location)
        request_handler = create_request_handler()
        grabber_handler = create_grabber_handler()
        self.master.space = space
        self.master.request_handler = request_handler
        self.master.grabber_handler = grabber_handler


class WaypointPage(customtkinter.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master)
        self.master: App = master
        self.waypoint_buttons = []
        self.configure(self, corner_radius=0, fg_color="transparent")
        customtkinter.CTkLabel(self, text="Waypoints", font=customtkinter.CTkFont(size=15, weight="bold")
                               ).place(relx=0.5, rely=0.05, anchor="center")

    def load(self):
        for button in self.waypoint_buttons:
            button.destroy()
        self.waypoint_buttons = []
        for i, waypoint in enumerate(self.master.space.waypoints):
            button = customtkinter.CTkButton(self, text=waypoint.name, font=customtkinter.CTkFont(size=15),
                                             command=lambda i=i: self.edit_waypoint(i))
            button.place(relx=0.2 + (i % 3) * 0.3, rely=0.2 + (i // 3) * 0.1, anchor="center")
            self.waypoint_buttons.append(button)
        add_button = customtkinter.CTkButton(self, text="Add Waypoint", font=customtkinter.CTkFont(size=15),
                                             command=self.add_waypoint)
        add_button.place(relx=0.5, rely=0.9, anchor="center")

    def edit_waypoint(self, index: int):
        waypoint = self.master.space.waypoints[index]
        editor = customtkinter.CTkToplevel(self)
        editor.title("Edit Waypoint")
        editor.geometry("500x300")
        editor.resizable(False, False)
        editor.grab_set()
        name_entry = customtkinter.CTkEntry(editor, width=200, font=customtkinter.CTkFont(size=15))
        name_entry.insert(0, waypoint.name)
        name_entry.place(relx=0.5, rely=0.1, anchor="center")
        x_label = customtkinter.CTkLabel(editor, text="x", font=customtkinter.CTkFont(size=15))
        x_entry = customtkinter.CTkEntry(editor, width=200, font=customtkinter.CTkFont(size=15))
        x_entry.insert(0, waypoint.x)
        x_label.place(relx=0.25, rely=0.3, anchor="center")
        x_entry.place(relx=0.5, rely=0.3, anchor="center")
        y_label = customtkinter.CTkLabel(editor, text="y", font=customtkinter.CTkFont(size=15))
        y_entry = customtkinter.CTkEntry(editor, width=200, font=customtkinter.CTkFont(size=15))
        y_entry.insert(0, waypoint.y)
        y_label.place(relx=0.25, rely=0.5, anchor="center")
        y_entry.place(relx=0.5, rely=0.5, anchor="center")
        z_label = customtkinter.CTkLabel(editor, text="z", font=customtkinter.CTkFont(size=15))
        z_entry = customtkinter.CTkEntry(editor, width=200, font=customtkinter.CTkFont(size=15))
        z_entry.insert(0, waypoint.z)
        z_label.place(relx=0.25, rely=0.7, anchor="center")
        z_entry.place(relx=0.5, rely=0.7, anchor="center")
        delete_button = customtkinter.CTkButton(editor, text="Delete", font=customtkinter.CTkFont(size=15), width=75, fg_color="#b52802",
                                                command=lambda: self.delete_waypoint(index, editor))
        delete_button.place(relx=0.4, rely=0.9, anchor="center")
        save_button = customtkinter.CTkButton(editor, text="Save", font=customtkinter.CTkFont(size=15), width=75,
                                              command=lambda: self.save_waypoint(index, editor, x_entry.get(), y_entry.get(), z_entry.get(),
                                                                                 name_entry.get()))
        save_button.place(relx=0.6, rely=0.9, anchor="center")

    def save_waypoint(self, index: int, editor: customtkinter.CTkToplevel, x, y, z, name):
        self.master.space.waypoints[index] = Waypoint(float(x), float(y), float(z), name)
        editor.destroy()
        self.load()

    def add_waypoint(self):
        self.master.space.waypoints.append(Waypoint(0, 0, 0, "New Waypoint"))
        self.load()
        self.edit_waypoint(-1)

    def delete_waypoint(self, index: int, editor: customtkinter.CTkToplevel):
        self.master.space.waypoints.pop(index)
        editor.destroy()
        self.load()


if __name__ == "__main__":
    app = App()
    app.mainloop()
