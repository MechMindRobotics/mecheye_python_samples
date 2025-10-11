# With this sample, you can acquire profile data triggered non-stop with software, and save the resulting intensity images and depth maps.

from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *
import cv2
import numpy as np
from time import sleep
from multiprocessing import Lock

mutex = Lock()
kRetrieveFrameCount = 3


class CustomAcquisitionCallback(AcquisitionCallbackBase):
    def __init__(self, width):
        AcquisitionCallbackBase.__init__(self)
        self.callback_counter = 0

    def run(self, batch: ProfileBatch):
        mutex.acquire()
        if self.callback_counter >= kRetrieveFrameCount:
            mutex.release()
            return
        status = batch.get_error_status()
        if not status.is_ok():
            print("Callback batch data with error:")
            show_error(status)
        if batch.check_flag(ProfileBatch.BatchFlag_Incomplete):
            print("Part of the batch's data is lost, the number of valid profiles is:",
                  batch.valid_height())
        print("Save the depth map and intensity image.")
        cv2.imwrite("DepthMap_" + str(self.callback_counter) +
                    ".tiff", batch.get_depth_map().data())
        cv2.imwrite("IntensityImage_" + str(self.callback_counter) +
                    ".png", batch.get_intensity_image().data())
        self.callback_counter = self.callback_counter + 1
        mutex.release()


class TriggerWithSoftwareAndFixedRate(object):
    def __init__(self):
        self.profiler = Profiler()

    def set_parameters(self):
        self.user_set = self.profiler.current_user_set()

        # Set the "Data Acquisition Method" parameter to "Nonstop"
        show_error(self.user_set.set_enum_value(
            DataAcquisitionMethod.name, DataAcquisitionMethod.Value_Nonstop))

        # # Set the "Data Acquisition Trigger Source" parameter to "Software"
        # show_error(self.user_set.set_enum_value(
        #     DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_Software))

        # # Set the "Line Scan Trigger Source" parameter to "Fixed rate"
        # show_error(self.user_set.set_enum_value(
        #     LineScanTriggerSource.name, LineScanTriggerSource.Value_FixedRate))
        # # Set the " Software Trigger Rate" to 1000 Hz
        # show_error(self.user_set.set_float_value(
        #     SoftwareTriggerRate.name, 1000))

        error, self.data_width = self.user_set.get_int_value(
            DataPointsPerProfile.name)
        show_error(error)

        error, data_acquisition_trigger_source = self.user_set.get_enum_value(
            DataAcquisitionTriggerSource.name)
        show_error(error)
        self.is_software_trigger = data_acquisition_trigger_source == DataAcquisitionTriggerSource.Value_Software

    def acquire_profile_data_using_callback(self) -> bool:
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
            if self.callback.callback_counter < kRetrieveFrameCount:
                mutex.release()
                sleep(0.5)
            else:
                mutex.release()
                break

        print("Stop data acquisition.")
        status = self.profiler.stop_acquisition()
        if not status.is_ok():
            show_error(status)
        return True

    def main(self):
        if not find_and_connect(self.profiler):
            return -1

        if not confirm_capture():
            return -1

        self.set_parameters()

        # Acquire the profile data using the callback function
        if not self.acquire_profile_data_using_callback():
            return -1

        self.profiler.disconnect()
        print("Disconnected from the Mech-Eye Profiler successfully")
        return 0


if __name__ == '__main__':
    a = TriggerWithSoftwareAndFixedRate()
    a.main()
