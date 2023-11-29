# With this sample, you can define and register the callback function for monitoring the camera connection status.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *


class CustomCallback(EventCallbackBase):
    def __init__(self):
        super().__init__()

    def run(self, event):
        print(
            "A camera event has occurred. The event ID is {0}.".format(event))


class RegisterCameraEvent(object):
    def __init__(self):
        self.camera = Camera()

    def main(self):
        if not find_and_connect(self.camera):
            return

        device_event = CameraEvent()
        callback = CustomCallback()
        print("Register the callback function for camera disconnection events.")
        show_error(device_event.register_camera_event_callback(
            self.camera, callback, CameraEvent.CAMERA_EVENT_DISCONNECTED))

        self.camera.disconnect()
        print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = RegisterCameraEvent()
    a.main()
