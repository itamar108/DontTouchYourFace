import math
import os
import sys
from sys import platform
import cv2
import numpy as np
import gui.AlertGui as alert
import gui.StartMenuGui as menu
import GraphicTools

HAND_RIGHT_EDGE_POINT = 12

HAND_LEFT_EDGE_POINT = 17

HAND_TOP_POINT = 9

HAND_BASE_POINT = 0

NO_HAND_DETECTED = -1

IN_ELLIPSE_THRESHOLD = 0.9

HAND_DETECTION_CONFIDENCE_THRESHOLD = 0.5

NO_TOUCH = 4

TOUCH_LEVEL_THREE = 3

TOUCH_LEVEL_ONE = 1

TOUCH_LEVEL_TWO = 2

HAND_DISTANCE_THRESHOLD = 3
HAND_DISTANCE_THRESHOLD_FACTOR = 1.5

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


class Detector:

    def __init__(self, mode, with_sound):
        self.cam = cv2.VideoCapture(0)  # modify here for camera number
        self.datum_hand = op.Datum()
        self.hand_opWrapper = self.get_opWrapper_hand()
        self.mode = mode
        self.with_sound = with_sound

    def check_single_frame(self):
        ret, frame = self.cam.read()
        frame_hand = self.run_hand_detect(frame)
        if len(self.datum_hand.poseKeypoints.shape) == 3:
            pose_coords, left_hand, right_hand = self.get_coords()
            level = self.check_for_touch(pose_coords, left_hand, right_hand, frame_hand)
            # cv2.imshow("Openpose 1.4.0 Webcam", frame_hand)  # datum.cvOutputData)
            return level
        return NO_HAND_DETECTED

    def run_hand_detect(self, frame):
        self.datum_hand.cvInputData = frame
        self.hand_opWrapper.emplaceAndPop([self.datum_hand])
        return self.datum_hand.cvOutputData

    def get_opWrapper_hand(self):
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

    def get_coords(self):
        pose_coords = np.array(self.datum_hand.poseKeypoints[0, :, :2])
        left_hand = self.datum_hand.handKeypoints[0]
        left_hand = np.array(left_hand[0, :, :])
        right_hand = self.datum_hand.handKeypoints[1]
        right_hand = np.array(right_hand[0, :, :])
        return pose_coords, left_hand, right_hand

    def check_for_touch(self, body_points, left_hand, right_hand, frame_hand):
        NoseX, NoseY = body_points[NoseBody]
        axesXLen, axesYLen = GraphicTools.get_ellipse_a_b_by_body(body_points)
        # there is tradeoff between false alarms and false alarms which here we can tune it
        # by changing the threshold
        hand_coords = self.get_hand_coords(left_hand, HAND_DISTANCE_THRESHOLD_FACTOR * axesXLen)
        hand_coords += self.get_hand_coords(right_hand, HAND_DISTANCE_THRESHOLD_FACTOR * axesXLen)
        hand_coords = np.array(hand_coords)
        level_three_touch = 0
        n = len(hand_coords)
        for i in range(0, n):
            index = n - 1 - i
            hand = hand_coords[index]
            level = self.check_level_of_touch(NoseX, NoseY, axesXLen, axesYLen, hand, level_three_touch)
            if level != NO_TOUCH:
                return level
            # draw_ellipse_around_face_by_body(body_points, frame_hand, 1)
        return NO_TOUCH

    def check_level_of_touch(self, NoseX, NoseY, axesXLen, axesYLen, hand, level_three_touch):
        x, y, c = hand
        if self.checkPointInEllipse(NoseX, NoseY, axesXLen, axesYLen, x, y):
            return TOUCH_LEVEL_ONE
        elif self.checkPointInEllipse(NoseX, NoseY, axesXLen * TOUCH_LEVEL_TWO, axesYLen * TOUCH_LEVEL_TWO, x, y):
            return TOUCH_LEVEL_TWO
        elif self.checkPointInEllipse(NoseX, NoseY, axesXLen * 2.5, axesYLen * 2.5, x, y):
            level_three_touch += 1
            if level_three_touch == HAND_DISTANCE_THRESHOLD:
                return TOUCH_LEVEL_THREE
        return NO_TOUCH

    def get_hand_coords(self, hand, threshold):
        # make us confidence we detected hand
        if np.average(hand[:, 2]) >= HAND_DETECTION_CONFIDENCE_THRESHOLD:
            hand_height, hand_width = self.calculate_hand_height_width(hand[:, :2])
            if hand_height < threshold and hand_width < threshold:
                return list(hand)
        return []

    def calculate_hand_height_width(self, hand):
        baseX, baseY = hand[HAND_BASE_POINT]
        topX, topY = hand[HAND_TOP_POINT]
        height = abs(topY - baseY)
        left_edgeX, left_edgeY = hand[HAND_LEFT_EDGE_POINT]
        right_edgeX, right_edgeY = hand[HAND_RIGHT_EDGE_POINT]
        width = abs(right_edgeX - left_edgeX)
        return height, width

    # Function to check the point
    def checkPointInEllipse(self, centerX, centerY, a, b, x, y):
        # checking the equation of
        # ellipse with the given point
        p = ((math.pow((x - centerX), 2) / math.pow(a, 2)) +
             (math.pow((y - centerY), 2) / math.pow(b, 2)))
        return p <= IN_ELLIPSE_THRESHOLD


def main():
    mode, with_sound = menu.run_start_window()
    if mode is None:
        return
    d = Detector(mode, with_sound)
    alert.set_up_gui(d)
    d.cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
