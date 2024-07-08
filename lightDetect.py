import cv2
import numpy as np
from numpy.linalg import norm
import os
from PIL import Image

INPUT_FOLDER = "inputVids"
OUTPUT_FOLDER = "outputVids"

MIN_LIGHT_INTERVAL = 490
LIGHT_INTERVAL = 500
BASELINE = 250
HELPER_FRAMES = 10
LIGHT_OFF_MIN = 3750

BRIGHTNESS_CUTOFF = 92


def brightness_funct(img):
    if len(img.shape) == 3:
        return np.average(norm(img, axis=2)) / np.sqrt(3)
    else:
        return np.average(img)


def save_video(filename, iteration, start, end):
    cap = cv2.VideoCapture(INPUT_FOLDER + "/" + filename)
    cap.set(1, start)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    # CAN MODIFY OUTPUTS VIDEO NAMES (currently using "iteration")
    writer = cv2.VideoWriter(OUTPUT_FOLDER + "/Vid" + str(iteration) + ".avi", fourcc, 25.0, (494, 256))

    f = start
    ret, frame = cap.read()
    while start <= f <= end:
        frame = Image.fromarray(frame)
        frame = frame.resize((494, 256))
        frame = np.asarray(frame)
        writer.write(frame)
        f += 1
        ret, frame = cap.read()

    print("SAVED {}-{}".format(start, end))
    

def lightDetect(iteration, filename):
    cap = cv2.VideoCapture(INPUT_FOLDER + "/" + filename)
    vidLength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    index = 0
    lightDetect = False
    done = False

    success, img = cap.read()
    while index < vidLength - 1:

        brightness = brightness_funct(img)

        if not lightDetect:
            if brightness > BRIGHTNESS_CUTOFF:
                lightDetect = True
                max_index = index
                index = max(index - MIN_LIGHT_INTERVAL, 0)

            else:
                index = min(index + MIN_LIGHT_INTERVAL, vidLength - 1)

        else:
            if brightness > BRIGHTNESS_CUTOFF:
                lightDetect = False

                save_video(filename, iteration, index - BASELINE - HELPER_FRAMES,
                        index + LIGHT_INTERVAL + HELPER_FRAMES)

                iteration += 1
                index = min(index + LIGHT_INTERVAL + LIGHT_OFF_MIN, vidLength - 1)

            else:
                index += 1

        cap.set(1, index)
        success, img = cap.read()
    return iteration