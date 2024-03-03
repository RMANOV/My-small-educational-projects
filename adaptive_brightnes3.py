import cv2
import csv
import math
import screen_brightness_control as sbc
from datetime import datetime
import time
import numpy as np

LOG_FILE = 'brightness_log.csv'


def calculate_smoothing_factor(brightness_diff):
    # Адаптивно изчисление на фактора за изглаждане в зависимост от разликата в яркостта
    return max(0.05, min(0.3, 1 / (1 + brightness_diff)))


def calculate_debounce_time(brightness_diff):
    # Адаптивно изчисление на времето за дебаунс в зависимост от разликата в яркостта
    return max(1, min(5, brightness_diff * 0.5))


def calculate_adaptive_threshold(smoothed_brightness):
    # Адаптивно изчисление на прага за осветеност в зависимост от изгладената яркост
    return max(5, min(20, smoothed_brightness * 0.1))


def analyze_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    brightness = calculate_histogram_brightness(hist)
    return brightness


def calculate_histogram_brightness(hist):
    brightness = sum(i * hist[i][0] for i in range(256)
                     ) / sum(hist[i][0] for i in range(256))
    return brightness / 256 * 100  # Нормализация до 100


def adjust_screen_brightness(camera_index=0):
    prev_brightness = 50  # Започва с разумна начална стойност
    prev_time = None
    smoothed_brightness = 50  # Предпочитана начална стойност за изглаждане

    cap = cv2.VideoCapture(camera_index)
    log_headers = ['timestamp', 'raw_brightness', 'smoothed_brightness',
                   'smoothing_factor', 'debounce_time', 'threshold']

    with open(LOG_FILE, 'w', newline='') as logfile:
        logwriter = csv.writer(logfile)
        logwriter.writerow(log_headers)

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            brightness = analyze_image(frame)
            brightness_diff = abs(brightness - prev_brightness)

            if brightness_diff < calculate_adaptive_threshold(prev_brightness):
                # Ако разликата е под адаптивния праг, не прави корекция
                time.sleep(1)
                continue

            smoothing_factor = calculate_smoothing_factor(brightness_diff)
            smoothed_brightness = smoothing_factor * brightness + \
                (1 - smoothing_factor) * prev_brightness

            debounce_time = calculate_debounce_time(brightness_diff)
            current_time = datetime.now()

            if prev_time is None or (current_time - prev_time).total_seconds() >= debounce_time:
                sbc.set_brightness(math.ceil(smoothed_brightness))
                print(f"Яркостта на екрана е зададена на {math.ceil(smoothed_brightness)}% в {
                      current_time.strftime('%H:%M:%S')} часа.")
                prev_time = current_time

                log_data = [current_time.strftime('%Y-%m-%d %H:%M:%S'), brightness, smoothed_brightness,
                            smoothing_factor, debounce_time, calculate_adaptive_threshold(smoothed_brightness)]
                logwriter.writerow(log_data)

            prev_brightness = smoothed_brightness
            time.sleep(1)  # Определете подходящ интервал за проверка

    cap.release()


if __name__ == '__main__':
    adjust_screen_brightness()
