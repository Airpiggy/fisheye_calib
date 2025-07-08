import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("camera_index", help="the index of your camera", type=int)
args = parser.parse_args()

calib_data = np.load("fisheye_calibration_result.npz")
K = calib_data["camera_matrix"]
D = calib_data["dist_coeffs"]
frame_width = int(calib_data["frame_width"])
frame_height = int(calib_data["frame_height"])
frame_size = (frame_width, frame_height)
print(type(frame_height))
print("successfully load calibration file data")

K_new = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K=K, 
                                                               D=D, 
                                                               image_size=frame_size, 
                                                               R=np.eye(3), 
                                                               balance=None)
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K=K, 
                                                 D=D,
                                                 R=np.eye(3),  
                                                 P=K_new, 
                                                 size=frame_size, 
                                                 m1type=cv2.CV_32FC1)

reference_points = np.array([[frame_width, frame_height/2], [frame_width/2, frame_height]], dtype=np.float32)
reference_points = reference_points.reshape(-1, 1, 2)
trans_reference_points = cv2.fisheye.undistortPoints(distorted=reference_points, 
                                                     K=K, 
                                                     D=D, 
                                                     R=np.eye(3), 
                                                     P=K_new)

map1_new, map2_new = cv2.fisheye.initUndistortRectifyMap(K=K, 
                                                         D=D,
                                                         R=np.eye(3),  
                                                         P=K_new, 
                                                         size=(int(trans_reference_points[0][0][0]), int(trans_reference_points[1][0][1])), 
                                                         m1type=cv2.CV_32FC1)

cap = cv2.VideoCapture(args.camera_index)

if cap.isOpened() is False:
    print("error opening the camera")

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        frame_corrected = cv2.remap(src=frame, 
                                    map1=map1_new, 
                                    map2=map2_new, 
                                    interpolation=cv2.INTER_LINEAR)
        cv2.imshow("orginal fisheye frame", frame)
        cv2.imshow("corrected frame", frame_corrected)
    else:
        print("error reading camera stream")

    key = cv2.waitKey(20) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()