

import cv2
import csv
import math
import screen_brightness_control as sbc
import time
import numpy as np
from datetime import datetime

LOG_FILE = 'brightness_log.csv'

def print_screen_brightness():
    # Използване на библиотеката screen_brightness_control за печат на текущата яркост (в проценти - закръглена нагоре до най-близкото цяло число) на екрана и часа корекция
    print(f"Текуща яркост на екрана: {sbc.get_brightness()}% в {datetime.now().strftime('%H:%M:%S')} часа.")


def calculate_smoothing_factor(brightness_diff):
    return max(0.05, min(0.3, 1/(1+brightness_diff)))


def calculate_debounce_time(brightness_diff):
    return max(1, min(5, brightness_diff * 0.5))


def calculate_adaptive_threshold(smoothed_brightness):
    return max(5, min(20, smoothed_brightness * 0.1))


def analyze_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Анализ на хистограма
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    brightness = calculate_histogram_brightness(hist)

    return brightness


def calculate_histogram_brightness(hist):
  max_bin_index = np.argmax(hist)
  brightness = max_bin_index / 255 * 100  # Сканирайте до 0-100 диапазон
  return brightness



def adjust_screen_brightness(camera_index=0):
    prev_brightness = 50
    prev_time = None
    smoothed_brightness = 50

    cap = cv2.VideoCapture(camera_index)
    log_headers = ['timestamp', 'raw_brightness', 'smoothed_brightness',
                   'smoothing_factor', 'debounce_time', 'threshold']

    with open(LOG_FILE, 'w') as logfile:
        logwriter = csv.writer(logfile)
        logwriter.writerow(log_headers)

        while True:
            ret, frame = cap.read()

            if not ret:
               continue

            brightness = analyze_image(frame)

            brightness_diff = abs(brightness - prev_brightness)

            smoothing_factor = calculate_smoothing_factor(brightness_diff)
            smoothed_brightness = smoothing_factor * brightness + \
                (1 - smoothing_factor) * prev_brightness

            threshold = calculate_adaptive_threshold(smoothed_brightness)
            debounce_time = calculate_debounce_time(brightness_diff)

            rounded_brightness = math.ceil(
                max(0, min(100, smoothed_brightness)))

            # Логика за задаване на яркост и логиране на данни

            log_data = [datetime, brightness, smoothed_brightness, smoothing_factor,
                        debounce_time, threshold]

            logwriter.writerow(log_data)

            prev_brightness = rounded_brightness

            if prev_time is None or (datetime.now() - prev_time).seconds >= debounce_time:
                sbc.set_brightness(rounded_brightness)
                print(f"Яркостта на екрана е зададена на {rounded_brightness}% в {datetime.now().strftime('%H:%M:%S')} часа.")

            time.sleep(5)

    cap.release()


if __name__ == '__main__':
    adjust_screen_brightness()
