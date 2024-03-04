import cv2
import csv
import math
import screen_brightness_control as sbc
from datetime import datetime
import time
import numpy as np
import pyautogui
from PIL import Image

LOG_FILE = 'brightness_log.csv'


def turn_on_keyboard_backlight():
    # Тази функция трябва да бъде имплементирана в зависимост от операционната система
    pass


def calculate_smoothing_factor(brightness_diff):
    return max(0.05, min(0.3, 1 / (1 + brightness_diff)))


def calculate_debounce_time(brightness_diff):
    return max(1, min(5, brightness_diff * 0.5))


def calculate_adaptive_threshold(smoothed_brightness):
    return max(5, min(20, smoothed_brightness * 0.1))


def analyze_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    brightness = sum(i * hist[i][0] for i in range(256)
                     ) / sum(hist[i][0] for i in range(256))
    return brightness / 256 * 100


def get_screenshot_brightness():
    # Вземане на скрийншот и анализ на неговата яркост
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([screenshot], [0], None, [256], [0, 256])
    brightness = sum(i * hist[i][0] for i in range(256)
                     ) / sum(hist[i][0] for i in range(256))
    return brightness / 256 * 100


def adjust_screen_brightness(camera_index=0):
    # Получаване на текущата яркост на екрана
    prev_brightness = sbc.get_brightness()[0]
    prev_time = None
    smoothed_brightness = prev_brightness

    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("Cannot open camera. Exiting...")
            return

        with open(LOG_FILE, 'w', newline='') as logfile:
            logwriter = csv.writer(logfile)
            logwriter.writerow(['timestamp', 'raw_brightness', 'smoothed_brightness',
                               'smoothing_factor', 'debounce_time', 'threshold'])

            while True:
                # Анализ на яркостта от камерата
                ret, frame = cap.read()
                if not ret:
                    camera_brightness = prev_brightness
                else:
                    camera_brightness = analyze_image(frame)

                # Анализ на яркостта от скрийншот
                screenshot_brightness = get_screenshot_brightness()

                # Комбиниране на двете стойности за яркост
                brightness = (camera_brightness + screenshot_brightness) / 2
                brightness_diff = abs(brightness - prev_brightness)

                if brightness_diff >= calculate_adaptive_threshold(smoothed_brightness):
                    smoothing_factor = calculate_smoothing_factor(
                        brightness_diff)
                    smoothed_brightness = smoothing_factor * brightness + \
                        (1 - smoothing_factor) * prev_brightness
                    debounce_time = calculate_debounce_time(brightness_diff)
                    current_time = datetime.now()

                    if prev_time is None or (current_time - prev_time).total_seconds() >= debounce_time:
                        sbc.set_brightness(math.ceil(smoothed_brightness))
                        print(f'New brightness: {math.ceil(smoothed_brightness)}% at {
                              current_time.strftime("%H:%M:%S")}, debounce time: {debounce_time:.2f}, smoothing factor: {smoothing_factor:.2f}')

                        if smoothed_brightness < 20:
                            turn_on_keyboard_backlight()

                        log_data = [current_time.strftime('%Y-%m-%d %H:%M:%S'), brightness, smoothed_brightness,
                                    smoothing_factor, debounce_time, calculate_adaptive_threshold(smoothed_brightness)]
                        logwriter.writerow(log_data)

                        prev_time = current_time

                prev_brightness = smoothed_brightness
                time.sleep(1)

    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    adjust_screen_brightness()
