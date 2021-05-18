import cv2
import numpy as np
from cams import RovCam

feedSize = (1480, 820)

cam = RovCam(port=5000)
cam1 = RovCam(port=5100)

while 1:
	img = cam.read()
	img1 = cam1.read()

	collage = np.concatenate((img, img1), axis=1)
	fullSizeFeed = cv2.resize(collage, feedSize)

	cv2.imshow("ROV", fullSizeFeed)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
# cam.s.close()