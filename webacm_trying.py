#  Openpose 1.4.0  Handpose recognition via webcam
#  Requires OpenCV installed for Python
#  Hardcoded WebCam (0)

import ctypes  # An included library with Python install.
import math
import os
import sys
from sys import platform

import cv2
import numpy as np

import gui.AlertGui as alert
import gui.StartMenuGui as menu
import threading

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
if platform == "win32":
    # Change these variables to point to the correct folder (Release/x64 etc.)
    sys.path.append('openpose/python/openpose/Release');
    os.environ['PATH'] = os.environ['PATH'] + ';' + 'openpose/x64/Release;' + 'openpose/bin;'
    import pyopenpose as op

LEar = 17
REar = 18
Nose = 30
NoseBody = 0
Lchik = 2
Rchik = 14
Chin = 8
cam = cv2.VideoCapture(0)  # modify here for camera number




import tkinter as tk
from PIL import Image,ImageTk
import simpleaudio as sa


DisappearingFactor = 50
ALERT_NAME = "ambient_sound.wav"
#
# def center(win):
#     """
#     centers a tkinter window
#     :param win: the root or Toplevel window to center
#     """
#     win.update_idletasks()
#     width = win.winfo_width()
#     frm_width = win.winfo_rootx() - win.winfo_x()
#     win_width = width + 2 * frm_width
#     height = win.winfo_height()
#     titlebar_height = win.winfo_rooty() - win.winfo_y()
#     win_height = height + titlebar_height + frm_width
#     x = round((win.winfo_screenwidth() / 2) - (win_width / 2))
#     y = round((win.winfo_screenheight() / 2) - (win_height / 2))
#     win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
#     win.deiconify()


class maintenaceWindow:
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.top_bar_initialization()
        self.exit_button = tk.Button(parent, command=finish_and_exit)
        self.exit_button.pack()
    def help_key(self):
        self.help_window = tk.Toplevel(self.parent)
        self.help_window.title("help & usage")
        self.help_label = tk.Label(self.help_window, image=myimg)
        self.help_label.pack(fill=tk.BOTH)

    def about(self):
        self.about_window = tk.Toplevel(self.parent)
        self.about_window.title("about...")
        self.about_label = tk.Label(self.about_window, image=myimg)
        self.about_label.pack(fill=tk.BOTH)

    def top_bar_initialization(self):
        self.menu = tk.Menu(self.root)
        self.parent.config(menu=self.menu)
        # self.filemenu = tk.Menu(self.menu)
        # self.menu.add_cascade(label="File", menu=self.filemenu)
        self.menu.add_command(label="Exit", command=self.root.quit)
        self.helpmenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="help & usage",
                                  command=self.help_key)
        self.helpmenu.add_command(label="about...", command=self.about)




class AlertWindow:

    def __init__(self, parent,myimg, myroot, sound, mode):
        self.root = myroot
        self.parent = parent
        self.fading = False
        self.sound= sound
        self.mode = mode
        self.label_img = tk.Label(parent, image=myimg)
        # self.label_img.place(x=30, y=30,relwidth= 5,relheight = 5)
        self.label_img.pack(side=tk.TOP, fill=tk.BOTH)

        # self.label_img.pack(side=tk.TOP)

        self.b = tk.Button(self.parent, text="Click to fade away",
                           command=self.quit,
                      font= ("David", 28),height= 1, width = 7, bg="green",
                           )


        self.b.configure(activeforeground="red")

        self.detected = False
        self.counter = 1
        self.parent.wm_attributes('-alpha', 0)




    def quit(self):
        self.fade_away()

    def build(self):
        self.fade_in()

    def fade_in(self):
        alpha = self.parent.attributes("-alpha")
        if takeFrameAndCheckForTouch()[1]==2 or takeFrameAndCheckForTouch()[1]==3:
            if not self.detected:
                self.detected = True
                if self.sound:
                    self.set_and_play_song()
            if alpha < 1:
                alpha += .008
                self.parent.attributes("-alpha", alpha)
                self.parent.after(DisappearingFactor, self.fade_in)
            elif alpha==1:
                self.b.pack(side=tk.BOTTOM, fill=tk.BOTH)

        else:
            self.stop_song()
            self.detected=False
            self.parent.attributes("-alpha", 0)


    def fade_away(self):
        self.b.destroy()
        self.parent.attributes("-alpha", 0)

    def set_and_play_song(self):
        self.wave_obj = sa.WaveObject.from_wave_file(ALERT_NAME)
        self.play_obj = self.wave_obj.play()

    def stop_song(self):
        self.play_obj.stop()

