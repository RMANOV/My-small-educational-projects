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
import random
import queue


def turn_on_keyboard_backlight():
    # Тази функция трябва да бъде имплементирана в зависимост от операционната система
    pass


def analyze_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    brightness = sum(i * hist[i][0] for i in range(256)
                     ) / sum(hist[i][0] for i in range(256))
    brightness = brightness / 256 * 100
    return brightness


def get_screenshot_brightness():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([screenshot], [0], None, [256], [0, 256])
    brightness = sum(i * hist[i][0] for i in range(256)
                     ) / sum(hist[i][0] for i in range(256))
    brightness = brightness / 256 * 100
    return brightness


def adjust_weights_based_on_content(camera_brightness, screenshot_brightness):
    if screenshot_brightness > 95:
        weight_camera = 0.98
        weight_screenshot = 0.02
    elif screenshot_brightness > 90:
        weight_camera = 0.95
        weight_screenshot = 0.05
    elif screenshot_brightness > 80:
        weight_camera = 0.9
        weight_screenshot = 0.1
    elif screenshot_brightness < 20:
        weight_camera = 0.2
        weight_screenshot = 0.8
    else:
        weight_camera = 0.5
        weight_screenshot = 0.5

    return weight_camera, weight_screenshot


def combine_brightness(camera_brightness, screenshot_brightness, weight_camera, weight_screenshot):
    combined_brightness = weight_camera * camera_brightness + \
        weight_screenshot * screenshot_brightness
    return combined_brightness


def process_frames(frame_queue, brightness_queue, batch_size, frame_interval):
    frames = []
    last_frame_time = time.time()
    while True:
        if time.time() - last_frame_time >= frame_interval:
            frame = frame_queue.get()
            if frame is None:
                break
            frames.append(frame)
            if len(frames) == batch_size:
                avg_frame = np.mean(frames, axis=0).astype(np.uint8)
                brightness = analyze_image(avg_frame)
                brightness_queue.put(brightness)
                frames = []
            last_frame_time = time.time()


def pid_controller(setpoint, current_value, kp, ki, kd, dt, integral_term, prev_error):
    error = setpoint - current_value
    integral_term = max(-50, min(50, integral_term + error * dt))
    derivative_term = (error - prev_error) / dt
    output = kp * error + ki * integral_term + kd * derivative_term
    output = max(-10, min(10, output))
    prev_error = error
    return output, integral_term, prev_error


def save_state(state):
    with open('brightness_controller_state.pkl', 'wb') as f:
        pickle.dump(state, f)


def load_state():
    try:
        with open('brightness_controller_state.pkl', 'rb') as f:
            state = pickle.load(f)
            prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd = state
            return prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd
    except (FileNotFoundError, ValueError):
        return None


def adjust_pid_parameters(setpoint, current_value, kp, ki, kd, error_history, brightness_history, adjustment_factor=0.1, stability_threshold=5, stability_count=3):
    current_error = setpoint - current_value
    error_history.append(current_error)
    brightness_history.append(current_value)
    if len(error_history) > 10:
        error_history.pop(0)
        brightness_history.pop(0)

    trend = sum(error_history) / len(error_history)
    brightness_avg = sum(brightness_history) / len(brightness_history)

    if abs(trend) <= stability_threshold:
        stability_count -= 1
    else:
        stability_count = 3

    if stability_count <= 0:
        learning_rate = adjustment_factor
    else:
        learning_rate = adjustment_factor / 2

    if trend > 10:
        kp -= 2 * learning_rate * abs(trend) / kp
        ki -= 2 * learning_rate * abs(trend) / 2 / ki
        kd -= 2 * learning_rate * abs(trend) / kd
    elif trend < -10:
        kp += 2 * learning_rate * abs(trend) / kp
        ki += 2 * learning_rate * abs(trend) / 2 / ki
        kd += 2 * learning_rate * abs(trend) / kd
    else:
        kp -= learning_rate * kp
        ki -= learning_rate * ki
        kd -= learning_rate * kd

    kp = max(0.01, min(5.0, kp))
    ki = max(0.001, min(1.0, ki))
    kd = max(0.001, min(1.0, kd))

    return kp, ki, kd, stability_count


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


