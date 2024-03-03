import cv2
import screen_brightness_control as sbc
from datetime import datetime
import time


"""
Автоматичен контрол на яркостта на екрана на десктоп компютъра с помощта на камера

Този скрипт анализира осветеността в стаята чрез камера и автоматично регулира яркостта на екрана на компютъра,
за да осигури оптимално визуално изживяване и комфорт. Използват се библиотеките OpenCV за обработка на изображения
и screen-brightness-control за контрол на яркостта на екрана.

Необходими библиотеки:
- opencv-python
- screen-brightness-control
- time
- datetime

"""

def adjust_screen_brightness(camera_index=0, debounce_time=1, threshold=5, smoothing_factor=0.5, read_interval=5):
    previous_brightness = None
    previous_time = None
    smoothed_brightness = None

    # Инициализация на камерата извън цикъла
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Не може да се отвори камерата.")
        return

    # Индикатор за първо прочитане
    first_read = True

    while True:
        # Четене на едно изображение от камерата
        ret, frame = cap.read()
        if not ret:
            print("Не може да се прочете изображението от камерата.")
            return

        # Преобразуване на изображението в сиви тонове и намиране на средната стойност на пикселите
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()

        # Изглаждане на осветеността
        if smoothed_brightness is None:
            smoothed_brightness = brightness
        else:
            smoothed_brightness = smoothing_factor * brightness + (1 - smoothing_factor) * smoothed_brightness

        # Проверка дали има значима промяна в осветеността
        if previous_brightness is not None and abs(smoothed_brightness - previous_brightness) < threshold:
            continue

        # Проверка дали е минал достатъчно време от последната корекция
        current_time = time.time()
        if previous_time is not None and current_time - previous_time < debounce_time:
            continue

        # Задаване на новата яркост на екрана
        new_brightness = int((smoothed_brightness / 255) * 100)
        sbc.set_brightness(new_brightness)
        print(f"Яркостта на екрана е зададена на {new_brightness}% в {datetime.now().strftime('%H:%M:%S')} часа.")

        # Запазване на текущата яркост и време за следващата итерация
        previous_brightness = smoothed_brightness
        previous_time = current_time

        # Изчакване на определен интервал преди следващото прочитане
        time.sleep(read_interval)

        # Изключване на индикатора след първото прочитане
        if first_read:
            sbc.set_brightness(0)
            first_read = False


if __name__ == "__main__":
    adjust_screen_brightness()
