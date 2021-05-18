import cv2
import socket
import sys
from time import sleep
from overflow import FrameSegment, getCams

# get camera indexes from linux device directory
camNums = getCams()

while True:
    # run until the correct number of cameras are connected
    while len(camNums) < 1:
        print("- Camera not detected, Restarting.")
        sleep(5)
        camNums = getCams()

    try:
        fs = FrameSegment(port=5000, camNum=camNum)
        cam.send()
        print("- Started streaming")
    except  KeyboardInterrupt:
        print("- Exiting")
        break

    except Exception:
        print("- Unkown error, exiting")

del cam