import cv2
from datetime import datetime
import time
import numpy as np
import screen_brightness_control as sbc
import math


def get_screen_brightness():
    return sbc.get_brightness()


def get_adaptive_threshold(smoothed_brightness):
    # Адаптивен праг, който може да варира в зависимост от нивото на яркост
    return max(5, min(20, smoothed_brightness * 0.1))


def adjust_screen_brightness(camera_index=0, initial_debounce_time=1, initial_threshold=15, initial_smoothing_factor=0.05, read_interval=5):
    previous_brightness = None
    previous_time = None
    smoothed_brightness = 50  # Предполагаема начална стойност за яркостта
    use_camera = True

    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("Не може да се отвори камерата. Използва се скрийншот на екрана.")
            use_camera = False

        while True:
            current_time = time.time()

            if use_camera:
                ret, frame = cap.read()
                if not ret:
                    print("Не може да се прочете изображението от камерата.")
                    continue
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness = gray.mean()
            else:
                brightness = get_screen_brightness()

            if previous_brightness is not None:
                smoothing_factor = initial_smoothing_factor if abs(
                    brightness - previous_brightness) > 5 else initial_smoothing_factor
                smoothed_brightness = smoothing_factor * brightness + \
                    (1 - smoothing_factor) * previous_brightness

            rounded_brightness = math.ceil(
                max(0, min(100, smoothed_brightness)))

            threshold = get_adaptive_threshold(smoothed_brightness)
            # Може да добавите адаптивно изчисление тук
            debounce_time = initial_debounce_time

            if previous_brightness is None or abs(rounded_brightness - previous_brightness) >= threshold:
                if previous_time is None or (current_time - previous_time) >= debounce_time:
                    sbc.set_brightness(rounded_brightness)
                    print(f"Яркостта на екрана е зададена на {rounded_brightness}% в {
                          datetime.now().strftime('%H:%M:%S')} часа.")
                    previous_time = current_time

            previous_brightness = rounded_brightness
            time.sleep(read_interval)

    finally:
        if use_camera and cap is not None:
            cap.release()


if __name__ == "__main__":
    adjust_screen_brightness()
