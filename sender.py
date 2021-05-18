from cams import RovCam
import cv2

cam = RovCam(port=5000)

while True:
	frame = cam.read()

	cv2.imshow("UAV", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
cam.s.close()