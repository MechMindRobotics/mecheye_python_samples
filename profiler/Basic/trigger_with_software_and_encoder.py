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


class TriggerWithSoftwareAndEncoder(object):
    def __init__(self):
        self.profiler = Profiler()

    def set_timed_exposure(self, exposure_time: int):
        # Set the exposure mode to timed
        show_error(self.user_set.set_enum_value(
            ExposureMode.name, ExposureMode.Value_Timed))

        # Set the exposure time to {exposure_time} μs
        show_error(self.user_set.set_int_value(
            ExposureTime.name, exposure_time))

    def set_hdr_exposure(self, exposure_time: int, proportion1: float, proportion2: float, first_threshold: float, second_threshold: float):
        # Set the "Exposure Mode" parameter to "HDR"
        show_error(self.user_set.set_enum_value(
            ExposureMode.name, ExposureMode.Value_HDR))

        # Set the total exposure time to {exposure_time} μs
        show_error(self.user_set.set_int_value(
            ExposureTime.name, exposure_time))

        # Set the proportion of the first exposure phase to {proportion1}%
        show_error(self.user_set.set_float_value(
            HdrExposureTimeProportion1.name, proportion1))

        # Set the proportion of the first + second exposure phases to {proportion2}% (that is, the
        # second exposure phase occupies {proportion2 - proportion1}%, and the third exposure phase
        # occupies {100 - proportion2}% of the total exposure time)
        show_error(self.user_set.set_float_value(
            HdrExposureTimeProportion2.name, proportion2))

        # Set the first threshold to {first_threshold}. This limits the maximum grayscale value to
        # {first_threshold} after the first exposure phase is completed.
        show_error(self.user_set.set_float_value(
            HdrFirstThreshold.name, first_threshold))

        # Set the second threshold to {second_threshold}. This limits the maximum grayscale value to
        # {second_threshold} after the second exposure phase is completed.
        show_error(self.user_set.set_float_value(
            HdrSecondThreshold.name, second_threshold))

    def set_encoder_trigger(self, trigger_direction: int, trigger_signal_counting_mode: int, trigger_interval: int):
        # Set the trigger source to Encoder
        show_error(self.user_set.set_enum_value(
            LineScanTriggerSource.name, LineScanTriggerSource.Value_Encoder))
        # Set the encoder trigger direction to {trigger_direction}
        show_error(self.user_set.set_enum_value(
            EncoderTriggerDirection.name, trigger_direction))
        # Set the encoder signal counting mode to be {trigger_signal_counting_mode}
        show_error(self.user_set.set_enum_value(
            EncoderTriggerSignalCountingMode.name, trigger_signal_counting_mode))
        # Set the encoder trigger interval to {trigger_interval}
        show_error(self.user_set.set_int_value(
            EncoderTriggerInterval.name, trigger_interval))

    def set_parameters(self):
        self.user_set = self.profiler.current_user_set()

        # Set the exposure mode to timed
        # Set the exposure time to 100 μs
        self.set_timed_exposure(100)

        """
        You can also use the HDR exposure mode, in which the laser profiler exposes in three phases
        while acquiring one profile. In this mode, you need to set the total exposure time, the
        proportions of the three exposure phases, as well as the two thresholds of grayscale values. The
        code for setting the relevant parameters for the HDR exposure mode is given in the following
        comments.
        """
        # # Set the "Exposure Mode" parameter to "HDR"
        # # Set the total exposure time to 100 μs
        # # Set the proportion of the first exposure phase to 40%
        # # Set the proportion of the first + second exposure phases to 80% (that is, the second
        # # exposure phase occupies 40%, and the third exposure phase occupies 20% of the total
        # # exposure
        # # Set the first threshold to 10. This limits the maximum grayscale value to 10 after the
        # # first exposure phase is completed.
        # # Set the second threshold to 60. This limits the maximum grayscale value to 60 after the
        # # second exposure phase is completed.
        # self.set_hdr_exposure(100, 40, 80, 10, 60)

        # # Enable outlier removal and adjust the outlier removal intensity.
        # # Set the "EnableOutlierRemoval" parameter to true
        # show_error(self.user_set.set_bool_value(EnableOutlierRemoval.name,True))
        # # Set the "OutlierRemovalIntensity" parameter to "VeryLow"
        # show_error(self.user_set.set_enum_value(OutlierRemovalIntensity.name,OutlierRemovalIntensity.Value_VeryLow))

        # Set the "Data Acquisition Trigger Source" parameter to "Software"
        show_error(self.user_set.set_enum_value(
            DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_Software))

        # Set the "Line Scan Trigger Source" parameter to "Encoder"
        # Set the (encoder) "Trigger Direction" parameter to "Both"
        # Set the (encoder) "Trigger Signal Counting Mode" parameter to "1×"
        # Set the (encoder) "Trigger Interval" parameter to 10
        self.set_encoder_trigger(EncoderTriggerDirection.Value_Both,
                                 EncoderTriggerSignalCountingMode.Value_Multiple_1, 10)

        # Set the "Scan Line Count" parameter (the number of lines to be scanned) to 1600
        show_error(self.user_set.set_int_value(ScanLineCount.name, 1600))

        # Set the "Laser Power" parameter to 100
        show_error(self.user_set.set_int_value(LaserPower.name, 100))
        # Set the "Analog Gain" parameter to "Gain_2"
        show_error(self.user_set.set_enum_value(
            AnalogGain.name, AnalogGain.Value_Gain_2))
        # Set the "Digital Gain" parameter to 0
        show_error(self.user_set.set_int_value(DigitalGain.name, 0))

        # Set the "Minimum Grayscale Value" parameter to 50
        show_error(self.user_set.set_int_value(MinGrayscaleValue.name, 50))
        # Set the "Minimum Laser Line Width" parameter to 2
        show_error(self.user_set.set_int_value(MinLaserLineWidth.name, 2))
        # Set the "Maximum Laser Line Width" parameter to 20
        show_error(self.user_set.set_int_value(MaxLaserLineWidth.name, 20))
        # Set the "Spot Selection" parameter to "Strongest"
        show_error(self.user_set.set_enum_value(
            SpotSelection.name, SpotSelection.Value_Strongest))

        # This parameter is only effective for firmware 2.2.1 and below. For firmware 2.3.0 and above,
        # adjustment of this parameter does not take effect.
        # Set the minimum laser line intensity to 10
        show_error(self.user_set.set_int_value(MinSpotIntensity.name, 51))
        # This parameter is only effective for firmware 2.2.1 and below. For firmware 2.3.0 and above,
        # adjustment of this parameter does not take effect.
        # Set the maximum laser line intensity to 205
        show_error(self.user_set.set_int_value(MaxSpotIntensity.name, 205))

        """
        Set the "Gap Filling" parameter to 16, which controls the size of the gaps that can be filled
        in the profile. When the number of consecutive data points in a gap in the profile is no
        greater than 16, this gap will be filled.
        """
        show_error(self.user_set.set_int_value(GapFilling.name, 16))
        """
        Set the "Filter" parameter to "Mean". The "Mean Filter Window Size" parameter needs to be set
        as well. This parameter controls the window size of mean filter. If the "Filter" parameter is
        set to "Median", the "Median Filter Window Size" parameter needs to be set. This parameter
        controls the window size of median filter.
        """
        show_error(self.user_set.set_enum_value(
            Filter.name, Filter.Value_Mean))
        # Set the "Mean Filter Window Size" parameter to 2
        show_error(self.user_set.set_enum_value(
            MeanFilterWindowSize.name, MeanFilterWindowSize.Value_WindowSize_2))

        error, self.data_width = self.user_set.get_int_value(
            DataPointsPerProfile.name)
        show_error(error)

        error, self.capture_line_count = self.user_set.get_int_value(
            ScanLineCount.name)
        show_error(error)

        error, data_acquisition_trigger_source = self.user_set.get_enum_value(
            DataAcquisitionTriggerSource.name)
        show_error(error)
        self.is_software_trigger = data_acquisition_trigger_source == DataAcquisitionTriggerSource.Value_Software

    def acquire_profile_data(self) -> bool:
        """
        Call start_acquisition() to enter the laser profiler into the acquisition ready status, and
        then call trigger_software() to start the data acquisition (triggered by software).
        """
        print("Start data acquisition.")
        status = self.profiler.start_acquisition()
        if not status.is_ok():
            show_error(status)
            return False

        if self.is_software_trigger:
            status = self.profiler.trigger_software()
            if (not status.is_ok()):
                show_error(status)
                return False

        self.profile_batch.clear()
        self.profile_batch.reserve(self.capture_line_count)

        while self.profile_batch.height() < self.capture_line_count:
            # Retrieve the profile data
            batch = ProfileBatch(self.data_width)
            status = self.profiler.retrieve_batch_data(batch)
            if status.is_ok():
                self.profile_batch.append(batch)
                sleep(0.2)
            else:
                show_error(status)
                return False

        print("Stop data acquisition.")
        status = self.profiler.stop_acquisition()
        if not status.is_ok():
            show_error(status)
        return status.is_ok()

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

        self.set_parameters()

        self.profile_batch = ProfileBatch(self.data_width)

        # Acquire profile data without using callback
        if not self.acquire_profile_data():
            return -1

        # # Acquire the profile data using the callback function
        # if not self.acquire_profile_data_using_callback():
            # return -1

        if self.profile_batch.check_flag(ProfileBatch.BatchFlag_Incomplete):
            print("Part of the batch's data is lost, the number of valid profiles is:",
                  self.profile_batch.valid_height())

        print("Save the depth map and intensity image")
        self.save_depth_and_intensity("depth.tiff", "intensity.png")
        save_point_cloud(profile_batch=self.profile_batch, user_set=self.user_set,
                         save_ply=True, save_csv=True, is_organized=True)

        # # Uncomment the following line to save a virtual device file using the ProfileBatch acquired.
        # self.profiler.save_virtual_device_file(self.profile_batch, "test.mraw")

        self.profiler.disconnect()
        print("Disconnected from the Mech-Eye Profiler successfully")
        return 0


if __name__ == '__main__':
    a = TriggerWithSoftwareAndEncoder()
    a.main()
