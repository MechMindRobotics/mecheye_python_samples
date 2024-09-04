# With this sample, you can define and register the callback function for monitoring the camera connection status.
import cv2
import time

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *


class CustomCallback(EventCallbackBase):
    def __init__(self):
        super().__init__()

    def process_event(self, eventData):
        print(
            "A camera event has occurred. The event ID is {0}.".format(eventData.event_id))


class RegisterCameraEvent(object):
    def __init__(self):
        self.camera = Camera()

    def capture_depth_map(self):
        r"""
        Note: The CAMERA_EVENT_EXPOSURE_END event is only sent after the acquisition of the 3D data (Frame3D) has completed.
        To ensure both 2D and 3D data have been acquired before the event is sent, check the following recommendations:
        If the flash exposure mode is used for acquiring the 2D data, and the :py:class:FlashAcquisitionMode parameter is set to "Fast",
        call capture_3d() before calling capture_2d(). Otherwise, call capture_2d() before calling capture_3d().
        Alternatively, you can call capture_2d_and_3d() instead to avoid the timing issue.
        """
        frame3d = Frame3D()
        show_error(self.camera.capture_3d(frame3d))

        depth_map = frame3d.get_depth_map()
        depth_file = "DepthMap.tiff"
        cv2.imwrite(depth_file, depth_map.data())
        print("Capture and save the depth map: {}".format(depth_file))

    def main(self):
        if not find_and_connect(self.camera):
            return

        device_event = CameraEvent()
        callback = CustomCallback()

        print("Register the callback function for camera exposure end event.")
        show_error(device_event.register_camera_event_callback(
            self.camera, CameraEvent.CAMERA_EVENT_EXPOSURE_END, callback))

        self.capture_depth_map()

        show_error(device_event.unregister_camera_event_callback(self.camera, CameraEvent.CAMERA_EVENT_EXPOSURE_END))

        print("Register the callback function for camera disconnection event.")
        show_error(device_event.register_camera_event_callback(
            self.camera, CameraEvent.CAMERA_EVENT_DISCONNECTED, callback))

        time.sleep(20)

        show_error(device_event.unregister_camera_event_callback(self.camera, CameraEvent.CAMERA_EVENT_DISCONNECTED))

        self.camera.disconnect()
        print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = RegisterCameraEvent()
    a.main()
