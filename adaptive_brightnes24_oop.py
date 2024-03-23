import cv2
import numpy as np
import screen_brightness_control as sbc
from datetime import datetime
import time
import pyautogui
from threading import Thread, Event
from queue import Queue, Empty
import pickle
import pynput
import pretty_errors as pe


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
        self.last_activity_time = time.time()
        self.is_active = True
        self.inactivity_printed = False
        self.inactivity_check_interval = 1
        self.last_screenshot_time = 0
        self.consecutive_errors = 0

    def on_activity(self):
        self.last_activity_time = time.time()
        self.is_active = True
        self.inactivity_printed = False
        self.inactivity_check_interval = 1
        self.stop_event.clear()  # Resume the threads
        # Decrease update interval if system is active
        self.update_interval = max(self.update_interval / 2, 1)
        # Resume the brightness control
        self.turn_on_keyboard_backlight()
        # Load state if system is active
        state = self.load_state()


    def on_inactivity(self):
    #     self.is_active = False
    #     self.inactivity_printed = True
    #     # Increase update interval if system is inactive
    #     self.update_interval = min(self.update_interval * 5, 10000000000000000)
    #     self.consecutive_errors = 0
    #     # Save state if system is inactive
    #     self.save_state((self.prev_brightness, self.smoothed_brightness,
    #                     self.integral_term, self.prev_error, self.kp, self.ki, self.kd))
    #     # Pause the brightness control
    #     self.turn_off_keyboard_backlight()
    #     # Print message if system is inactive
    #     print(f'Inactivity detected at {datetime.now().strftime("%H:%M:%S")}')
    #     # Increase inactivity check interval if system is inactive

        # self.stop_event.set()
        # self.when_go_to_sleep()
        # if self.when_go_to_sleep():
        #     self.on_activity()
        # else:
        #     self.on_inactivity()

        self.is_active = False
        self.inactivity_printed = True
        # Increase update interval if system is inactive
        # self.update_interval = min(self.update_interval * 5, 10000000000000000) 
        # self.consecutive_errors = 0
        # Save state if system is inactive
        self.save_state((self.prev_brightness, self.smoothed_brightness, self.integral_term, self.prev_error, self.kp, self.ki, self.kd))
        # Pause the brightness control
        self.turn_off_keyboard_backlight()
        # Print message if system is inactive
        print(f'Inactivity detected at {datetime.now().strftime("%H:%M:%S")}')
        # Increase inactivity check interval if system is inactive
        # self.inactivity_check_interval = min(self.inactivity_check_interval * 1000, 10000000000000000)
        self.stop_event.set()
        cv2.destroyAllWindows()
        
        self.when_go_to_sleep()
        while True:
            if self.when_go_to_sleep():
                self.on_activity()
            else:
                self.on_inactivity()
                time.sleep(self.inactivity_check_interval^2)



    def when_go_to_sleep(self):
        # if time.time() - self.last_activity_time > self.inactivity_threshold and not self.is_active and self.stop_event.is_set():
        #     self.on_inactivity()  # Pause the brightness control
        #     return False
        # else:
        #     self.on_activity()  # Resume the brightness control
        #     return True
        while True:
            if time.time() - self.last_activity_time > self.inactivity_threshold and not self.is_active and self.stop_event.is_set():
                self.on_inactivity()  # Pause the brightness control
                return False
            else:
                self.on_activity()  # Resume the brightness control
                return True


    def turn_on_keyboard_backlight(self):
        pass

    def turn_off_keyboard_backlight(self):
        pass

    def analyze_image(self, frame):
        brightness = cv2.meanStdDev(frame)[0][0][0] / 255 * 100
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
        cap = None
        try:
            cap = cv2.VideoCapture(self.camera_index)
            if not cap.isOpened():
                print(f'Cannot open camera. Exiting...at {
                      datetime.now().strftime("%H:%M:%S")}')
                return
            prev_camera_brightness = None
            prev_screenshot_brightness = None
            while not self.stop_event.is_set():
                self.when_go_to_sleep()
                if self.is_active:
                    current_brightness = sbc.get_brightness()[0]
                    if abs(current_brightness - self.prev_brightness) > 10:
                        print(f'Brightness changed to {current_brightness}% at {
                              datetime.now().strftime("%H:%M:%S")}')
                        self.smoothed_brightness = current_brightness
                        self.integral_term = 0
                        self.prev_error = 0

                    ret, frame = cap.read()
                    if not ret:
                        print(f"Error reading frame from camera. Exiting...at {
                              datetime.now().strftime('%H:%M:%S')}")
                        camera_brightness = prev_camera_brightness if prev_camera_brightness is not None else 50
                    else:
                        frame_queue.put(frame)
                        try:
                            camera_brightness = brightness_queue.get(
                                block=True, timeout=1)
                        except Empty:
                            camera_brightness = prev_camera_brightness if prev_camera_brightness is not None else 50

                    try:
                        screenshot_brightness = screenshot_brightness_queue.get(
                            block=False)
                    except Empty:
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
                    self.integral_term = max(
                        -50, min(50, self.integral_term + error * self.update_interval))
                    derivative_term = (
                        error - self.prev_error) / self.update_interval
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
                        print(f"Error setting brightness: {str(e)} at {
                              datetime.now().strftime('%H:%M:%S')}")

                    if time.time() - last_brightness_change_time > 5:
                        self.update_interval = min(
                            self.update_interval * 1.5, 5)
                    else:
                        self.update_interval = max(
                            self.update_interval / 1.5, 1)

                    prev_camera_brightness = camera_brightness
                    prev_screenshot_brightness = screenshot_brightness
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
