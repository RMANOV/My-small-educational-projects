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
    # return brightness / 256 * 100
    if not brightness:
        return 0
    return brightness / 256 * 100


# Инициализация на базови тегла
weight_camera = 0.5
weight_screenshot = 0.5

def adjust_weights_based_on_content(camera_brightness, screenshot_brightness):
    """
    Динамично регулиране на теглата в зависимост от съотношението между яркостта, 
    измерена от камерата, и яркостта на скрийншота.
    """
    # Определяне на съотношението между яркостта на скрийншота и яркостта от камерата
    ratio = screenshot_brightness / camera_brightness if camera_brightness != 0 else 1



    # # Динамично коригиране на теглата в зависимост от съотношението
    # if ratio > 1.2:  # Екранът е значително по-ярък от околната осветеност
    #     weight_camera = 0.3
    #     weight_screenshot = 0.7
    # elif ratio < 0.8:  # Екранът е значително по-тъмен от околната осветеност
    #     weight_camera = 0.7
    #     weight_screenshot = 0.3

    min_weight = 0.3
    max_weight = 0.7
    min_ratio = 0.8
    max_ratio = 1.2
    


    if ratio > 1:
        weight_camera = min_weight + (1 - min_weight) * (ratio - 1) / (max_ratio - 1)
        weight_screenshot = 1 - weight_camera
    elif ratio < 1:
        weight_screenshot = min_weight + (1 - min_weight) * (1 - ratio) / (1 - min_ratio) 
        weight_camera = 1 - weight_screenshot
    else:
        weight_camera = 0.5
        weight_screenshot = 0.5

    # brightness = weight_camera * camera_brightness + weight_screenshot * screenshot_brightness
        

    return weight_camera, weight_screenshot


def combine_brightness(camera_brightness, screenshot_brightness, weight_camera, weight_screenshot):
    """
    Комбиниране на стойностите за яркост с използване на динамично регулирани тегла.
    """
    combined_brightness = (weight_camera * camera_brightness + weight_screenshot * (
        100 / screenshot_brightness)) / (weight_camera + weight_screenshot)
    return combined_brightness

# Във функцията за регулиране на яркостта:
    # Определяне на теглата
    weight_camera, weight_screenshot = adjust_weights_based_on_content(
        camera_brightness, screenshot_brightness)

    # Комбиниране на яркостите с определените тегла
    brightness = combine_brightness(
        camera_brightness, screenshot_brightness, weight_camera, weight_screenshot)



def adjust_screen_brightness(camera_index=0):
    # Получаване на текущата яркост на екрана
    prev_brightness = sbc.get_brightness()[0]
    prev_time = None
    smoothed_brightness = prev_brightness

    print(f'Initial brightness: {prev_brightness}% at {datetime.now().strftime("%H:%M:%S")}')

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

                # if camera_brightness == 0 or screenshot_brightness == 0:
                #     print('Error: camera or screenshot brightness is 0')
                #     time.sleep(1)
                #     continue
                if screenshot_brightness == 0:
                    brightness = camera_brightness  # Ако скрийншота е черен, използваме само камерата
                
                elif camera_brightness == 0:
                    brightness = screenshot_brightness  # Ако камерата е черна, използваме само скрийншота

                elif camera_brightness == 0 and screenshot_brightness == 0:
                    print('Error: camera and screenshot brightness is 0')
                    time.sleep(1)
                    continue

                else:
                    # Комбиниране на двете стойности за яркост
                    # brightness = (camera_brightness + 1/screenshot_brightness) / 2
                    # brightness = combine_brightness(
                    #     camera_brightness, screenshot_brightness,adjust_weights_based_on_content(camera_brightness, screenshot_brightness))
                    adjust_weights_based_on_content(camera_brightness, screenshot_brightness)
                    brightness = combine_brightness(
                        camera_brightness, screenshot_brightness, weight_camera, weight_screenshot)
                        

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
