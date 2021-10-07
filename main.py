import cv2
import numpy as np
import pyautogui

import HandTrackingModule as htm

import autopy
import fps_module as fps

cam_width = 640
cam_height = 480

# fetches my screen width and height
screen_width, screen_height = autopy.screen.size()

frameReduction = 115

# smoothening variables
smoothening = 5
previousX, previousY = 0, 0
currentX, currentY = 0, 0

previousTime = 0

cap = cv2.VideoCapture(0)

cap.set(3, cam_width)
cap.set(4, cam_height)

detector = htm.handDetector(maxHands=1)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and thumb fingers
    if len(lmList) > 0:
        # list[1:] notation skips first value (which is id in our case)
        inX, inY = lmList[8][1:]
        thmX, thmY = lmList[4][1:]

        # print(f'Index Finger Coordinates: ({inX}, {inY})')
        # print(f'Thumb Finger Coordinates: ({thmX}, {thmY})')

    # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(f'Fingers Up: {fingers}')

    # 4. Index Finger Up and Thumb Down: Moving Mode: On ([0] is thumb, [1] is index)
        if fingers[1] == 1 and fingers[0] == 0:

    # 5. Convert Coordinates
            InterpolatedX = np.interp(inX, (frameReduction, cam_width - frameReduction), (0, screen_width))
            InterpolatedY = np.interp(inY, (frameReduction, cam_height - frameReduction), (0, screen_height))
    # 6. Smoothen Values
            currentX = previousX + (InterpolatedX - previousX) / smoothening
            currentY = previousY + (InterpolatedY - previousY) / smoothening
    # 7. Move Mouse
            autopy.mouse.move(screen_width - currentX, currentY)
            # draw objects
            cv2.circle(img, (inX, inY), 15, (255, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (frameReduction, frameReduction), (cam_width - frameReduction, cam_height - frameReduction), (0, 255, 255), 3)

            previousX, previousY = currentX, currentY
    # 8. Index and Middle Fingers Up and Close, Thumb is Down: Clicking Mode
        if fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 1:
    # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)  # distance between Index and Middle Ends
    # 10. Click mouse if the distance between fingers is short
            if length < 20:
                cv2.circle(img, lineInfo[4:], 10, (0, 255, 255), cv2.FILLED)
                # print("Click Coordinates:", lineInfo[4:])  # equivalent to (lineInfo[4], lineInfo[5])
                pyautogui.click()

    # 11. Frame Rate Display
    previousTime = fps.display(img, previousTime)

    # 12. Display Results
    cv2.imshow("Output", img)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break