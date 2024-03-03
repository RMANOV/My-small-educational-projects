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
    return current_brightness * 0.2


def adjust_screen_brightness(camera_index=0, debounce_time=1, threshold=5, smoothing_factor=0.5, read_interval=5):
    previous_brightness = 0  # Инициализиране с начална стойност
    previous_time = None
    smoothed_brightness = None
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
                    use_camera = False
                    continue
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                brightness = gray.mean()
            else:
                brightness = get_screen_brightness()

            if smoothed_brightness is None:
                smoothed_brightness = brightness
            else:
                smoothing_factor = 0.5 if abs(
                    brightness - previous_brightness) > 5 else smoothing_factor
                smoothed_brightness = smoothing_factor * brightness + \
                    (1 - smoothing_factor) * smoothed_brightness

            # Ограничаване на стойността на smoothed_brightness в диапазона 0-100
            smoothed_brightness = max(0, min(100, smoothed_brightness))

            threshold = get_adaptive_threshold(smoothed_brightness)

            if previous_brightness is not None and abs(smoothed_brightness - previous_brightness) >= threshold:
                if previous_time is None or (current_time - previous_time) >= debounce_time:
                    print(f"Яркостта на екрана е зададена на {smoothed_brightness}% в {
                          datetime.now().strftime('%H:%M:%S')} часа.")
                    previous_time = current_time

            previous_brightness = smoothed_brightness
            time.sleep(read_interval)

    finally:
        if use_camera and cap is not None:
            cap.release()


if __name__ == "__main__":
    adjust_screen_brightness()
