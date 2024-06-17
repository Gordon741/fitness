import numpy as np
import cv2
import time
import math

import cvzone
from cvzone.PoseModule import PoseDetector


cap = cv2.VideoCapture(0)

ctime = 0
ptime = 0
direction = 0
push_ups = 0

# --------------------------- rgb(37, 150, 190)
b_color = (0, 0, 0)
blue_color = (190, 150, 37)


detector = PoseDetector()
while True:
    _, img = cap.read()
    img = detector.findPose(img)
    lmlist, bbox = detector.findPosition(img, draw=False)
    if lmlist:
        point1 = lmlist[11]
        point2 = lmlist[13]
        point3 = lmlist[15]
        point4 = lmlist[12]
        point5 = lmlist[14]
        point6 = lmlist[16]

        x1, y1 = point1[0:-1]
        x2, y2 = point2[0:-1]
        x3, y3 = point3[0:-1]
        x4, y4 = point4[0:-1]
        x5, y5 = point5[0:-1]
        x6, y6 = point6[0:-1]

        a1 = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                         math.atan2(y1 - y2, x1 - x2))
        
        a2 = math.degrees(math.atan2(y6 - y5, x6 - x5) -
                                          math.atan2(y4 - y5, x4 - x5))

        per_val1 = int(np.interp(a1, (90, 170), (100, 0)))
        per_val2 = int(np.interp(a2, (90, 170), (100, 0)))

        bar_val1 = int(np.interp(per_val1, (0, 100), (40+350, 40)))
        bar_val2 = int(np.interp(per_val2, (0, 100), (40+350, 40)))

        # 1st bar
        cv2.rectangle(img, (570, bar_val1), (570 + 35, 40 + 350), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (570, 40), (570 + 35, 40+350), (), 2)

        # 2st bar
        cv2.rectangle(img, (35, bar_val2), (35 + 35, 40 + 350), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (35, 40), (35 + 35, 40 + 350), (), 2)

        # bar %
        cvzone.putTextRect(img, f"{per_val1} %", (570, 25), 1.3, 2, colorT=blue_color, colorR=(255, 255, 255), border=1, colorB=b_color)  # (B,G,R)
        cvzone.putTextRect(img, f"{per_val2} %", (25, 25), 1.3, 2, colorT=blue_color, colorR=(255, 255, 255), border=1, colorB=b_color)  # (B,G,R)

        if per_val1 == 100 and per_val2 == 100:
            if direction == 0:
                push_ups += 0.5
                direction = 1
                color = (0, 255, 0)

        elif per_val1 == 0 and per_val2 == 0:
            if direction == 1:
                push_ups += 0.5
                direction = 0
                color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        cvzone.putTextRect(img, f"Push_ups : {int(push_ups)}", (200, 35), 2, 2, colorT=(0, 0, 255), colorR=(0, 255, 0), colorB=(), border=1)
        cvzone.putTextRect(img, "Left Hand", (15, 350+100), 1.5, 2, colorT=(255, 255, 255), colorR=blue_color, colorB=b_color, border=1)
        cvzone.putTextRect(img, "Right Hand", (485, 350+100), 1.5, 2, colorT=(255, 255, 255), colorR=blue_color, colorB=b_color, border=1)

        print(push_ups)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    # cvzone.putTextRect(img, f"FPS :{int(fps)}", (288, 440), 1.5, 1, colorT=(255, 255, 255), colorR=(1, 155, 0), border=2,colorB=(0, 0, 0))

    cv2.imshow("Posh-ups Counter", img)
    if cv2.waitKey(1) == ord("q"):
        break

