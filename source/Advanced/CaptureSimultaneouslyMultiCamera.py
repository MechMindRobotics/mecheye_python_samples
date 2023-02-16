import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
import threading
from MechEye import Device
from source import Common


class CaptureThread (threading.Thread):
    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device

    def run(self):
        device_info = self.device.get_device_info()
        print("Camera {} start capturing.".format(device_info.id))
        self.device.capture_color()
        self.device.capture_depth()
        self.device.capture_point_xyz()
        self.device.capture_point_xyz_bgr()

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")


class CaptureSimultaneouslyMultiCamera(object):
    def __init__(self):
        self.device = Device()

    def connect_device_and_capture(self):
        devices = []
        for index in self.indices:
            device = Device()
            error_status = device.connect(self.device_list[index])
            if not error_status.ok():
                print(error_status.description())
                quit()
            devices.append(device)

        for device in devices:
            capture_thread = CaptureThread(device)
            capture_thread.start()
            capture_thread.join()

    def main(self):
        Common.find_camera_list(self)
        Common.choose_multi_camera(self)
        if len(self.indices) != 0:
            self.connect_device_and_capture()
        else:
            print("No camera was selected.")


if __name__ == '__main__':
    a = CaptureSimultaneouslyMultiCamera()
    a.main()
