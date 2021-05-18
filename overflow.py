import socket
import struct
import cv2
import math
import os


class FrameSegment():

    MAX_IMAGE_DGRAM = 2**16 - 64 # minus 64 bytes in case UDP frame overflown

    def __init__(self, port=5000, camNum=0, ip="192.168.1.255"):
        self.IP = ip
        self.cam = cv2.VideoCapture(camNum)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # for linux use SO_REUSEPORT
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # self.s.settimeout(0.2)
        self.PORT = port

    def __del__(self):
        self.cam.release()
        self.s.close()

    def send(self):
        while 1:
            _, img = self.cam.read()
            compress_img = cv2.imencode(".jpg", img)[1]
            dat = compress_img.tostring()
            size = len(dat)
            num_of_segments = math.ceil(size/(self.MAX_IMAGE_DGRAM))
            array_pos_start = 0

            while num_of_segments:
                array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
                self.s.sendto(
                            struct.pack("B", num_of_segments) +
                            dat[array_pos_start:array_pos_end], 
                            (self.IP, self.PORT)
                            )
                array_pos_start = array_pos_end
                num_of_segments -= 1


def isVideo(element):
    return True if element.startswith("video") else False

def getCams():

    cams = filter(isVideo, os.listdir("/dev/")) # gets list of video devices if isVideo finds them in os list
    camNums = []

    for cam in cams:
        res = ''.join(filter(lambda i: i.isdigit(), cam))
        camNums.append(int(res))

    return camNums