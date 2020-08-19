import tkinter as tk
from PIL import Image, ImageTk

PATH_GUI_FOLDER = "C:\\Users\\ASUS\\PycharmProjects\\Dont_touch_your_face\\gui\\"

ROOT_TITLE = "D.T.Y.F  (= Don't Touch Your Face)"


class startMenu:
    def __init__(self, parent):
        self.parent = parent
        self.soundMode = False
        self.top_bar_initialization()
        initalize_start_photo()
        self.canvas = tk.Canvas(self.parent, width=620, height=404, highlightthickness=0, borderwidth=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=main_start_photo, anchor="nw")
        self.set_sound_button()
        self.set_up_protection_detection_buttons()
        self.set_start_button()
        self.start_pushed = False

    def set_up_protection_detection_buttons(self):
        self.mode = "Protection"
        self.protection_button = tk.Label(self.parent, image=protection_pushed_img, highlightthickness=0, borderwidth=0)
        self.protection_button.bind("<Button-1>", self.protection_button_pushed)
        self.protection_button_window = self.canvas.create_window(13, 258, anchor='nw', window=self.protection_button)
        self.detection_button = tk.Label(self.parent, image=detection_unpushed_img, highlightthickness=0, borderwidth=0)
        self.detection_button.bind("<Button-1>", self.detection_button_pushed)
        self.detection_button_window = self.canvas.create_window(140, 260, anchor='nw', window=self.detection_button)

    def detection_button_pushed(self, *args):
        self.mode = "Detection"
        self.protection_button.configure(image=protection_unpushed_img)
        self.detection_button.configure(image=detection_pushed_img)

    def protection_button_pushed(self, *args):
        self.mode = "Protection"
        self.detection_button.configure(image=detection_unpushed_img)
        self.protection_button.configure(image=protection_pushed_img)

    def set_sound_button(self):
        self.sound_button = tk.Label(self.parent, image=sound_off_icon, highlightthickness=0, borderwidth=0)
        self.sound_button.bind("<Button-1>", self.click_sound_button)
        self.sound_button_window = self.canvas.create_window(13, 284, anchor='nw', window=self.sound_button)

    def click_sound_button(self, *args):
        if self.soundMode:
            self.sound_button.configure(image=sound_off_icon)
            self.soundMode = False
        else:
            self.sound_button.configure(image=sound_on_icon)
            self.soundMode = True

    def set_start_button(self):
        self.start_button = tk.Label(self.parent, image=start_button_img, highlightthickness=0, borderwidth=0)
        self.start_button.bind("<Button-1>", self.start_button_pushed)
        self.start_button_window = self.canvas.create_window(78, 322,
                                                             anchor='nw',
                                                             window=self.start_button)

    def start_button_pushed(self, *args):
        self.start_pushed = True
        self.parent.destroy()
        return

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

    def top_bar_initialization(self):
        self.menu = tk.Menu(self.parent)
        self.parent.config(menu=self.menu)
        self.menu.add_command(label="Exit", command=self.parent.quit)
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="help & usage", command=self.help_key)
        self.helpmenu.add_command(label="about...", command=self.about)


def initalize_start_photo():
    global main_start_photo, sound_on_icon, sound_off_icon, help_img, \
        about_img, start_button_img, protection_pushed_img, \
        detection_pushed_img, protection_unpushed_img, detection_unpushed_img
    sound_on_icon_photo = Image.open("%sAudio_ON.png" % PATH_GUI_FOLDER)
    sound_off_icon_photo = Image.open(
        "%saudio_off.png" % PATH_GUI_FOLDER)
    start_photo = Image.open("%sBG.jpg" % PATH_GUI_FOLDER)
    help_photo = Image.open("%shelp_image.png" % PATH_GUI_FOLDER)
    about_photo = Image.open("%sabout_screen.jpg" % PATH_GUI_FOLDER)
    start_button_photo = Image.open(
        "%sstart.png" % PATH_GUI_FOLDER)

    protection_pushed_photo = Image.open(
        "%sprotection_on.png" % PATH_GUI_FOLDER)

    detection_pushed_photo = Image.open(
        "%sDetection_on.png" % PATH_GUI_FOLDER)

    protection_unpushed_photo = Image.open(
        "%sprotection_off.png" % PATH_GUI_FOLDER)

    detection_unpushed_photo = Image.open(
        "%sDetection_off.png" % PATH_GUI_FOLDER)

    main_start_photo = ImageTk.PhotoImage(start_photo)
    sound_on_icon = ImageTk.PhotoImage(sound_on_icon_photo)
    sound_off_icon = ImageTk.PhotoImage(sound_off_icon_photo)
    help_img = ImageTk.PhotoImage(help_photo)
    about_img = ImageTk.PhotoImage(about_photo)
    start_button_img = ImageTk.PhotoImage(start_button_photo)
    protection_pushed_img = ImageTk.PhotoImage(protection_pushed_photo)
    protection_unpushed_img = ImageTk.PhotoImage(protection_unpushed_photo)
    detection_pushed_img = ImageTk.PhotoImage(detection_pushed_photo)
    detection_unpushed_img = ImageTk.PhotoImage(detection_unpushed_photo)


def center_window(root):
    # Gets the requested values of the height and widht.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = round(root.winfo_screenwidth() / windowWidth - 1 / 2)
    positionDown = round(root.winfo_screenheight() / windowHeight - 0.5 / 2)
    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))


def create_start_menu(root):
    s = startMenu(root)
    root.title(ROOT_TITLE)
    return s


def run_start_window():
    root = tk.Tk()
    s = create_start_menu(root)
    root.mainloop()
    if s.start_pushed:
        return s.mode, s.soundMode
    return None, None
