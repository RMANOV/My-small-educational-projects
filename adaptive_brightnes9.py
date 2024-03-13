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
    # print(f"Camera brightness: {brightness:.2f}%")
    return brightness


def get_screenshot_brightness():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([screenshot], [0], None, [256], [0, 256])
    brightness = sum(i * hist[i][0] for i in range(256)
                     ) / sum(hist[i][0] for i in range(256))
    brightness = brightness / 256 * 100
    # print(f"Screenshot brightness: {brightness:.2f}%")
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

    # Ensure weights are not zero
    weight_camera = max(0.1, weight_camera)
    weight_screenshot = max(0.1, weight_screenshot)

    # print(f"Camera weight: {weight_camera:.2f}, Screenshot weight: {
    #         weight_screenshot:.2f}")
    return weight_camera, weight_screenshot


def combine_brightness(camera_brightness, screenshot_brightness, weight_camera, weight_screenshot):
    combined_brightness = weight_camera * camera_brightness + \
        weight_screenshot * screenshot_brightness
    # print(f"Combined brightness: {combined_brightness:.2f}%")
    return combined_brightness


def process_frames(frame_queue, brightness_queue, batch_size):
    frames = []
    while True:
        frame = frame_queue.get()
        if frame is None:
            break
        frames.append(frame)
        if len(frames) == batch_size:
            avg_frame = np.mean(frames, axis=0).astype(np.uint8)
            brightness = analyze_image(avg_frame)
            brightness_queue.put(brightness)
            frames = []


def pid_controller(setpoint, current_value, kp, ki, kd, dt, integral_term, prev_error):
    error = setpoint - current_value
    integral_term = max(-50, min(50, integral_term + error * dt))
    derivative_term = (error - prev_error) / dt
    output = kp * error + ki * integral_term + kd * derivative_term
    output = max(-10, min(10, output))
    prev_error = error
    # print(f"PID output: {output:.2f}")
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


# def adjust_pid_parameters(setpoint, current_value, kp, ki, kd, error_history, adjustment_factor=0.1):
#     error = setpoint - current_value
#     error_history.append(error)

#     if len(error_history) > 10:
#         error_history.pop(0)

#     error_avg = sum(error_history) / len(error_history)
#     error_std = math.sqrt(
#         sum((x - error_avg) ** 2 for x in error_history) / len(error_history))

#     if error_std > 10:
#         # Голямо отклонение в грешката, увеличете коефициентите
#         kp *= (1 + adjustment_factor)
#         ki *= (1 + adjustment_factor / 2)
#         kd *= (1 + adjustment_factor / 2)
#     elif error_std < 5:
#         # Малко отклонение в грешката, намалете коефициентите
#         kp *= (1 - adjustment_factor)
#         ki *= (1 - adjustment_factor / 2)
#         kd *= (1 - adjustment_factor / 2)

#     # Ограничете коефициентите в разумни граници
#     kp = max(0.1, min(10, kp))
#     ki = max(0.01, min(1, ki))
#     kd = max(0.01, min(1, kd))

#     print(f"Adjusted PID parameters: KP={kp:.2f}, KI={
#           ki:.2f}, KD={kd:.2f}, Error STD={error_std:.2f}")
#     return kp, ki, kd

def adjust_pid_parameters(setpoint, current_value, kp, ki, kd, error_history):
    """
    Adaptively adjust PID parameters based on error trends and performance.
    
    Args:
    - setpoint: Desired target value for the control system.
    - current_value: Current value from the control system.
    - kp, ki, kd: Current PID parameters.
    - error_history: History of recent errors to analyze trends.
    
    Returns:
    - kp, ki, kd: Adjusted PID parameters.
    """
    # Calculate current error and update history
    current_error = setpoint - current_value
    error_history.append(current_error)
    if len(error_history) > 5:  # Keep a fixed window of recent errors
        error_history.pop(0)

    # Calculate error trend (simple moving average)
    trend = sum(error_history) / len(error_history)

    # Adjust PID parameters based on error trend
    learning_rate = 0.05  # Smaller values for gradual adjustments
    if abs(trend) > 5:  # Significant trend detected
        kp += learning_rate * abs(trend) / kp
        ki += learning_rate * abs(trend) / 2 / ki  # Adjust less aggressively
        kd += learning_rate * abs(trend) / kd
    else:  # Minimal trend, focus on stability
        kp -= learning_rate * kp
        ki -= learning_rate * ki
        kd -= learning_rate * kd

    # Ensure PID parameters remain within sensible bounds
    kp = max(0.01, min(5.0, kp))
    ki = max(0.001, min(1.0, ki))
    kd = max(0.001, min(1.0, kd))

    # print(f"Adjusted PID parameters: KP={kp:.3f}, KI={ki:.3f}, KD={kd:.3f}")
    return kp, ki, kd



