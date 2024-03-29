import cv2
from datetime import datetime
import time
import numpy as np
import screen_brightness_control as sbc
import cv2
from datetime import datetime
import time
import numpy as np
import screen_brightness_control as sbc
import math


"""
Автоматичен контрол на яркостта на екрана на десктоп компютъра с помощта на камера или скрийншот

Този скрипт анализира осветеността в стаята чрез камера или скрийншот на екрана и автоматично регулира яркостта на екрана на компютъра,
за да осигури оптимално визуално изживяване и комфорт. Използват се библиотеките OpenCV за обработка на изображения
и screen-brightness-control за контрол на яркостта на екрана.

Необходими библиотеки:
- opencv-python
- screen-brightness-control
- time
- datetime
- pyautogui
- numpy

"""

def get_screen_brightness():
    return sbc.get_brightness()

def get_adaptive_threshold(current_brightness):
    return current_brightness * 0.1


def adjust_screen_brightness(camera_index=0, debounce_time=1, threshold=15, smoothing_factor=0.05, read_interval=5):
    previous_brightness = None  # Инициализиране с None за първоначална проверка
    previous_time = None
    smoothed_brightness = 0  # Започнете с предполагаема начална стойност
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
                    continue  # Продължава да опитва да чете от камерата
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness = gray.mean()
            else:
                brightness = get_screen_brightness()

            if previous_brightness is not None:
                smoothing_factor = 0.05 if abs(
                    brightness - previous_brightness) > 5 else smoothing_factor
                smoothed_brightness = smoothing_factor * brightness + \
                    (1 - smoothing_factor) * previous_brightness

            rounded_brightness = math.ceil(
                max(0, min(95, smoothed_brightness)))

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
