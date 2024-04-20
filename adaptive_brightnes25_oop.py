import cv2
import numpy as np
import screen_brightness_control as sbc
from screen_brightness_control.exceptions import NoValidDisplayError
from datetime import datetime
import time
import pyautogui
from threading import Thread, Event
from queue import Queue, Empty
import pickle
import pynput
import pretty_errors as pe
import ctypes


class BrightnessController:
    def __init__(self, camera_index=0, num_threads=4, frame_queue_size=100, brightness_queue_size=100,
                 batch_size=5, frame_interval=0.1, update_interval=1, inactivity_threshold=300):
        self.camera_index = camera_index
        self.num_threads = num_threads
        self.frame_queue_size = frame_queue_size
        self.brightness_queue_size = brightness_queue_size
        self.batch_size = batch_size
        self.frame_interval = frame_interval
        self.update_interval = update_interval
        self.inactivity_threshold = inactivity_threshold
        self.setup_state()
        self.stop_event = Event()
        self.last_activity_time = time.time()
        self.is_active = True
        self.inactivity_printed = False
        self.inactivity_check_interval = 1
        self.last_screenshot_time = 0
        self.consecutive_errors = 0
        self.cap = cv2.VideoCapture(self.camera_index)
        self.prev_camera_brightness = None
        self.prev_screenshot_brightness = None
        self.brightness_change_threshold = 10
        self.brightness_smoothing_factor = 0.5
        self.min_brightness = 5
        self.max_brightness = 95
        self.max_integral_term = 50
        self.kp, self.ki, self.kd = 0.6, 0.15, 0.08
        self.camera_weight = 0.7
        self.screenshot_weight = 0.3

    def setup_state(self):
        self.state = self.load_state()
        if self.state is None:
            try:
                self.prev_brightness = sbc.get_brightness()[0]
            except NoValidDisplayError:
                self.prev_brightness = 50
            self.smoothed_brightness = self.prev_brightness
            self.integral_term = 0
            self.prev_error = 0
        else:
            (self.prev_brightness, self.smoothed_brightness, self.integral_term,
             self.prev_error, self.kp, self.ki, self.kd) = self.state

    def is_screensaver_active(self):
        return ctypes.windll.user32.SystemParametersInfoW(114, 0, None, 0)

    def on_activity(self, *_):
        self.last_activity_time = time.time()
        self.is_active = True
        self.inactivity_printed = False
        self.inactivity_check_interval = 1
        self.stop_event.clear()
        self.update_interval = max(self.update_interval / 2, 0.1)
        if not self.is_screensaver_active():
            self.turn_on_keyboard_backlight()
            self.load_state()

    def on_inactivity(self):
        self.save_state((self.prev_brightness, self.smoothed_brightness,
                        self.integral_term, self.prev_error, self.kp, self.ki, self.kd))
        self.is_active = False
        self.stop_event.set()
        cv2.destroyAllWindows()
        while not self.when_go_to_sleep():
            self.is_active = False
            if not self.inactivity_printed:
                print(f'Inactivity detected at {
                      datetime.now().strftime("%H:%M:%S")}')
                self.inactivity_printed = True
            if self.is_screensaver_active():
                self.pause_brightness_control()
            self.inactivity_check_interval = min(
                self.inactivity_check_interval * 2, 60)
            self.update_interval = max(self.update_interval * 2, 1)
            return False
        else:
            self.is_active = True
            self.inactivity_printed = False
            return True

    def when_go_to_sleep(self):
        while True:
            if time.time() - self.last_activity_time > self.inactivity_threshold and not self.is_active and self.stop_event.is_set():
                self.on_inactivity()
            else:
                self.on_activity()
                return True

    def pause_brightness_control(self):
        self.stop_event.set()
        self.turn_off_keyboard_backlight()

    def turn_on_keyboard_backlight(self):
        pass

    def turn_off_keyboard_backlight(self):
        pass

    def analyze_image(self, frame):
        brightness = cv2.mean(frame)[0] / 255 * 100
        return brightness

    def get_screenshot_brightness(self):
        if self.when_go_to_sleep():
            try:
                screenshot = pyautogui.screenshot(region=(0, 0, 100, 100))
                screenshot = np.array(screenshot)
                screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
                brightness = self.analyze_image(screenshot)
                self.last_screenshot_time = time.time()
                self.consecutive_errors = 0
                return brightness
            except Exception as e:
                self.on_inactivity()
                self.consecutive_errors += 1
                return None
        else:
            return None

    def get_screenshot_brightness_thread(self, screenshot_brightness_queue):
        while not self.stop_event.is_set():
            if self.is_active:
                screenshot_brightness = self.get_screenshot_brightness()
                if screenshot_brightness is not None:
                    screenshot_brightness_queue.put(screenshot_brightness)
                time.sleep(1)
            else:
                self.save_state((self.prev_brightness, self.smoothed_brightness,
                                self.integral_term, self.prev_error, self.kp, self.ki, self.kd))
                time.sleep(self.inactivity_check_interval)
                self.inactivity_check_interval = min(
                    self.inactivity_check_interval * 2, 60)

    def process_frames(self, frame_queue, brightness_queue):
        frames = []
        last_frame_time = time.time()
        while not self.stop_event.is_set():
            if self.is_active:
                if time.time() - last_frame_time >= self.frame_interval:
                    frame = frame_queue.get()
                    if frame is None:
                        break
                    frames.append(frame)
                    if len(frames) == self.batch_size:
                        avg_frame = cv2.GaussianBlur(
                            np.stack(frames), (1, 1), 0)
                        brightness = self.analyze_image(avg_frame)
                        brightness_queue.put(brightness)
                        frames = []
                    last_frame_time = time.time()
            else:
                time.sleep(self.inactivity_check_interval)

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
        mouse_listener = pynput.mouse.Listener(
            on_move=self.on_activity, on_click=self.on_activity, on_scroll=self.on_activity)
        mouse_listener.start()
        keyboard_listener = pynput.keyboard.Listener(
            on_press=self.on_activity, on_release=self.on_activity)
        keyboard_listener.start()
        last_update_time = time.time()
        last_brightness_change_time = time.time()

        try:
            while not self.stop_event.is_set():
                self.when_go_to_sleep()
                if self.is_active:
                    try:
                        current_brightness = sbc.get_brightness()[0]
                    except NoValidDisplayError:
                        current_brightness = self.prev_brightness
                    brightness_diff = abs(
                        current_brightness - self.prev_brightness)
                    if brightness_diff > self.brightness_change_threshold:
                        print(f'Brightness changed to {current_brightness}% at {
                              datetime.now().strftime("%H:%M:%S")}')
                        self.smoothed_brightness = current_brightness
                        self.integral_term = 0
                        self.prev_error = 0

                    ret, frame = self.cap.read()
                    if not ret:
                        print(f"Error reading frame from camera. Exiting...at {
                              datetime.now().strftime('%H:%M:%S')}")
                        camera_brightness = self.prev_camera_brightness if self.prev_camera_brightness is not None else 50
                    else:
                        frame_queue.put(frame)
                        try:
                            camera_brightness = brightness_queue.get(
                                block=True, timeout=1)
                        except Empty:
                            camera_brightness = self.prev_camera_brightness if self.prev_camera_brightness is not None else 50

                    try:
                        screenshot_brightness = screenshot_brightness_queue.get(
                            block=False)
                    except Empty:
                        screenshot_brightness = self.prev_screenshot_brightness if self.prev_screenshot_brightness is not None else 50

                    self.prev_camera_brightness = camera_brightness
                    self.prev_screenshot_brightness = screenshot_brightness

                    combined_brightness = self.camera_weight * camera_brightness + \
                        self.screenshot_weight * screenshot_brightness

                    brightness_diff = abs(
                        combined_brightness - self.smoothed_brightness)
                    if brightness_diff > self.brightness_change_threshold:
                        setpoint = combined_brightness
                        self.integral_term = 0
                        self.prev_error = 0
                    else:
                        setpoint = self.smoothed_brightness

                    error = setpoint - self.smoothed_brightness
                    self.integral_term = max(-self.max_integral_term, min(
                        self.max_integral_term, self.integral_term + error * self.update_interval))
                    derivative_term = (
                        error - self.prev_error) / self.update_interval
                    output = self.kp * error + self.ki * \
                        self.integral_term + self.kd * derivative_term
                    output = max(-10, min(10, output))
                    self.prev_error = error
                    self.smoothed_brightness += output * self.brightness_smoothing_factor
                    self.smoothed_brightness = max(self.min_brightness, min(
                        self.max_brightness, self.smoothed_brightness))

                    try:
                        sbc.set_brightness(round(self.smoothed_brightness))
                        if abs(self.smoothed_brightness - self.prev_brightness) > self.brightness_change_threshold:
                            print(f'New brightness: {round(self.smoothed_brightness)}% at {
                                  datetime.now().strftime("%H:%M:%S")}')
                            self.prev_brightness = self.smoothed_brightness
                            last_brightness_change_time = time.time()
                        else:
                            self.when_go_to_sleep()
                            print("-", end="")
                        if self.smoothed_brightness < 20:
                            self.turn_on_keyboard_backlight()
                        self.save_state((self.prev_brightness, self.smoothed_brightness,
                                         self.integral_term, self.prev_error, self.kp, self.ki, self.kd))
                    except NoValidDisplayError:
                        print(f"Error setting brightness: no displays detected at {
                              datetime.now().strftime('%H:%M:%S')}")
                        self.smoothed_brightness = self.prev_brightness
                        self.update_interval = max(self.update_interval * 2, 1)
                        exit()

                    self.update_interval = min(self.update_interval * 1.5, 5) if time.time(
                    ) - last_brightness_change_time > 5 else max(self.update_interval / 1.5, 0.1)
                    time.sleep(self.update_interval)
                else:
                    time.sleep(self.inactivity_check_interval)
        except KeyboardInterrupt:
            print(f'KeyboardInterrupt at {
                  datetime.now().strftime("%H:%M:%S")}')
        finally:
            self.stop_event.set()
            mouse_listener.stop()
            keyboard_listener.stop()
            for _ in range(self.num_threads):
                frame_queue.put(None)
            self.cap.release()
            cv2.destroyAllWindows()

    def load_state(self):
        try:
            with open('brightness_controller_state.pkl', 'rb') as f:
                state = pickle.load(f)
                return state
        except (FileNotFoundError, ValueError, EOFError):
            return None

    def save_state(self, state):
        with open('brightness_controller_state.pkl', 'wb') as f:
            pickle.dump(state, f)


if __name__ == '__main__':
    controller = BrightnessController()
    controller.adjust_screen_brightness()
