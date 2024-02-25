"""
Автоматичен контрол на яркостта на екрана на десктоп компютъра с помощта на камера

Този скрипт анализира осветеността в стаята чрез камера и автоматично регулира яркостта на екрана на компютъра,
за да осигури оптимално визуално изживяване и комфорт. Използват се библиотеките OpenCV за обработка на изображения
и screen-brightness-control за контрол на яркостта на екрана.

Необходими библиотеки:
- opencv-python
- screen-brightness-control

Автор: <Твоето Име>
"""

import cv2
import screen_brightness_control as sbc


def adjust_screen_brightness(camera_index=0):
    previous_brightness = None

    while True:
        # Инициализация на камерата
        cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            print("Не може да се отвори камерата.")
            return

        # Четене на едно изображение от камерата
        ret, frame = cap.read()
        if not ret:
            print("Не може да се прочете изображението от камерата.")
            return

        # Преобразуване на изображението в сиви тонове и намиране на средната стойност на пикселите
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()

        # Освобождаване на камерата
        cap.release()

        # Регулиране на яркостта на екрана в зависимост от осветеността
        # Предполагаме, че яркостта е в диапазон от 0 до 255
        # Нормализираме стойността и я преобразуваме в проценти за screen-brightness-control
        new_brightness = int((brightness / 255) * 100)

        # Проверка дали има драстична промяна в яркостта
        if previous_brightness is not None and abs(new_brightness - previous_brightness) < 5:
            continue

        # Задаване на новата яркост на екрана
        sbc.set_brightness(new_brightness)
        print(f"Яркостта на екрана е зададена на {new_brightness}%.")

        # Запазване на текущата яркост за следващата итерация
        previous_brightness = new_brightness


if __name__ == "__main__":
    adjust_screen_brightness()
