import cv2
import numpy as np
import screen_brightness_control as sbc
from datetime import datetime
import time
import pyautogui
from threading import Thread
from queue import Queue
import pickle


def turn_on_keyboard_backlight():
    pass


def turn_off_keyboard_backlight():
    pass


def analyze_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist = hist.flatten()
    brightness = np.sum(np.arange(256) * hist) / np.sum(hist)
    brightness = brightness / 256 * 100
    return brightness


def get_screenshot_brightness():
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([screenshot], [0], None, [256], [0, 256])
    hist = hist.flatten()
    brightness = np.sum(np.arange(256) * hist) / np.sum(hist)
    brightness = brightness / 256 * 100
    return brightness


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


def adjust_screen_brightness(camera_index=0, num_threads=4, frame_queue_size=100, brightness_queue_size=100,
                             batch_size=5, frame_interval=0.1, update_interval=1):
    state = load_state()
    if state is None:
        prev_brightness = sbc.get_brightness()[0]
        smoothed_brightness = prev_brightness
        integral_term = 0
        prev_error = 0
        kp, ki, kd = 0.6, 0.15, 0.08
    else:
        prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd = state

    print(f'Initial brightness: {round(prev_brightness)}% at {
          datetime.now().strftime("%H:%M:%S")}')

    frame_queue = Queue(maxsize=frame_queue_size)
    brightness_queue = Queue(maxsize=brightness_queue_size)

    for _ in range(num_threads):
        t = Thread(target=process_frames, args=(
            frame_queue, brightness_queue, batch_size, frame_interval))
        t.start()

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
            current_brightness = sbc.get_brightness()[0]
            if abs(current_brightness - prev_brightness) > 10:
                print(f'Brightness changed manually to {current_brightness}%')
                smoothed_brightness = current_brightness
                integral_term = 0
                prev_error = 0

            ret, frame = cap.read()
            if not ret:
                print("Error reading frame from camera.")
                camera_brightness = prev_camera_brightness if prev_camera_brightness is not None else 50
            else:
                frame_queue.put(frame)
                try:
                    camera_brightness = brightness_queue.get(
                        block=True, timeout=1)
                except:
                    camera_brightness = prev_camera_brightness if prev_camera_brightness is not None else 50
                    

            screenshot_brightness = get_screenshot_brightness()

            if prev_camera_brightness is None:
                prev_camera_brightness = camera_brightness
            if prev_screenshot_brightness is None:
                prev_screenshot_brightness = screenshot_brightness

            weight_camera = camera_brightness / 100
            weight_screenshot = 1/2 * (1 - weight_camera) * (1 - weight_camera)
            combined_brightness = weight_camera * camera_brightness + \
                weight_screenshot * screenshot_brightness

            brightness_diff = abs(combined_brightness - smoothed_brightness)
            if brightness_diff > 10:
                setpoint = combined_brightness
                integral_term = 0
                prev_error = 0
            else:
                setpoint = smoothed_brightness

            error = setpoint - smoothed_brightness
            integral_term = max(-50, min(50, integral_term +
                                error * update_interval))
            derivative_term = (error - prev_error) / update_interval
            output = kp * error + ki * integral_term + kd * derivative_term
            output = max(-10, min(10, output))
            prev_error = error

            smoothed_brightness += output
            smoothed_brightness = max(5, min(95, smoothed_brightness))

            try:
                sbc.set_brightness(round(smoothed_brightness))
                if abs(smoothed_brightness - prev_brightness) > 5:
                    print(f'New brightness: {round(smoothed_brightness)}% at {
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

            prev_camera_brightness = camera_brightness
            prev_screenshot_brightness = screenshot_brightness

            time.sleep(update_interval)

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
    finally:
        for _ in range(num_threads):
            frame_queue.put(None)
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()


def load_state():
    try:
        with open('brightness_controller_state.pkl', 'rb') as f:
            state = pickle.load(f)
            prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd = state
            return prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd
    except (FileNotFoundError, ValueError):
        return None


def save_state(state):
    with open('brightness_controller_state.pkl', 'wb') as f:
        pickle.dump(state, f)


if __name__ == '__main__':
    adjust_screen_brightness()
