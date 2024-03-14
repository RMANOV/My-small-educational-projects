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

    weight_camera = max(0.1, weight_camera)
    weight_screenshot = max(0.1, weight_screenshot)

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
    if state:
        prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd = state
    else:
        # Assuming single or primary display
        prev_brightness = sbc.get_brightness()[0]
        smoothed_brightness = prev_brightness
        integral_term = prev_error = 0
        kp, ki, kd = 0.1, 0.01, 0.01  # Initial PID coefficients

    frame_queue = Queue(maxsize=frame_queue_size)
    brightness_queue = Queue(maxsize=brightness_queue_size)

    for _ in range(num_threads):
        Thread(target=process_frames, args=(frame_queue,
               brightness_queue, batch_size, frame_interval)).start()

    error_history = []
    brightness_history = []

    cap = cv2.VideoCapture(camera_index)
    last_update_time = time.time()
    while True:
        _, frame = cap.read()
        if frame is not None:
            frame_queue.put(frame)

        current_time = time.time()
        if current_time - last_update_time > update_interval:
            if not brightness_queue.empty():
                camera_brightness = brightness_queue.get()
                screenshot_brightness = get_screenshot_brightness()
                weight_camera, weight_screenshot = adjust_weights_based_on_content(
                    camera_brightness, screenshot_brightness)
                combined_brightness = combine_brightness(
                    camera_brightness, screenshot_brightness, weight_camera, weight_screenshot)

                if screenshot_brightness > 80:  # If screen is very bright, reduce brightness more aggressively
                    setpoint = max(30, prev_brightness - 20)
                else:
                    setpoint = 50  # Default setpoint adjustment

                # Ensure the brightness_history list is updated before calling adjust_pid_parameters
                brightness_history.append(combined_brightness)
                if len(brightness_history) > 10:
                    brightness_history.pop(0)

                kp, ki, kd, _ = adjust_pid_parameters(setpoint, combined_brightness, kp, ki, kd, error_history,
                                                      brightness_history, adjustment_factor=0.1, stability_threshold=5, stability_count=3)

                output, integral_term, prev_error = pid_controller(
                    setpoint, smoothed_brightness, kp, ki, kd, 1, integral_term, prev_error)
                smoothed_brightness += output
                sbc.set_brightness(smoothed_brightness)
                save_state((smoothed_brightness, integral_term,
                           prev_error, kp, ki, kd))
                last_update_time = current_time

    cap.release()



if __name__ == '__main__':
    adjust_screen_brightness()