def adjust_num_threads(frame_queue_size, num_threads):
    if frame_queue_size > num_threads * 10:
        num_threads += 1
    elif frame_queue_size < num_threads * 5 and num_threads > 1:
        num_threads -= 1
    # print(f"Adjusted number of threads: {num_threads}")
    return num_threads


def adjust_batch_size(brightness_queue_size, batch_size):
    if brightness_queue_size > batch_size * 2:
        batch_size += 1
    elif brightness_queue_size < batch_size and batch_size > 1:
        batch_size -= 1
    # print(f"Adjusted batch size: {batch_size}")
    return batch_size


def adjust_screen_brightness(camera_index=0, num_threads=4, frame_queue_size=100, brightness_queue_size=100, batch_size=5):
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
            frame_queue, brightness_queue, batch_size))
        t.start()

    error_history = []

    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("Cannot open camera. Exiting...")
            return

        prev_camera_brightness = None
        prev_screenshot_brightness = None

        while True:
            current_brightness = sbc.get_brightness()[0]
            if current_brightness != prev_brightness:
                print(f'Brightness changed manually to {current_brightness}%')
                smoothed_brightness = current_brightness
                integral_term = 0
                prev_error = 0
                prev_brightness = current_brightness

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

            try:
                screenshot_brightness = get_screenshot_brightness()
            except:
                print("Error getting screenshot brightness.")
                screenshot_brightness = prev_brightness

            if prev_camera_brightness is not None and prev_screenshot_brightness is not None:
                camera_diff = abs(camera_brightness - prev_camera_brightness)
                screenshot_diff = abs(
                    screenshot_brightness - prev_screenshot_brightness)

                if camera_diff < 5 and screenshot_diff < 5:
                    # print("No significant change in brightness. Skipping adjustment.")
                    continue

            prev_camera_brightness = camera_brightness
            prev_screenshot_brightness = screenshot_brightness

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

            if brightness > 80:
                setpoint = 70
            elif brightness < 20:
                setpoint = 30
            else:
                setpoint = brightness

            output, integral_term, prev_error = pid_controller(
                setpoint, smoothed_brightness, kp, ki, kd, dt=1, integral_term=integral_term, prev_error=prev_error)
            smoothed_brightness += output

            kp, ki, kd = adjust_pid_parameters(
                setpoint, smoothed_brightness, kp, ki, kd, error_history)
            num_threads = adjust_num_threads(frame_queue.qsize(), num_threads)
            batch_size = adjust_batch_size(
                brightness_queue.qsize(), batch_size)

            try:
                smoothed_brightness = max(1, min(100, smoothed_brightness))
                if abs(smoothed_brightness - current_brightness) > 5:
                    sbc.set_brightness(math.ceil(smoothed_brightness))
                    print(f'New brightness: {math.ceil(smoothed_brightness)}% at {
                          datetime.now().strftime("%H:%M:%S")}')
                    prev_brightness = smoothed_brightness
                else:
                    print(f'Brightness remains at {math.ceil(current_brightness)}% at {
                          datetime.now().strftime("%H:%M:%S")}')

                if smoothed_brightness < 20:
                    turn_on_keyboard_backlight()

                save_state((prev_brightness, smoothed_brightness,
                           integral_term, prev_error, kp, ki, kd))
            except Exception as e:
                print(f"Error setting brightness: {str(e)}")

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
