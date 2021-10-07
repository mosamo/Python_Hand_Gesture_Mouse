import time
import cv2

def display(img, pTime):
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
    return cTime
