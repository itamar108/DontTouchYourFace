import tkinter as tk
from PIL import Image, ImageTk

PATH_GUI_FOLDER = "C:\\Users\\ASUS\\PycharmProjects\\Dont_touch_your_face\\gui\\"


class MaintenanceWindow:
    def __init__(self, parent, root, sound_mode):
        self.sound_on = sound_mode
        self.sound_on_button = False
        self.parent = parent
        self.root = root
        intialize_photo()
        self.top_bar_initialization()
        self.background_label = tk.Label(self.parent, image=face_palm_small)
        self.background_label.pack(fill=tk.BOTH)
        self.set_exit_button()
        self.add_commands()

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
        self.set_up_options_menu()
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)

    def set_up_options_menu(self):
        self.options_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Options", menu=self.options_menu)
        if self.sound_on:
            self.options_menu.add_checkbutton(label="disable sound", onvalue=True,
                                              offvalue=False,
                                              variable=self.sound_on, command=self.switch_sound_mode)
        else:
            self.options_menu.add_checkbutton(label="Enable sound", onvalue=True,
                                              offvalue=False,
                                              variable=self.sound_on, command=self.switch_sound_mode)
        self.window_on_top = tk.BooleanVar()
        self.options_menu.add_checkbutton(label="Window on Top",
                                          onvalue=1,
                                          offvalue=0,
                                          variable=self.window_on_top,
                                          command=self.change_window_apperance)

    def change_window_apperance(self):
        self.parent.attributes('-topmost', self.window_on_top.get())

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
    face_palm_small_photo = Image.open("%ssmall_screen_bg.jpg" % PATH_GUI_FOLDER)
    face_palm_small = ImageTk.PhotoImage(face_palm_small_photo)
    exit_button_photo = Image.open("%sexit_button_improved.png" % PATH_GUI_FOLDER)
    exit_button = ImageTk.PhotoImage(exit_button_photo)