def creating_transparent_window():
    root = tk.Tk()
    root.wait_visibility(root)
    root.wm_attributes('-alpha', 0.09)
    root.mainloop()


def finish_and_exit():

    # Always clean up
    cam.release()
    cv2.destroyAllWindows()


def creating_disappearing_button():
    root = tk.Tk()
    AlertWindow(root).pack(fill="both", expand=True)
    root.mainloop()


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
    dimg = Image.open("/Users/itamar/Desktop/mygui/jd.png")
    myimg = ImageTk.PhotoImage(dimg)


def create_alert_window(sound, mode):
    root = tk.Tk()
    root.iconify()
    intialize_photo()
    window = tk.Toplevel(root)
    window.overrideredirect(1)
    center_window(window)
    d = AlertWindow(window, myimg, root, sound, mode)
    d.build()
    program_window = maintenaceWindow(tk.Toplevel(root), root)
    window.mainloop()



def get_opWrapper_only_body():
    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../models/"
    params["net_resolution"] = "160x80"
    params["hand"] = False
    params["face"] = False
    params["body"] = 1

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    return opWrapper


def get_opWrapper_face():
    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../models/"
    params["net_resolution"] = "160x80"
    params["face"] = True
    params["face_detector"] = 0
    params["body"] = 1

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    return opWrapper


def get_opWrapper_hand():
    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "openpose/models/"
    params["net_resolution"] = "160x80"
    params["hand"] = True
    params["hand_detector"] = 3
    params["body"] = 1

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    return opWrapper


def draw_rectangle_around_face(face, frame, text):
    x, y, w, h = face
    color = (255, 0, 0)
    stroke = 2
    end_x = x + w
    end_y = y + h
    cv2.rectangle(frame, (x, y), (end_x, end_y), color, stroke)
    put_text_in_frame(face, frame, text)


def put_text_in_frame(face, frame, text):
    x, y, w, h = face
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)
    stroke = 2
    cv2.putText(frame, text, (x, y), font, 1, color, stroke, cv2.LINE_AA)


def calculate_rectangle_for_face(pose_coords):
    # distance between the two ears.
    LEarx, LEary = pose_coords[LEar]
    REarx, REary = pose_coords[REar]
    distance = REarx - LEarx
    rectangle_y = LEary - distance
    rectangle_x = LEarx - int(0.5 * distance)
    width = 2 * distance
    high = 2 * distance
    return rectangle_x, rectangle_y, width, high


def get_face_image_recognized(face, frame):
    """
    save only the face on the given frame.
    :param face: Tuple of four values x,y,w,h. where (x,y) are the location of the face "start" on the frame and w , h
    are the width and height respectively
    :param frame: frame where the face was detected.
    :return:
    """
    x, y, w, h = face
    # cut the face form the entire frame.
    only_face = frame[y:y + h, x: x + w]
    return only_face


def save_face_image_recognized(face, frame):
    """
    save only the face on the given frame.
    :param face: Tuple of four values x,y,w,h. where (x,y) are the location of the face "start" on the frame and w , h
    are the width and height respectively
    :param frame: frame where the face was detected.
    :return:
    """
    only_face = get_face_image_recognized(face, frame)
    cv2.imwrite("openpose/examples/tutorial_api_python/original.png", frame)
    cv2.imwrite("openpose/examples/tutorial_api_python/detected_face_.png", only_face)


