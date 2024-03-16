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

class BrightnessController:
    def __init__(self, camera_index=0, num_threads=4, frame_queue_size=100, brightness_queue_size=100, batch_size=5, frame_interval=0.1, update_interval=1):
        self.camera_index = camera_index
        self.num_threads = num_threads
        self.frame_queue_size = frame_queue_size
        self.brightness_queue_size = brightness_queue_size
        self.batch_size = batch_size
        self.frame_interval = frame_interval
        self.update_interval = update_interval
        self.frame_queue = Queue(maxsize=frame_queue_size)
        self.brightness_queue = Queue(maxsize=brightness_queue_size)
        self.error_history = []
        self.brightness_history = []
        self.stability_count = 3
        self.last_update_time = time.time()
        self.last_brightness_change_time = time.time()
        self.last_screenshot_brightness = None

    def turn_on_keyboard_backlight(self):
        # Тази функция трябва да бъде имплементирана в зависимост от операционната система
        pass

    def turn_off_keyboard_backlight(self):
        # Тази функция трябва да бъде имплементирана в зависимост от операционната система
        pass

    def turn_on_sleep_mode(self):
        wait_count = 0
        screenshot_wait_count = 0
        last_brightness_change_time = time.time()
        last_screenshot_time = time.time()
       
        while True:
            try:
                screenshot_brightness = self.get_screenshot_brightness()
                screenshot_wait_count = 0
                last_screenshot_time = time.time()
               
                if screenshot_brightness is not None:
                    if abs(screenshot_brightness - self.last_screenshot_brightness) > 5:
                        last_brightness_change_time = time.time()
                    self.last_screenshot_brightness = screenshot_brightness
                   
                    if self.is_system_stable() and not self.is_system_sleeping() and not self.is_fullscreen_mode():
                        return screenshot_brightness
                else:
                    screenshot_wait_count += 1
                    print(f'Checking screenshot brightness: {screenshot_brightness}% at {datetime.now().strftime("%H:%M:%S")}', end=" ")
                   
            except Exception as e:
                print(f'Error getting screenshot brightness: {str(e)} at {datetime.now().strftime("%H:%M:%S")}')
                screenshot_wait_count += 1
               
            if time.time() - last_brightness_change_time > 300 or not self.is_system_stable() or self.is_system_sleeping() or self.is_fullscreen_mode() or screenshot_wait_count > 300:
                print(f"Exiting main loop due to inactivity or system instability at {datetime.now().strftime('%H:%M:%S')}")
                self.release_resources()
               
                while True:
                    try:
                        wait_time = self.calculate_wait_time(wait_count)
                        time.sleep(wait_time)
                       
                        if self.is_user_active():
                            print(f"User activity detected. Resuming brightness control at {datetime.now().strftime('%H:%M:%S')}")
                            return self.get_screenshot_brightness()
                       
                        screenshot_brightness = self.get_screenshot_brightness()
                       
                        if screenshot_brightness is not None:
                            print(f"Screenshot brightness available. Resuming brightness control at {datetime.now().strftime('%H:%M:%S')}")
                            return screenshot_brightness
                       
                        wait_count += 1
                       
                    except Exception as e:
                        print(f'Error during sleep mode: {str(e)} at {datetime.now().strftime("%H:%M:%S")}')
                        wait_count += 1
                       
        return self.last_screenshot_brightness

    def analyze_image(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        total_pixels = frame.shape[0] * frame.shape[1]
        brightness = np.sum(hist) / total_pixels / 255 * 100
        return brightness

    def get_screenshot_brightness(self):
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        total_pixels = screenshot_gray.shape[0] * screenshot_gray.shape[1]
        brightness = np.sum(screenshot_gray) / total_pixels / 255 * 100
        return brightness

    def adjust_weights_based_on_content(self, camera_brightness, screenshot_brightness):
        weight_camera = camera_brightness / 100
        weight_screenshot = 1 - weight_camera
        return weight_camera, weight_screenshot

    def combine_brightness(self, camera_brightness, screenshot_brightness, weight_camera, weight_screenshot):
        return weight_camera * camera_brightness + weight_screenshot * screenshot_brightness

    def process_frames(self):
        frames = []
        last_frame_time = time.time()
        while True:
            if time.time() - last_frame_time >= self.frame_interval:
                frame = self.frame_queue.get()
                if frame is None:
                    break
                frames.append(frame)
                if len(frames) == self.batch_size:
                    avg_frame = np.mean(frames, axis=0).astype(np.uint8)
                    brightness = self.analyze_image(avg_frame)
                    self.brightness_queue.put(brightness)
                    frames = []
                last_frame_time = time.time()

    def pid_controller(self, setpoint, current_value, kp, ki, kd, dt, integral_term, prev_error):
        error = setpoint - current_value
        integral_term = np.clip(integral_term + error * dt, -50, 50)
        derivative_term = (error - prev_error) / dt
        output = np.clip(kp * error + ki * integral_term + kd * derivative_term, -10, 10)
        prev_error = error
        return output, integral_term, prev_error

    def save_state(self, state):
        with open('brightness_controller_state.pkl', 'wb') as f:
            pickle.dump(state, f)

    def load_state(self):
        try:
            with open('brightness_controller_state.pkl', 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, ValueError):
            return None

    def adjust_pid_parameters(self, setpoint, current_value, kp, ki, kd, adjustment_factor=0.1, stability_threshold=5):
        current_error = setpoint - current_value
        self.error_history.append(current_error)
        self.brightness_history.append(current_value)
        if len(self.error_history) > 10:
            self.error_history.pop(0)
            self.brightness_history.pop(0)
        trend = np.mean(self.error_history)
        if np.abs(trend) <= stability_threshold:
            self.stability_count -= 1
        else:
            self.stability_count = 3
        learning_rate = adjustment_factor if self.stability_count <= 0 else adjustment_factor / 2
        if trend > 10:
            kp -= 2 * learning_rate * np.abs(trend) / kp
            ki -= 2 * learning_rate * np.abs(trend) / 2 / ki
            kd -= 2 * learning_rate * np.abs(trend) / kd
        elif trend < -10:
            kp += 2 * learning_rate * np.abs(trend) / kp
            ki += 2 * learning_rate * np.abs(trend) / 2 / ki
            kd += 2 * learning_rate * np.abs(trend) / kd
        else:
            kp -= learning_rate * kp
            ki -= learning_rate * ki
            kd -= learning_rate * kd
        kp = np.clip(kp, 0.01, 5.0)
        ki = np.clip(ki, 0.001, 1.0)
        kd = np.clip(kd, 0.001, 1.0)
        return kp, ki, kd

    def adjust_num_threads(self):
        if self.frame_queue.qsize() > self.num_threads * 10:
            self.num_threads += 1
        elif self.frame_queue.qsize() < self.num_threads * 5 and self.num_threads > 1:
            self.num_threads -= 1

    def adjust_batch_size(self):
        if self.brightness_queue.qsize() > self.batch_size * 2:
            self.batch_size += 1
        elif self.brightness_queue.qsize() < self.batch_size and self.batch_size > 1:
            self.batch_size -= 1

    def check_screenshot_brightness(self, prev_screenshot_brightness):
        try:
            screenshot_brightness = self.get_screenshot_brightness()
        except Exception as e:
            print(f'Error getting screenshot brightness: {str(e)} at {datetime.now().strftime("%H:%M:%S")}')
            screenshot_brightness = prev_screenshot_brightness if prev_screenshot_brightness is not None else 50
            self.adjust_pid_parameters(50, screenshot_brightness, 0.6, 0.15, 0.08)
            if time.time() - self.last_update_time > 300 or time.time() - self.last_brightness_change_time > 300 or self.stability_count <= 0:
                print(f"Screenshot brightness isn't available for 5 minutes or no brightness change for 5 minutes or System is busy. Exiting at {datetime.now().strftime('%H:%M:%S')}")
                self.turn_on_sleep_mode()
                return False
            if pyautogui.getActiveWindowTitle() == "full screen application":
                print(f'Exiting due to full screen application at {datetime.now().strftime("%H:%M:%S")}')
                self.turn_on_sleep_mode()
                return False
            # check for the user playing a game
            # check for the video playing
            # check for the video call in progress
            # check for the system in sleep mode
            # check for the user not active
            # check for the system is unstable
            print("Exiting due to other scenarios...")
            self.turn_on_sleep_mode()
            return False
        return screenshot_brightness

    def is_system_stable(self):
        trend = np.mean(self.error_history)
        return len(self.error_history) >= 10 and np.abs(trend) <= 5

    def is_system_sleeping(self):
        return time.time() - self.last_update_time > 300

    def is_fullscreen_mode(self):
        return pyautogui.getActiveWindowTitle() == "full screen application"

    def release_resources(self):
        if not self.frame_queue.empty():
            for _ in range(self.num_threads):
                self.frame_queue.put(None)
        self.brightness_queue.queue.clear()
        self.turn_off_keyboard_backlight()
        if self.num_threads > 1:
            self.num_threads -= 1
        if self.batch_size > 1:
            self.batch_size -= 1
        cv2.destroyAllWindows()

    def calculate_wait_time(self, wait_count):
        return wait_count * 5

    def is_user_active(self):
        return pyautogui.onScreen(0, 0) or pyautogui.onScreen(100, 100)

    def run(self):
        state = self.load_state()
        if state is None:
            prev_brightness = sbc.get_brightness()[0]
            smoothed_brightness = prev_brightness
            integral_term = 0
            prev_error = 0
            kp, ki, kd = 0.6, 0.15, 0.08
        else:
            prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd = state
        print(f'Initial brightness: {math.ceil(prev_brightness)}% at {datetime.now().strftime("%H:%M:%S")}')
        for _ in range(self.num_threads):
            Thread(target=self.process_frames).start()
        try:
            cap = cv2.VideoCapture(self.camera_index)
            if not cap.isOpened():
                print("Cannot open camera. Exiting...")
                return
            prev_camera_brightness = None
            prev_screenshot_brightness = None
            while True:
                current_brightness = sbc.get_brightness()[0]
                if np.abs(current_brightness - prev_brightness) > 10:
                    print(f'Brightness changed manually to {current_brightness}%')
                    smoothed_brightness = current_brightness
                    integral_term = 0
                    prev_error = 0
                ret, frame = cap.read()
                if not ret:
                    print("Error reading frame from camera.")
                    camera_brightness = prev_camera_brightness if prev_camera_brightness is not None else 50
                else:
                    self.frame_queue.put(frame)
                    try:
                        camera_brightness = self.brightness_queue.get(block=True, timeout=1)
                    except queue.Empty:
                        camera_brightness = prev_camera_brightness if prev_camera_brightness is not None else 50
                screenshot_brightness = self.check_screenshot_brightness(prev_screenshot_brightness)
                if screenshot_brightness is False:
                    break
                prev_camera_brightness = camera_brightness if prev_camera_brightness is None else prev_camera_brightness
                prev_screenshot_brightness = screenshot_brightness if prev_screenshot_brightness is None else prev_screenshot_brightness
                weight_camera, weight_screenshot = self.adjust_weights_based_on_content(camera_brightness, screenshot_brightness)
                combined_brightness = self.combine_brightness(camera_brightness, screenshot_brightness, weight_camera, weight_screenshot)
                brightness_diff = np.abs(combined_brightness - smoothed_brightness)
                setpoint = combined_brightness if brightness_diff > 10 else smoothed_brightness
                output, integral_term, prev_error = self.pid_controller(setpoint, smoothed_brightness, kp, ki, kd, dt=self.update_interval, integral_term=integral_term, prev_error=prev_error)
                prev_camera_brightness = camera_brightness
                prev_screenshot_brightness = screenshot_brightness
                prev_brightness = smoothed_brightness
                smoothed_brightness = np.clip(smoothed_brightness + output, 0, 100)
                sbc.set_brightness(smoothed_brightness)
                self.save_state((prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd))
                self.last_update_time = time.time()
                if np.abs(smoothed_brightness - prev_brightness) > 1:
                    self.last_brightness_change_time = time.time()
                self.adjust_num_threads()
                self.adjust_batch_size()
                kp, ki, kd = self.adjust_pid_parameters(setpoint, smoothed_brightness, kp, ki, kd)
                time.sleep(self.update_interval)
        except Exception as e:
                    print(f'Error: {str(e)} at {datetime.now().strftime("%H:%M:%S")}')
        finally:
                self.release_resources()
                print("Exiting at", datetime.now().strftime("%H:%M:%S"))

if __name__ == "__main__":
    bc = BrightnessController()
    bc.run()