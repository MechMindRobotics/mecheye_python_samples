# With this sample, you can define and register the callback function for monitoring the camera connection status.
import cv2
import time
from datetime import datetime

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *


class CustomCallback(EventCallbackBase):
    def __init__(self):
        super().__init__()

    def process_event_with_payload(self, event_data: EventData, extra_payload: Payload):
        print(
            "A camera event has occurred.")
        print("\tEvent ID: {0}".format(event_data.event_id))
        if event_data.event_name != "":
            print("\tEvent Name: {0}".format(event_data.event_name))
        print("\tFrame ID: {0}".format(event_data.frame_id))
        print("\tTimestamp: {0}".format(
            datetime.fromtimestamp(event_data.timestamp / 1000)))
        for member in extra_payload:
            if member.type == PayloadMember.Type__UInt32:
                print("\t{0} : {1}".format(
                    member.name, member.value.uint_32value))
            elif member.type == PayloadMember.Type__Int32:
                print("\t{0} : {1}".format(
                    member.name, member.value.int_32value))
            elif member.type == PayloadMember.Type__Int64:
                print("\t{0} : {1}".format(
                    member.name, member.value.int_64value))
            elif member.type == PayloadMember.Type__Float:
                print("\t{0} : {1}".format(
                    member.name, member.value.float_value))
            elif member.type == PayloadMember.Type__Double:
                print("\t{0} : {1}".format(
                    member.name, member.value.double_value))
            elif member.type == PayloadMember.Type__Bool:
                print("\t{0} : {1}".format(
                    member.name, member.value.bool_value))
            elif member.type == PayloadMember.Type__String:
                print("\t{0} : {1}".format(
                    member.name, member.value.string_value))


class RegisterCameraEvent(object):
    def __init__(self):
        self.camera = Camera()

    def register_events(self):
        supported_events = EventInfos()
        show_error(CameraEvent.get_supported_events(
            self.camera, supported_events))
        camera_event = CameraEvent()
        self.callback = CustomCallback()
        print("\nEvents supported on this camera")
        for event_info in supported_events:
            print()
            print(event_info.event_name, event_info.event_id)
            print("Register the callback function for the event ",
                  event_info.event_name)
            show_error(camera_event.register_camera_event_callback(
                self.camera, event_info.event_id, self.callback))
        print()

    def capture_depth_map(self):
        r"""
        If the 3D data has been acquired successfully, the callback function will detect the CAMERA_EVENT_EXPOSURE_END event.
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

        self.register_events()

        self.capture_depth_map()

        # Set the heartbeat interval to 2 seconds
        show_error(self.camera.set_heartbeat_interval(2000))

        # Let the program sleep for 20 seconds. During this period, if the camera disconnects, the
        # callback function will detect and report the disconnection. To test the event mechanism, you
        # can disconnect the camera Ethernet cable during this period.
        print("Wait for 20 seconds for disconnect event.")
        time.sleep(20)

        self.camera.disconnect()
        print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = RegisterCameraEvent()
    a.main()