def adjust_screen_brightness(camera_index=0, num_threads=4, frame_queue_size=100, brightness_queue_size=100, batch_size=5, frame_interval=0.1, update_interval=1):
    state = load_state()
    if state is None:
        prev_brightness = sbc.get_brightness()[0]
        smoothed_brightness = prev_brightness
        integral_term = 0
        prev_error = 0
        kp, ki, kd = 0.8, 0.2, 0.1
    else:
        prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd = state

    print(f'Initial brightness: {prev_brightness:.1f}% at {
          datetime.now().strftime("%H:%M:%S")}')

    frame_queue = Queue(maxsize=frame_queue_size)
    brightness_queue = Queue(maxsize=brightness_queue_size)

    for _ in range(num_threads):
        t = Thread(target=process_frames, args=(
            frame_queue, brightness_queue, batch_size, frame_interval))
        t.start()

    error_history = []
    brightness_history = []
    stability_count = 3
    last_update_time = time.time()
    last_brightness_change_time = time.time()

    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("Cannot open camera. Exiting...")
            return

        prev_camera_brightness = None
        prev_screenshot_brightness = None

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame from camera.")
                camera_brightness = prev_brightness
            else:
                frame_queue.put(frame)
                try:
                    camera_brightness = brightness_queue.get(
                        block=True, timeout=1)
                except queue.Empty:
                    camera_brightness = prev_brightness

            if time.time() - last_update_time >= update_interval:
                try:
                    screenshot_brightness = get_screenshot_brightness()
                except:
                    print("Error getting screenshot brightness.")
                    screenshot_brightness = prev_brightness

                if prev_camera_brightness is not None and prev_screenshot_brightness is not None:
                    camera_diff = abs(camera_brightness -
                                      prev_camera_brightness)
                    screenshot_diff = abs(
                        screenshot_brightness - prev_screenshot_brightness)

                    if camera_diff < 5 and screenshot_diff < 5:
                        print("-", end="")
                        last_update_time = time.time()
                        continue

                prev_camera_brightness = camera_brightness
                prev_screenshot_brightness = screenshot_brightness

                weight_camera, weight_screenshot = adjust_weights_based_on_content(
                    camera_brightness, screenshot_brightness)
                brightness = combine_brightness(
                    camera_brightness, screenshot_brightness, weight_camera, weight_screenshot)

                if screenshot_brightness > 95:
                    setpoint = max(30, prev_brightness - 40)
                elif screenshot_brightness > 90:
                    setpoint = max(40, prev_brightness - 30)
                elif screenshot_brightness > 80:
                    setpoint = max(50, prev_brightness - 20)
                elif screenshot_brightness < 20:
                    setpoint = min(80, prev_brightness + 20)
                else:
                    setpoint = brightness

                output, integral_term, prev_error = pid_controller(
                    setpoint, smoothed_brightness, kp, ki, kd, dt=update_interval, integral_term=integral_term, prev_error=prev_error)
                smoothed_brightness += output

                if 10 <= screenshot_brightness <= 90:
                    kp, ki, kd, stability_count = adjust_pid_parameters(
                        setpoint, smoothed_brightness, kp, ki, kd, error_history, brightness_history, stability_count=stability_count)

                num_threads = adjust_num_threads(
                    frame_queue.qsize(), num_threads)
                batch_size = adjust_batch_size(
                    brightness_queue.qsize(), batch_size)

                try:
                    smoothed_brightness = max(1, min(100, smoothed_brightness))
                    if abs(smoothed_brightness - prev_brightness) > 5:
                        sbc.set_brightness(math.ceil(smoothed_brightness))
                        print(f'New brightness: {math.ceil(smoothed_brightness)}% at {
                              datetime.now().strftime("%H:%M:%S")}')
                        prev_brightness = smoothed_brightness
                        last_brightness_change_time = time.time()
                    else:
                        print("-", end="")

                    if smoothed_brightness < 20:
                        turn_on_keyboard_backlight()

                    save_state((prev_brightness, smoothed_brightness,
                               integral_term, prev_error, kp, ki, kd))
                except Exception as e:
                    print(f"Error setting brightness: {str(e)}")

                if time.time() - last_brightness_change_time > 5:
                    update_interval = min(update_interval * 1.5, 5)
                else:
                    update_interval = max(update_interval / 1.5, 1)

                last_update_time = time.time()

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