def first_stage_rectangle():
    # Process Image
    datum = op.Datum()
    body_opWrapper = get_opWrapper_only_body()
    # Get camera frame
    ret, frame = cam.read()
    datum.cvInputData = frame
    body_opWrapper.emplaceAndPop([datum])
    pose_coords = np.array(datum.poseKeypoints[0, :, :2]).astype("int")
    rectangle_of_face = calculate_rectangle_for_face(pose_coords)
    save_face_image_recognized(rectangle_of_face, frame)
    draw_rectangle_around_face(rectangle_of_face, frame, "face")
    return rectangle_of_face


def first_stage_ellipse():
    datum_face = op.Datum()
    face_opWrapper = get_opWrapper_face()
    while True:
        ret, frame_face = cam.read()
        datum_face.cvInputData = frame_face
        face_opWrapper.emplaceAndPop([datum_face])
        if len(datum_face.faceKeypoints.shape) == 3:
            a, b = get_ellipse_a_b_by_face(np.array(datum_face.faceKeypoints[0, :, :2]).astype("int"))
            face_opWrapper.stop()
            return a, b


BGR_GREEN = (0, 255, 0)
BGR_RED = (0, 0, 255)
BGR_YELLOW = (0, 255, 255)
color_dict = {1: BGR_RED, 2: BGR_YELLOW, 3: BGR_GREEN}


def draw_ellipse_in_frame(center, axesLength, frame, level):
    angle = 0
    startAngle = 0
    endAngle = 360
    # Red color in BGR
    color = color_dict[level]
    # Line thickness of 1 px
    thickness = 1
    # Using cv2.ellipse() method
    # Draw a ellipse with red line borders of thickness of 1 px
    cv2.ellipse(frame, center, axesLength,
                angle, startAngle, endAngle, color, thickness)


def draw_ellipse_around_face(face, frame):
    NoseX, NoseY = face[Nose]
    axesLength = get_ellipse_a_b_by_face(face)
    draw_ellipse_in_frame((NoseX, NoseY), axesLength, frame, 1)


def get_ellipse_a_b_by_face(face_keypoints):
    NoseX, NoseY = face_keypoints[Nose]
    Lchikx, Lchiky = face_keypoints[Lchik]
    Rchikx, Rchiky = face_keypoints[Rchik]
    ChinX, ChinY = face_keypoints[Chin]
    axesXLen = (Rchikx - Lchikx) // 2
    axesYLen = ChinY - NoseY
    axesLength = (axesXLen, axesYLen)
    return axesLength


def get_ellipse_a_b_by_body(body_points):
    NoseX, NoseY = body_points[NoseBody]
    LEarx, LEary = body_points[LEar]
    REarx, REary = body_points[REar]
    axesXLen = max(REarx - NoseX, NoseX - LEarx)
    axesYLen = int(1.5 * axesXLen)
    axesLength = (axesXLen, axesYLen)
    return axesLength


def draw_ellipse_around_face_by_body(body_points, frame, level):
    NoseX, NoseY = body_points[NoseBody]
    axesX, axesY = get_ellipse_a_b_by_body(body_points)
    axesX = int(axesX * level)
    axesY = int(axesY * level)
    draw_ellipse_in_frame((NoseX, NoseY), (axesX, axesY), frame, level)


# Function to check the point
def checkPointInEllipse(centerX, centerY, a, b, x, y):
    # checking the equation of
    # ellipse with the given point
    p = ((math.pow((x - centerX), 2) / math.pow(a, 2)) +
         (math.pow((y - centerY), 2) / math.pow(b, 2)))
    print(p)
    return p <= 0.9


def calculate_hand_height_width(hand):
    baseX, baseY = hand[0]
    topX, topY = hand[9]
    height = abs(topY - baseY)
    left_edgeX, left_edgeY = hand[17]
    right_edgeX, right_edgeY = hand[12]
    width = abs(right_edgeX - left_edgeX)
    return height, width


def get_hand_coords(hand, axesXLen):
    # make us confidence we detected hand
    if np.average(hand[:, 2]) >= 0.5:
        hand_height, hand_width = calculate_hand_height_width(hand[:, :2])
        if hand_height < axesXLen and hand_width < axesXLen:
            return list(hand)
    return []


class alarmThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.alert_object = None
        self.end_alert = False

    def run(self):
        self.alert_object = alert.create_alert_window()
        self.alert_object.start_alarm()


alarm_thread = alarmThread()


def check_for_touch(body_points, left_hand, right_hand, frame_hand, I):
    NoseX, NoseY = body_points[NoseBody]
    axesXLen, axesYLen = get_ellipse_a_b_by_body(body_points)

    hand_coords = get_hand_coords(left_hand, axesXLen)
    hand_coords += get_hand_coords(right_hand, axesXLen)
    hand_coords = np.array(hand_coords)
    hand_coords = hand_coords[::-1]
    for hand in hand_coords:
        x, y, c = hand
        # if checkPointInEllipse(NoseX, NoseY, axesXLen * 3, axesYLen * 3, x, y):
        #     ctypes.windll.user32.MessageBoxW(0, "Stop touching your face level 3", "Alarm", 1)
        if checkPointInEllipse(NoseX, NoseY, axesXLen, axesYLen, x, y):
            ctypes.windll.user32.MessageBoxW(0, "Stop touching your face level 1", "Alarm", 1)
            return I,1

        elif checkPointInEllipse(NoseX, NoseY, axesXLen * 2, axesYLen * 2, x, y):
            # alarm_thread.alert_object.touchlevel = 1
            ctypes.windll.user32.MessageBoxW(0, "Stop touching your face level 2", "Alarm", 1)
            return I,2

    # draw_ellipse_around_face_by_body(body_points, frame_hand, 2)
    # draw_ellipse_around_face_by_body(body_points, frame_hand, 3)
    return I,3


def get_coords(datum_hand):
    pose_coords = np.array(datum_hand.poseKeypoints[0, :, :2])
    left_hand = datum_hand.handKeypoints[0]
    # print(left_hand)
    left_hand = np.array(left_hand[0, :, :])
    right_hand = datum_hand.handKeypoints[1]
    right_hand = np.array(right_hand[0, :, :])
    # hands_coords = np.concatenate((left_hand, right_hand))
    return pose_coords, left_hand, right_hand


# def run_face_detect(frame):
#     datum_face.cvInputData = frame
#     face_opWrapper.emplaceAndPop([datum_face])
#     return datum_face.cvOutputData


def run_hand_detect(frame):
    datum_hand.cvInputData = frame
    hand_opWrapper.emplaceAndPop([datum_hand])
    return datum_hand.cvOutputData


I = 0
frame_number = 0
# a, b = first_stage_ellipse()
# rectangle_of_face = first_stage()


# Process Image
# datum_face = op.Datum()
datum_hand = op.Datum()
# face_opWrapper = get_opWrapper_face()
hand_opWrapper = get_opWrapper_hand()


def start(detector_mode, with_sound):
    global I
    ret, frame = cam.read()
    frame_hand = run_hand_detect(frame)
    # frame_face = run_face_detect(frame)
    if len(datum_hand.poseKeypoints.shape) == 3:
        pose_coords, left_hand, right_hand = get_coords(datum_hand)
        I = check_for_touch(pose_coords, left_hand, right_hand, frame_hand, I)

        # cv2.imshow("Openpose 1.4.0 Webcam", frame_face)  # datum.cvOutputData)
        # cv2.imshow("Openpose 1.4.0 Webcam", frame_hand)  # datum.cvOutputData)


    # Always clean up
    cam.release()
    cv2.destroyAllWindows()


def takeFrameAndCheckForTouch():
    I=0
    ret, frame = cam.read()
    frame_hand = run_hand_detect(frame)
    # frame_face = run_face_detect(frame)
    if len(datum_hand.poseKeypoints.shape) == 3:
        pose_coords, left_hand, right_hand = get_coords(datum_hand)
        I = check_for_touch(pose_coords, left_hand, right_hand, frame_hand, 0)
    return I, None

def main():
    mode, with_sound = menu.run_start_window()
    create_alert_window(with_sound,mode)



if __name__ == '__main__':
    main()
