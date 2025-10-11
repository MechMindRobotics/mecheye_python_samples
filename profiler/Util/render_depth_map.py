# With this sample, you can obtain and save the depth map rendered with the jet color scheme.

from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *
import cv2
import numpy as np
from time import sleep
from multiprocessing import Lock

mutex = Lock()


class CustomAcquisitionCallback(AcquisitionCallbackBase):
    def __init__(self, width):
        AcquisitionCallbackBase.__init__(self)
        self.profile_batch = ProfileBatch(width)

    def run(self, batch):
        mutex.acquire()
        if (not batch.get_error_status().is_ok()):
            print("Error occurred during data acquisition.")
            show_error(batch.get_error_status())
        self.profile_batch.append(batch)
        mutex.release()


class RenderedDepthMap(object):
    def __init__(self):
        self.profiler = Profiler()

    def acquire_profile_data_using_callback(self) -> bool:
        self.profile_batch.clear()

        # Set a large CallbackRetrievalTimeout
        show_error(self.user_set.set_int_value(
            CallbackRetrievalTimeout.name, 60000))

        self.callback = CustomAcquisitionCallback(self.data_width)

        # Register the callback function
        status = self.profiler.register_acquisition_callback(
            self.callback)
        if not status.is_ok():
            show_error(status)
            return False

        # Call the start_acquisition to take the laser profiler into the acquisition ready status
        print("Start data acquisition")
        status = self.profiler.start_acquisition()
        if not status.is_ok():
            show_error(status)
            return False

        if self.is_software_trigger:
            status = self.profiler.trigger_software()
            if not status.is_ok():
                show_error(status)
                return False

        while True:
            mutex.acquire()
            if self.callback.profile_batch.is_empty():
                mutex.release()
                sleep(0.5)
            else:
                mutex.release()
                break

        print("Stop data acquisition.")
        status = self.profiler.stop_acquisition()
        if not status.is_ok():
            show_error(status)
        self.profile_batch.append(self.callback.profile_batch)
        return True

    def render_depth_data(self, depth):
        if depth is None or depth.size == 0:
            return np.array([])

        mask = np.isfinite(depth).astype(np.uint8)
        min_depth_value, max_depth_value, _, _ = cv2.minMaxLoc(depth, mask)

        if np.isclose(max_depth_value - min_depth_value, 0):
            depth8U = depth.astype(np.uint8)
        else:
            depth8U = cv2.convertScaleAbs(depth, alpha=(255.0 / (min_depth_value - max_depth_value)), beta=(
                (max_depth_value * 255.0) / (max_depth_value - min_depth_value) + 1))

        if depth8U.size == 0:
            return np.array([])

        colored_depth = cv2.applyColorMap(depth8U, cv2.COLORMAP_JET)
        colored_depth[depth8U == 0] = [0, 0, 0]

        return colored_depth

    def save_depth_and_intensity(self, depth_file_name, intensity_file_name, color_depth_file_name):
        cv2.imwrite(depth_file_name,
                    self.profile_batch.get_depth_map().data())
        cv2.imwrite(intensity_file_name,
                    self.profile_batch.get_intensity_image().data())
        rendered_depth = self.render_depth_data(
            self.profile_batch.get_depth_map().data())
        cv2.imwrite(color_depth_file_name, rendered_depth)

    def main(self):
        if not find_and_connect(self.profiler):
            return -1

        if not confirm_capture():
            return -1

        self.user_set = self.profiler.current_user_set()
        error, self.data_width = self.user_set.get_int_value(
            DataPointsPerProfile.name)
        show_error(error)
        self.profile_batch = ProfileBatch(self.data_width)

        error, data_acquisition_trigger_source = self.user_set.get_enum_value(
            DataAcquisitionTriggerSource.name)
        show_error(error)
        self.is_software_trigger = data_acquisition_trigger_source == DataAcquisitionTriggerSource.Value_Software
        # Acquire the profile data using the callback function
        if not self.acquire_profile_data_using_callback():
            return -1

        print("Save the depth map and intensity image")
        self.save_depth_and_intensity(
            "depth.tiff", "intensity.png", "renderedDepthMap.tiff")

        # # Uncomment the following line to save a virtual device file using the ProfileBatch acquired.
        # self.profiler.save_virtual_device_file(self.profile_batch, "test.mraw")

        self.profiler.disconnect()
        print("Disconnected from the Mech-Eye Profiler successfully")
        return 0


if __name__ == '__main__':
    a = RenderedDepthMap()
    a.main()
