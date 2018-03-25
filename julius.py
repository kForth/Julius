import time

import numpy as np
from PIL import Image
from mss import mss
import cv2

sct = mss()
test = False
x = 0
y = 0
z = 0
iter_x = 0
iter_y = 0
div = 10
should_block = False
last_histogram = None


def get_frame():
    img = None
    # TODO: Run on all monitor images.
    for num, monitor in enumerate(sct.monitors[1:], 1):
        img = sct.grab(monitor)
    img = np.array(Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX'))
    return cv2.resize(img, tuple([int(e / 3) for e in reversed(img.shape[:2])]))


def analyse_record(record):
    global iter_y
    global iter_x
    danger_counts = np.zeros((iter_x, iter_y), dtype=np.uint64)
    for dangerMap in record:
        danger_counts += dangerMap.astype(np.uint64)
    return np.any(np.greater(danger_counts, 5))


def precise_scan(new_frame):
    global iter_x, iter_y, div, last_histogram
    danger_map = np.zeros((iter_x, iter_y), dtype=np.bool)
    for X in range(0, iter_x):
        for Y in range(0, iter_y):
            new_hist = cv2.calcHist([new_frame[X * div:(X + 1) * div, Y * div:(Y + 1) * div]], [0], None, [256], [0, 256])
            old_hist = last_histogram[X, Y]
            if old_hist is not None:
                sc = cv2.compareHist(old_hist, new_hist, cv2.HISTCMP_HELLINGER)
                danger_map[X, Y] = sc > 0.95
            last_histogram[X, Y] = new_hist
    return danger_map


def draw_centered_text(img, text, font, scale, color, yPos):
    size = cv2.getTextSize(text, font, scale, 1)
    text_width = size[0][0]
    width = img.shape[1]
    cv2.putText(img, text, (int((width - text_width) / 2), int(yPos)), font, scale, color, 1, cv2.LINE_AA)


def block_screen():
    screen_width, screen_height = 1440, 900
    img = np.zeros((screen_height, screen_width), np.uint8)
    cv2.rectangle(img, (0, 0), (screen_width, screen_height), (50, 50, 50), -1)
    draw_centered_text(img, "Julius", cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 60)
    draw_centered_text(img, "Content Blocked", cv2.FONT_HERSHEY_SIMPLEX,
                       2, (255, 255, 255), screen_height / 2)
    draw_centered_text(img, "Protection Will Resume When This Window Closes", cv2.FONT_HERSHEY_SIMPLEX,
                       .75, (255, 255, 255), screen_height / 2 + 50)

    cv2.namedWindow("Julius", cv2.WINDOW_NORMAL)
    # cv2.setWindowProperty("Julius", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # This works well but kinda freezes on my system.
    cv2.imshow("Julius", img)
    cv2.waitKey(5000)
    cv2.destroyWindow("Julius")
    cv2.destroyAllWindows()
    cv2.waitKey(5)


def scan():
    global dangerMapRecord
    new_frame = get_frame()
    if new_frame is not None:
        dangerMapRecord.append(precise_scan(new_frame))
        if len(dangerMapRecord) > 10:
            dangerMapRecord.pop(0)
            if analyse_record(dangerMapRecord):
                block_screen()
                dangerMapRecord = []

if __name__ == "__main__":
    img_base = get_frame()
    iter_x, iter_y = [int(e / div) for e in img_base.shape[:2]]
    dangerMapRecord = []
    last_histogram = np.empty((iter_x, iter_y), dtype=np.ndarray)
    while True:
        start_time = time.time()
        scan()
        print("Frame took: {}s".format(round((time.time() - start_time), 3)))
