import numpy as np
import cv2

capture = cv2.VideoCapture("slow_traffic.mkv")

# take first frame of the video
ret, frame = capture.read()

# setup initial location of window
x, y, width, height = 300, 200, 100, 50
track_window = (x, y, width, height)

# set up the ROI for tracking
roi = frame[y:y+height, x:x+width]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
cv2.imshow('roi', roi)

while True:
    ret, frame = capture.read()
    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # apply mean-shift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # draw it on image
        x, y, w, h = track_window
        final_image = cv2.rectangle(frame, (x, y), (x+w, y+h), 255, 3)

        cv2.imshow('dst', dst)
        cv2.imshow('final_image', final_image)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break
