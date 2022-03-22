import subprocess as sp
import cv2
import time
import numpy as np
from platform import system

if system() == "Windows":
    windows = True
else:
    windows = False


def press(x, y):
    sp.run(["adb", "-d", "shell", "input", "tap", x, y])


def calculate(prepared, result):
    mat_top, mat_left = result
    (
        prepared_height,
        prepared_width,
        prepared_channels,
    ) = prepared.shape  # missing channels
    x = str((mat_top + mat_top + prepared_width) / 2)
    y = str((mat_left + mat_left + prepared_height) / 2)
    return x, y


def find(img, timeout, click):
    screencap = ["adb", "-d", "shell", "screencap", "-p"]
    start = time.time()
    while True:
        pipe = sp.Popen(
            screencap,
            stdin=sp.PIPE,
            stdout=sp.PIPE,
        )
        if windows:
            image_bytes = pipe.stdout.read().replace(b"\r\n", b"\n")
        else:
            image_bytes = pipe.stdout.read()

        screenshot = cv2.imdecode(
            np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR
        )

        prepared = cv2.imread(str(img.resolve()))
        result = cv2.matchTemplate(screenshot, prepared, cv2.TM_CCORR_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        end = time.time()
        if max_val >= 0.992:
            x, y = calculate(prepared, max_loc)
            if click == True:
                press(x, y)
            return [True, x, y]
        elif timeout == 0:
            return [False]
        elif timeout == -1:
            pass
        elif (end - start) >= timeout:
            raise ButtonNotFound


class Timeout(Exception):
    # Raised when code times out
    pass


class ButtonNotFound(Timeout):
    # Raised when target button does not appear
    pass


class FailedToJoinLobby(Timeout):
    # Raised when joining lobby fails
    pass


class FailedToEnterGame(Timeout):
    # Raised when entering game fails
    pass


class FailedToCompleteGame(Timeout):
    # Raised when you die L
    pass
