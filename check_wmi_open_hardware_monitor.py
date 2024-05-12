import wmi


def check_open_hardware_monitor():
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        temperature_info = w.Sensor()
        if temperature_info:
            print("OpenHardwareMonitor е стартиран и предоставя данни чрез WMI.")
            for sensor in temperature_info:
                if sensor.SensorType == 'Temperature':
                    print(f"{sensor.Name}: {sensor.Value}°C")
        else:
            print(
                "OpenHardwareMonitor е стартиран, но не са намерени температурни сензори.")
    except wmi.x_wmi as e:
        print("Не може да се свърже с WMI namespace 'root\\OpenHardwareMonitor'.")
        print("Уверете се, че OpenHardwareMonitor е стартиран и е конфигуриран да предоставя данни чрез WMI.")
        print(f"Грешка: {e}")


check_open_hardware_monitor()
