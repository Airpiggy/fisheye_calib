import cv2
import argparse
import numpy as np

CHECKBOARD = (8, 5)
objp = np.zeros((1, CHECKBOARD[0]*CHECKBOARD[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0:CHECKBOARD[0], 0:CHECKBOARD[1]].T.reshape(-1, 2)
obj_points = []
img_points = []
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
img_size = (0, 0)
MINFIGURENUM = 50

parser = argparse.ArgumentParser()
parser.add_argument("camera_index", help="the index of your fisheye camera", type=int)
args = parser.parse_args()

cap = cv2.VideoCapture(args.camera_index)
if cap.isOpened() is False:
    print("Error opening the camera")

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray frame", gray_frame)

        ret_corners, corners = cv2.findChessboardCorners(gray_frame, CHECKBOARD)
        cv2.drawChessboardCorners(frame, CHECKBOARD, corners, ret_corners)
        cv2.imshow("corners finding result preview", frame)

        key = cv2.waitKey(20) & 0xFF
        if key == ord('s') and ret_corners:
            corners_optimized = cv2.cornerSubPix(gray_frame, corners, (3, 3), (-1, -1), criteria)
            obj_points.append(objp)
            img_points.append(corners_optimized)
            if len(obj_points) < MINFIGURENUM:
                print(f"{len(obj_points)} figures have been saved, still need {MINFIGURENUM - len(obj_points)} at least")
            else:
                print(f"{len(obj_points)} figures have been saved, enough for calibration")
  
        elif key == ord('q'):
            img_size = gray_frame.shape[::-1]
            print("stop saving figures, begin calibration")
            break

    else:
        print("Error reading frame from the camera")
        break

K = np.zeros((3, 3))
D = np.zeros((4, 1))

if len(obj_points) < MINFIGURENUM:
    print("not enough data for stable calibration")
elif len(obj_points) >= MINFIGURENUM:
    print("enough data for calibration")    
    ret_calib, K, D, _, _ = cv2.fisheye.calibrate(obj_points, 
                          img_points, 
                          img_size, 
                          K, 
                          D, 
                          flags=cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC | cv2.fisheye.CALIB_CHECK_COND | cv2.fisheye.CALIB_FIX_SKEW)
    print("K = ", K)
    print("D = ", D)
    np.savez_compressed("fisheye_calibration_result.npz", camera_matrix=K, dist_coeffs=D, frame_width=img_size[0], frame_height=img_size[1])
    print("calibration result has been saved to fisheye_calibration_result.npz")

cap.release()
cv2.destroyAllWindows()