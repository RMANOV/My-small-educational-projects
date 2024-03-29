import cv2
import numpy as np
import screen_brightness_control as sbc
from datetime import datetime
import time
import pyautogui
from threading import Thread, Event
from queue import Queue
import pickle
import queue


class BrightnessController:
    def __init__(self, camera_index=0, num_threads=4, frame_queue_size=100, brightness_queue_size=100,
                 batch_size=5, frame_interval=0.1, update_interval=1):
        self.camera_index = camera_index
        self.num_threads = num_threads
        self.frame_queue_size = frame_queue_size
        self.brightness_queue_size = brightness_queue_size
        self.batch_size = batch_size
        self.frame_interval = frame_interval
        self.update_interval = update_interval
        self.state = self.load_state()
        if self.state is None:
            self.prev_brightness = sbc.get_brightness()[0]
            self.smoothed_brightness = self.prev_brightness
            self.integral_term = 0
            self.prev_error = 0
            self.kp, self.ki, self.kd = 0.6, 0.15, 0.08
        else:
            self.prev_brightness, self.smoothed_brightness, self.integral_term, self.prev_error, self.kp, self.ki, self.kd = self.state
        self.stop_event = Event()

    def turn_on_keyboard_backlight(self):
        pass

    def turn_off_keyboard_backlight(self):
        pass

    def analyze_image(self, frame):
        brightness = cv2.meanStdDev(frame)[0][0][0] / 255 * 100
        return brightness

    def get_screenshot_brightness(self):
        while not self.stop_event.is_set():
            try:
                screenshot = pyautogui.screenshot()
                screenshot = np.array(screenshot)
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
                brightness = cv2.meanStdDev(screenshot)[0][0][0] / 255 * 100
                return brightness
            except Exception as e:
                print(f"Error getting screenshot brightness: {str(e)} at {datetime.now().strftime('%H:%M:%S')}")
                time.sleep(self.update_interval*10)
                self.update_interval = max(self.update_interval * 1.5, 5)
                self.save_state((self.prev_brightness, self.smoothed_brightness,
                                 self.integral_term, self.prev_error, self.kp, self.ki, self.kd))
                cv2.destroyAllWindows()

    def get_screenshot_brightness_thread(self, screenshot_brightness_queue):
        while not self.stop_event.is_set():
            screenshot_brightness = self.get_screenshot_brightness()
            screenshot_brightness_queue.put(screenshot_brightness)
            time.sleep(0.1)

    def process_frames(self, frame_queue, brightness_queue):
        frames = []
        last_frame_time = time.time()
        while not self.stop_event.is_set():
            if time.time() - last_frame_time >= self.frame_interval:
                frame = frame_queue.get()
                if frame is None:
                    break
                frames.append(frame)
                if len(frames) == self.batch_size:
                    avg_frame = cv2.GaussianBlur(np.stack(frames), (1, 1), 0)
                    brightness = self.analyze_image(avg_frame)
                    brightness_queue.put(brightness)
                    frames = []
                last_frame_time = time.time()

    def adjust_screen_brightness(self):
        print(f'Initial brightness: {round(self.prev_brightness)}% at {
              datetime.now().strftime("%H:%M:%S")}')
        frame_queue = Queue(maxsize=self.frame_queue_size)
        brightness_queue = Queue(maxsize=self.brightness_queue_size)
        for _ in range(self.num_threads):
            t = Thread(target=self.process_frames,
                       args=(frame_queue, brightness_queue))
            t.start()

        screenshot_brightness_queue = Queue()
        screenshot_thread = Thread(target=self.get_screenshot_brightness_thread, args=(
            screenshot_brightness_queue,))
        screenshot_thread.start()

        last_update_time = time.time()
        last_brightness_change_time = time.time()

        cap = None
        try:
            cap = cv2.VideoCapture(self.camera_index)
            if not cap.isOpened():
                print(f'Cannot open camera. Exiting...at {datetime.now().strftime("%H:%M:%S")}')
                return

            prev_camera_brightness = None
            prev_screenshot_brightness = None

            while not self.stop_event.is_set():
                current_brightness = sbc.get_brightness()[0]
                if abs(current_brightness - self.prev_brightness) > 10:
                    print(f'Brightness changed to {current_brightness}% at {
                          datetime.now().strftime("%H:%M:%S")}')
                    self.smoothed_brightness = current_brightness
                    self.integral_term = 0
                    self.prev_error = 0

                ret, frame = cap.read()
                if not ret:
                    print(f"Error reading frame from camera. Exiting...at {datetime.now().strftime('%H:%M:%S')}")
                    camera_brightness = prev_camera_brightness if prev_camera_brightness is not None else 50
                else:
                    frame_queue.put(frame)
                    try:
                        camera_brightness = brightness_queue.get(
                            block=True, timeout=1)
                    except queue.Empty:
                        camera_brightness = prev_camera_brightness if prev_camera_brightness is not None else 50

                try:
                    screenshot_brightness = screenshot_brightness_queue.get(
                        block=False)
                except queue.Empty:
                    screenshot_brightness = prev_screenshot_brightness if prev_screenshot_brightness is not None else 50

                if prev_camera_brightness is None:
                    prev_camera_brightness = camera_brightness
                if prev_screenshot_brightness is None:
                    prev_screenshot_brightness = screenshot_brightness

                weight_camera = camera_brightness / 100
                weight_screenshot = 1/2 * \
                    (1 - weight_camera) * (1 - weight_camera)
                combined_brightness = weight_camera * camera_brightness + \
                    weight_screenshot * screenshot_brightness

                brightness_diff = abs(
                    combined_brightness - self.smoothed_brightness)
                if brightness_diff > 10:
                    setpoint = combined_brightness
                    self.integral_term = 0
                    self.prev_error = 0
                else:
                    setpoint = self.smoothed_brightness

                error = setpoint - self.smoothed_brightness
                self.integral_term = max(-50, min(50,
                                         self.integral_term + error * self.update_interval))
                derivative_term = (error - self.prev_error) / \
                    self.update_interval
                output = self.kp * error + self.ki * \
                    self.integral_term + self.kd * derivative_term
                output = max(-10, min(10, output))
                self.prev_error = error

                self.smoothed_brightness += output
                self.smoothed_brightness = max(
                    5, min(95, self.smoothed_brightness))

                try:
                    sbc.set_brightness(round(self.smoothed_brightness))
                    if abs(self.smoothed_brightness - self.prev_brightness) > 5:
                        print(f'New brightness: {round(self.smoothed_brightness)}% at {
                              datetime.now().strftime("%H:%M:%S")}')
                        self.prev_brightness = self.smoothed_brightness
                        last_brightness_change_time = time.time()
                    else:
                        print("-", end="")

                    if self.smoothed_brightness < 20:
                        self.turn_on_keyboard_backlight()

                    self.save_state((self.prev_brightness, self.smoothed_brightness,
                                     self.integral_term, self.prev_error, self.kp, self.ki, self.kd))
                except Exception as e:
                    print(f"Error setting brightness: {str(e)} at {datetime.now().strftime('%H:%M:%S')}")

                if time.time() - last_brightness_change_time > 5:
                    self.update_interval = min(self.update_interval * 1.5, 5)
                else:
                    self.update_interval = max(self.update_interval / 1.5, 1)

                prev_camera_brightness = camera_brightness
                prev_screenshot_brightness = screenshot_brightness

                time.sleep(self.update_interval)

        except KeyboardInterrupt:
            print(f'KeyboardInterrupt at {datetime.now().strftime("%H:%M:%S")}')
        finally:
            self.stop_event.set()
            for _ in range(self.num_threads):
                frame_queue.put(None)
            if cap is not None:
                cap.release()
            cv2.destroyAllWindows()

    def load_state(self):
        try:
            with open('brightness_controller_state.pkl', 'rb') as f:
                state = pickle.load(f)
                prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd = state
                return prev_brightness, smoothed_brightness, integral_term, prev_error, kp, ki, kd
        except (FileNotFoundError, ValueError):
            return None

    def save_state(self, state):
        with open('brightness_controller_state.pkl', 'wb') as f:
            pickle.dump(state, f)


if __name__ == '__main__':
    controller = BrightnessController()
    controller.adjust_screen_brightness()
