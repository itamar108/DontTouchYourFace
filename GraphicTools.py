import cv2

from DontTouchYourFace import LEar, REar, Nose, Lchik, Rchik, Chin, NoseBody


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
    cv2.ellipse(frame, center, axesLength, angle, startAngle, endAngle, color, thickness)


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
    draw_ellipse_in_frame((NoseX, NoseY), (axesX, axesY), frame, int(level))