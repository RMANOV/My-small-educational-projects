import cv2
import math
import screen_brightness_control as sbc
from datetime import datetime
import time
import numpy as np
import pyautogui
from PIL import Image
from threading import Thread
from queue import Queue
import pickle


def turn_on_keyboard_backlight():
    # Тази функция трябва да бъде имплементирана в зависимост от операционната система
    pass


def analyze_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    brightness = sum(i * hist[i][0] for i in range(256)
                     ) / sum(hist[i][0] for i in range(256))
    return brightness / 256 * 100


def get_screenshot_brightness():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([screenshot], [0], None, [256], [0, 256])
    brightness = sum(i * hist[i][0] for i in range(256)
                     ) / sum(hist[i][0] for i in range(256))
    if not brightness:
        return 0
    return brightness / 256 * 100


def adjust_weights_based_on_content(camera_brightness, screenshot_brightness):
    ratio = screenshot_brightness / camera_brightness if camera_brightness != 0 else 1

    min_weight = 0.3
    max_weight = 0.7
    min_ratio = 0.8
    max_ratio = 1.2

    if ratio < min_ratio:
        min_ratio = ratio
    if ratio > max_ratio:
        max_ratio = ratio

    if ratio > 1:
        weight_camera = min_weight + \
            (1 - min_weight) * (ratio - 1) / (max_ratio - 1)
        weight_screenshot = 1 - weight_camera
    elif ratio < 1:
        weight_screenshot = min_weight + \
            (1 - min_weight) * (1 - ratio) / (1 - min_ratio)
        weight_camera = 1 - weight_screenshot
    else:
        weight_camera = 0.5
        weight_screenshot = 0.5

    return weight_camera, weight_screenshot


def combine_brightness(camera_brightness, screenshot_brightness, weight_camera, weight_screenshot):
    combined_brightness = (weight_camera * camera_brightness + weight_screenshot * (
        100 / screenshot_brightness)) / (weight_camera + weight_screenshot)
    return combined_brightness


def process_frames(frame_queue, brightness_queue, batch_size):
    frames = []
    while True:
        frame = frame_queue.get()
        if frame is None:
            break
        frames.append(frame)
        if len(frames) == batch_size:
            brightness = analyze_image(np.mean(frames, axis=0))
            brightness_queue.put(brightness)
            frames = []


def pid_controller(setpoint, current_value, kp, ki, kd, dt, integral_term, prev_error):
    error = setpoint - current_value
    integral_term += error * dt
    derivative_term = (error - prev_error) / dt
    output = kp * error + ki * integral_term + kd * derivative_term
    prev_error = error
    return output, integral_term, prev_error


def save_state(state):
    with open('brightness_controller_state.pkl', 'wb') as f:
        pickle.dump(state, f)


def load_state():
    try:
        with open('brightness_controller_state.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def adjust_pid_parameters(setpoint, current_value, kp, ki, kd):
    error = abs(setpoint - current_value)
    if error > 20:
        kp *= 1.1
        ki *= 1.05
        kd *= 1.05
    elif error < 5:
        kp *= 0.9
        ki *= 0.95
        kd *= 0.95
    return kp, ki, kd


def adjust_num_threads(frame_queue_size, num_threads):
    if frame_queue_size > num_threads * 10:
        num_threads += 1
    elif frame_queue_size < num_threads * 5 and num_threads > 1:
        num_threads -= 1
    return num_threads


def adjust_batch_size(brightness_queue_size, batch_size):
    if brightness_queue_size > batch_size * 2:
        batch_size += 1
    elif brightness_queue_size < batch_size and batch_size > 1:
        batch_size -= 1
    return batch_size


def adjust_screen_brightness(camera_index=0, num_threads=4, frame_queue_size=100, brightness_queue_size=100, batch_size=5):
    state = load_state()
    if state is None:
        prev_brightness = sbc.get_brightness()[0]
        smoothed_brightness = prev_brightness
        integral_term = 0
        prev_error = 0
        kp, ki, kd = 0.5, 0.1, 0.05
    else:
        prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd = state

    print(f'Initial brightness: {prev_brightness:.1f}% at {
          datetime.now().strftime("%H:%M:%S")}')

    frame_queue = Queue(maxsize=frame_queue_size)
    brightness_queue = Queue(maxsize=brightness_queue_size)

    for _ in range(num_threads):
        t = Thread(target=process_frames, args=(
            frame_queue, brightness_queue, batch_size))
        t.start()

    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("Cannot open camera. Exiting...")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame from camera.")
                camera_brightness = prev_brightness
            else:
                frame_queue.put(frame)
                try:
                    camera_brightness = brightness_queue.get(timeout=1)
                except:
                    camera_brightness = prev_brightness

            try:
                screenshot_brightness = get_screenshot_brightness()
            except:
                print("Error getting screenshot brightness.")
                screenshot_brightness = prev_brightness

            if screenshot_brightness == 0:
                brightness = camera_brightness
            elif camera_brightness == 0:
                brightness = screenshot_brightness
            elif camera_brightness == 0 and screenshot_brightness == 0:
                print('Error: camera and screenshot brightness is 0')
                time.sleep(1)
                continue
            else:
                weight_camera, weight_screenshot = adjust_weights_based_on_content(
                    camera_brightness, screenshot_brightness)
                brightness = combine_brightness(
                    camera_brightness, screenshot_brightness, weight_camera, weight_screenshot)

            setpoint = brightness
            output, integral_term, prev_error = pid_controller(
                setpoint, smoothed_brightness, kp, ki, kd, dt=1, integral_term=integral_term, prev_error=prev_error)
            smoothed_brightness += output

            kp, ki, kd = adjust_pid_parameters(
                setpoint, smoothed_brightness, kp, ki, kd)
            num_threads = adjust_num_threads(frame_queue.qsize(), num_threads)
            batch_size = adjust_batch_size(
                brightness_queue.qsize(), batch_size)

            try:
                if smoothed_brightness < 0:
                    smoothed_brightness = 0
                elif smoothed_brightness > 100:
                    smoothed_brightness = 100

                sbc.set_brightness(math.ceil(smoothed_brightness))
                print(f'New brightness: {math.ceil(smoothed_brightness)}% at {
                      datetime.now().strftime("%H:%M:%S")}')

                if smoothed_brightness < 20:
                    turn_on_keyboard_backlight()

                save_state((prev_brightness, smoothed_brightness,
                           integral_term, prev_error, kp, ki, kd))
            except:
                print("Error setting brightness.")

            prev_brightness = smoothed_brightness

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
    finally:
        for _ in range(num_threads):
            frame_queue.put(None)
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    adjust_screen_brightness()
