import customtkinter
import os
from PIL import Image
from fake_grabber import FakeGrabber

# load images with light and dark mode image
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
images = {
    "logo_image": customtkinter.CTkImage(Image.open(os.path.join(image_path, "crane.png")), size=(26, 26)),
    "grabber_open": customtkinter.CTkImage(Image.open(os.path.join(image_path, "grabber_open.png")), size=(300, 300)),
    "grabber_closed": customtkinter.CTkImage(Image.open(os.path.join(image_path, "grabber_closed.png")), size=(300, 300)),
}


class App(customtkinter.CTk):
    def __init__(self, fg: FakeGrabber):
        super().__init__()
        self.fg = fg
        self.title("Grabber Emulator")
        self.geometry("540x540")
        self.iconbitmap(os.path.join(image_path, "crane.ico"))
        self.grabber_frame = GrabberDisplay(self)
        self.grabber_frame.place(relx=0.5, rely=0.5, anchor="center")

    def update_values(self):
        if self.fg.is_open:
            self.grabber_frame.open()
        else:
            self.grabber_frame.close()


class GrabberDisplay(customtkinter.CTkFrame):
    def __init__(self, master: App):
        super().__init__(master)
        self.configure(height=300, width=300, fg_color="transparent")
        self.pulley_image_label = customtkinter.CTkLabel(self, image=images["grabber_closed"], text="")
        self.pulley_image_label.pack(fill="both", expand=True)

    def open(self):
        self.pulley_image_label.configure(image=images["grabber_open"])

    def close(self):
        self.pulley_image_label.configure(image=images["grabber_closed"])
