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


class BlindSpotFilter(object):
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

    def save_depth_and_intensity(self, depth_file_name, intensity_file_name):
        cv2.imwrite(depth_file_name,
                    self.profile_batch.get_depth_map().data())
        cv2.imwrite(intensity_file_name,
                    self.profile_batch.get_intensity_image().data())

    def main(self):
        if not find_and_connect(self.profiler):
            return -1

        if not confirm_capture():
            return -1

        self.user_set = self.profiler.current_user_set()
        # Enable the blind spot filtering function
        show_error(self.user_set.set_bool_value(
            EnableBlindSpotFiltering.name, True))

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

        if self.profile_batch.check_flag(ProfileBatch.BatchFlag_Incomplete):
            print("Part of the batch's data is lost, the number of valid profiles is:",
                  self.profile_batch.valid_height())

        print("Save the depth map and intensity image")
        self.save_depth_and_intensity("depth.tiff", "intensity.png")

        # # Uncomment the following line to save a virtual device file using the ProfileBatch acquired.
        # self.profiler.save_virtual_device_file(self.profile_batch, "test.mraw")

        self.profiler.disconnect()
        print("Disconnected from the Mech-Eye Profiler successfully")
        return 0


if __name__ == '__main__':
    a = BlindSpotFilter()
    a.main()
