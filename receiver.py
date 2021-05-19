import cv2
import numpy as np
from cams import RovCam

cam = RovCam(port=5000)

while 1:
	try:
		img = cam.read()

		cv2.imshow("UAV", img)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	except:
		countinue

cv2.destroyAllWindows()
