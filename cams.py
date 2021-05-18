import socket
import cv2
import numpy as np
import struct

class RovCam():

    MAX_DGRAM = 2**16 - 16

    def __init__(self,port=5000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # for linux use SO_REUSEPORT
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(("", port))
        self.dat = b''
        self.dump_buffer()
        print("ROV CAM : Connected successfully")

    def dump_buffer(self):
        while True:
            seg, addr = self.s.recvfrom(self.MAX_DGRAM)
            if struct.unpack("B", seg[0:1])[0] == 1:
                break

    def read(self):
        seg, addr = self.s.recvfrom(self.MAX_DGRAM)
        while struct.unpack("B", seg[0:1])[0] > 1:
            self.dat += seg[1:]
            seg, addr = self.s.recvfrom(self.MAX_DGRAM)
            
        self.dat += seg[1:]
        img = cv2.imdecode(np.fromstring(self.dat, dtype=np.uint8), 1)
        self.dat = b''
        return img