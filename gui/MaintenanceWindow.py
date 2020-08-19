import tkinter as tk
from PIL import Image, ImageTk

PATH_GUI_FOLDER = "C:\\Users\\ASUS\\PycharmProjects\\Dont_touch_your_face\\gui\\"


class MaintenanceWindow:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        intialize_photo()
        self.top_bar_initialization()
        self.background_label = tk.Label(self.parent, image=face_palm_small)
        self.background_label.pack(fill=tk.BOTH)
        self.set_exit_button()

    def set_exit_button(self):
        self.exit_button = tk.Label(self.parent, image=exit_button)
        self.exit_button.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.exit_button.bind("<Button-1>", self.finish_and_exit)

    def help_key(self):
        self.help_window = tk.Toplevel(self.parent)
        self.help_window.title("help & usage")
        self.help_label = tk.Label(self.help_window, image=help_img)
        self.help_label.pack(fill=tk.BOTH)

    def about(self):
        self.about_window = tk.Toplevel(self.parent)
        self.about_window.title("about...")
        self.about_label = tk.Label(self.about_window, image=about_img)
        self.about_label.pack(fill=tk.BOTH)

    def finish_and_exit(self, *args):
        self.root.destroy()

    def top_bar_initialization(self):
        self.menu = tk.Menu(self.root)
        self.parent.config(menu=self.menu)
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.sound_on = tk.BooleanVar()
        self.mode_menu = tk.Menu(self.menu)
        self.mode_menu.add_checkbutton(label="Sound On", onvalue=1, offvalue=0, variable=self.sound_on,
                                       command=self.switch_sound_mode)
        self.mode_menu.add_checkbutton(label="Sound Off", onvalue=1, offvalue=0, variable=self.sound_on,
                                       command=self.switch_sound_mode)
        self.menu.add_cascade(label="Mode", command=self.mode_menu)
        self.add_commands()

    def add_commands(self):
        self.helpmenu.add_command(label="help & usage", command=self.help_key)
        self.helpmenu.add_command(label="about...", command=self.about)

    def switch_sound_mode(self):
        self.sound_on = not self.sound_on


def intialize_photo():
    global help_img, about_img, face_palm_small, exit_button
    help_photo = Image.open("%shelp_image.png" % PATH_GUI_FOLDER)
    help_img = ImageTk.PhotoImage(help_photo)
    about_photo = Image.open("%sabout_screen.jpg" % PATH_GUI_FOLDER)
    about_img = ImageTk.PhotoImage(about_photo)
    face_palm_small_photo = Image.open("%sface_palm_greek_small_img.jpg" % PATH_GUI_FOLDER)
    face_palm_small = ImageTk.PhotoImage(face_palm_small_photo)
    exit_button_photo = Image.open("%sexit_button_improved.png" % PATH_GUI_FOLDER)
    exit_button = ImageTk.PhotoImage(exit_button_photo)
