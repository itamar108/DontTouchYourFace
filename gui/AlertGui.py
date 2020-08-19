import tkinter as tk
from PIL import Image, ImageTk
import simpleaudio as sa
from gui.MaintenanceWindow import MaintenanceWindow

NO_HAND_DETECTED = -1

NO_TOUCH = 4

TOUCH_LEVEL_ONE = 1

TOUCH_LEVEL_TWO = 2

TOUCH_LEVEL_THREE = 3

LEVEL_TWO_BRIGHTNESS = 0.55

LEVEL_THREE_BRIGHTNESS = 0.4

LEVEL_ONE_BRIGHTNESS = 1

INITIAL_LEVEL_BRIGHTNESS = 0.1

PATH_GUI_FOLDER = "C:\\Users\\ASUS\\PycharmProjects\\Dont_touch_your_face\\gui\\"

DisappearingFactor = 1
ALERT_NAME = PATH_GUI_FOLDER + "ambient_sound.wav"


class AlertWindow:
    INCREMENT_FACTOR = 0.15

    def __init__(self, parent, myimg, myroot, detector_obj, maintenaceWindow_obj):
        self.root = myroot
        self.parent = parent
        self.label_img = tk.Label(parent, image=myimg)
        self.label_img.pack(side=tk.TOP, fill=tk.BOTH)
        self.b = tk.Button(self.parent, text="Click to fade away", command=self.quit, font=("David", 28), height=1,
                           width=7, bg="green", )
        self.b.configure(activeforeground="red")
        self.parent.wm_attributes('-alpha', 0)
        self.detector_obj = detector_obj
        self.wave_obj = sa.WaveObject.from_wave_file(ALERT_NAME)
        self.song_on = False
        self.maintenaceWindow = maintenaceWindow_obj

    def set_and_play_song(self):
        self.play_obj = self.wave_obj.play()
        self.song_on = True

    def quit(self):
        self.fade_away()

    def start_alarm(self):
        if self.detector_obj.mode == "Protection":
            self.fade_in_protection()
        else:
            self.fade_in_detection()

    def fade_in_protection(self):
        level = self.detector_obj.check_single_frame()
        if level == NO_TOUCH or level == NO_HAND_DETECTED:
            self.fade_away()
            self.parent.after(DisappearingFactor, self.fade_in_protection)
        else:
            self.update_alert_brightness_parameter(level)

    def update_alert_brightness_parameter(self, level):
        alpha = self.parent.attributes("-alpha")
        if alpha == 0:
            alpha = INITIAL_LEVEL_BRIGHTNESS
            print(self.maintenaceWindow.sound_on)
            if self.maintenaceWindow.sound_on:
                self.set_and_play_song()
        else:
            if level == TOUCH_LEVEL_THREE:
                if alpha < LEVEL_THREE_BRIGHTNESS:
                    alpha += AlertWindow.INCREMENT_FACTOR
                else:
                    alpha = LEVEL_THREE_BRIGHTNESS
            elif level == TOUCH_LEVEL_TWO:
                if alpha < LEVEL_TWO_BRIGHTNESS:
                    alpha += AlertWindow.INCREMENT_FACTOR
                else:
                    alpha = LEVEL_TWO_BRIGHTNESS
            elif level == TOUCH_LEVEL_ONE:
                if alpha < LEVEL_ONE_BRIGHTNESS:
                    alpha += AlertWindow.INCREMENT_FACTOR
                else:
                    alpha = LEVEL_ONE_BRIGHTNESS
        self.parent.attributes("-alpha", alpha)
        self.parent.after(DisappearingFactor, self.fade_in_protection)

    def fade_away(self):
        if self.song_on:
            self.play_obj.stop()
            self.song_on = False
        self.parent.attributes("-alpha", 0)

    def fade_in_detection(self):
        level = self.detector_obj.check_single_frame()
        if level == TOUCH_LEVEL_ONE:
            if self.maintenaceWindow.sound_on and not self.song_on:
                self.set_and_play_song()
            self.parent.attributes("-alpha", 1)
            self.b.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.parent.after(DisappearingFactor, self.fade_in_detection)


def center_window(root):
    # Gets the requested values of the height and widht.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = round(root.winfo_screenwidth() / 2.3 - windowWidth / 2)
    positionDown = round(root.winfo_screenheight() / 3 - windowHeight / 2)
    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))


def center_window_secondWay(root):
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))


def intialize_photo():
    global myimg
    dimg = Image.open("%sjd.png" % PATH_GUI_FOLDER)
    myimg = ImageTk.PhotoImage(dimg)


def set_up_gui(detector_obj):
    root = tk.Tk()
    root.iconify()
    intialize_photo()
    maintenance_window = create_maintenance_window(root, detector_obj.with_sound)
    d = create_alert_window(detector_obj, maintenance_window, root)
    d.start_alarm()
    d.parent.mainloop()
    d.root.mainloop()
    return


def create_alert_window(detector_obj, maintenance_window, root):
    window = tk.Toplevel(root)
    window.overrideredirect(1)
    center_window(window)
    window.attributes('-topmost', True)
    window.update()
    d = AlertWindow(window, myimg, root, detector_obj, maintenance_window)
    return d


def create_maintenance_window(root, sound_mode):
    prog_window = tk.Toplevel(root)
    prog_window.attributes('-topmost', True)
    prog_window.overrideredirect(1)
    maintenance_window = MaintenanceWindow(prog_window, root, sound_mode)
    return maintenance_window
