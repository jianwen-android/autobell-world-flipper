from functions import *
from gui import *

imgSz = 530, 550
btnSz = 10, 1
padding = 0, 16


window = windowSetup(btnSz, imgSz, padding)  # Create the Window


def updateText(text="Placeholder text") -> None:
    # Updates the text of the window to display the appropriate sign
    window["outputText"].update(text)


def updateImg(src=None) -> None:
    # Updates the image of the window to display the appropriate sign
    window["signImg"].update(source=src, size=imgSz)
