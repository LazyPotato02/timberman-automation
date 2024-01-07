import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui

pyautogui.PAUSE = 0

print("Press 's' to start playing.")
print("Once started press 'q' to quit.")
keyboard.wait('s')
left = True
x = 340
y = 850
sct = mss.mss()
dimensions_left = {
    'left': 290,
    'top': 450,
    'width': 350,
    'height': 400
}

dimensions_right = {
    'left': 520,
    'top': 450,
    'width': 350,
    'height': 400
}

# wood_left = cv2.imread('woodleft.jpg')
#
# wood_right = cv2.imread('woodright.jpg')


wood_left = cv2.imread('leftpiece.jpg')

wood_right = cv2.imread('rightpiece.jpg')
w = wood_left.shape[1]
h = wood_left.shape[0]

fps_time = time()
while True:

    if left:
        scr = numpy.array(sct.grab(dimensions_left))
        wood = wood_left
    else:
        scr = numpy.array(sct.grab(dimensions_right))
        wood = wood_right

    # Cut off alpha
    scr_remove = scr[:, :, :3]

    result = cv2.matchTemplate(scr_remove, wood, cv2.TM_CCOEFF_NORMED)

    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(f"Max Val: {max_val} Max Loc: {max_loc}")
    src = scr.copy()
    if max_val > .85:
        left = not left
        if left:
            x = 310
        else:
            x = 640
        cv2.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 255), 2)

    cv2.imshow('Screen Shot', scr)
    cv2.waitKey(1)
    if left:
        pyautogui.click(x=x, y=y)
    else:
        pyautogui.rightClick(x=x, y=y)
    sleep(.10)
    if keyboard.is_pressed('q'):
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()