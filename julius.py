import time

import cv2
import numpy as np
from PIL import Image
from mss import mss


class JuliusMonitor:
    def __init__(self):
        self.sct = mss()
        self.period = 0.0625  # 16Hz
        self.x = 0
        self.y = 0
        self.z = 0
        self.div = 10

        self.iter_x = {}
        self.iter_y = {}
        self.last_histograms = {}
        self.dangerMapRecord = []
        for mon_num, mon in self.get_monitors():
            img_base = self.get_frame(mon)
            self.iter_x[mon_num], self.iter_y[mon_num] = [int(e / self.div) for e in img_base.shape[:2]]
            self.last_histograms[mon_num] = np.empty((self.iter_x[mon_num], self.iter_y[mon_num]), dtype=np.ndarray)

    def get_frame(self, mon):
        img = self.sct.grab(mon)
        img = np.array(Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX'))
        return cv2.resize(img, tuple([int(e / 3) for e in reversed(img.shape[:2])]))

    def analyse_record(self, record, mon_num):
        danger_counts = np.zeros((self.iter_x[mon_num], self.iter_y[mon_num]), dtype=np.uint64)
        for dangerMap in record:
            danger_counts += dangerMap.astype(np.uint64)
        return np.any(np.greater(danger_counts, 5))

    def precise_scan(self, mon_num, new_frame):
        danger_map = np.zeros((self.iter_x[mon_num], self.iter_y[mon_num]), dtype=np.bool)
        for X in range(0, self.iter_x[mon_num]):
            for Y in range(0, self.iter_y[mon_num]):
                new_hist = cv2.calcHist([new_frame[X * self.div:(X + 1) * self.div, Y * self.div:(Y + 1) * self.div]],
                                        [0], None, [256], [0, 256])
                old_hist = self.last_histograms[mon_num][X, Y]
                if old_hist is not None:
                    sc = cv2.compareHist(old_hist, new_hist, cv2.HISTCMP_HELLINGER)
                    danger_map[X, Y] = sc > 0.95
                self.last_histograms[mon_num][X, Y] = new_hist
        return danger_map

    def draw_centered_text(self, img, text, font, scale, color, yPos):
        size = cv2.getTextSize(text, font, scale, 1)
        text_width = size[0][0]
        width = img.shape[1]
        cv2.putText(img, text, (int((width - text_width) / 2), int(yPos)), font, scale, color, 1, cv2.LINE_AA)

    def block_screen(self, mon):
        screen_width, screen_height = mon["width"], mon["height"]
        img = np.zeros((screen_height, screen_width), np.uint8)
        cv2.rectangle(img, (0, 0), (screen_width, screen_height), (50, 50, 50), -1)
        self.draw_centered_text(img, "Julius", cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 60)
        self.draw_centered_text(img, "Content Blocked", cv2.FONT_HERSHEY_SIMPLEX,
                                2, (255, 255, 255), screen_height / 2)
        self.draw_centered_text(img, "Protection Will Resume When This Window Closes", cv2.FONT_HERSHEY_SIMPLEX,
                                .75, (255, 255, 255), screen_height / 2 + 50)

        cv2.namedWindow("Julius", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Julius", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # This works well but kinda freezes on my system.
        cv2.imshow("Julius", img)
        cv2.waitKey(5000)
        cv2.destroyWindow("Julius")
        cv2.destroyAllWindows()
        cv2.waitKey(5)

    def get_monitors(self):
        return enumerate(self.sct.monitors[1:], 1)

    def scan(self):
        for mon_num, mon in self.get_monitors():
            frame = self.get_frame(mon)
            self.dangerMapRecord.append(self.precise_scan(mon_num, frame))
            if len(self.dangerMapRecord) > 10:
                self.dangerMapRecord.pop(0)
                if self.analyse_record(self.dangerMapRecord, mon_num):
                    self.block_screen(mon)
                    self.dangerMapRecord = []

    def run(self, is_running, print_time):
        while is_running():
            start_time = time.time()
            self.scan()
            if print_time():
                print("Frame took: {}s".format(round((time.time() - start_time), 3)))
            time.sleep(max(0, self.period - (time.time() - start_time)))

if __name__ == "__main__":
    monitor = JuliusMonitor()
    monitor.run(lambda: True, lambda: True)
