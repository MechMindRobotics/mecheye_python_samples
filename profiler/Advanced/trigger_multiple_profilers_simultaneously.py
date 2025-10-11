# With this sample, you can obtain and save 2D images, depth maps and point clouds
# simultaneously from multiple profilers.

import cv2
import multiprocessing
from time import sleep

from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *


def set_timed_exposure(user_set: UserSet, exposure_time: int):
    # Set the exposure mode to timed
    show_error(user_set.set_enum_value(
        ExposureMode.name, ExposureMode.Value_Timed))

    # Set the exposure time to {exposure_time} μs
    show_error(user_set.set_int_value(
        ExposureTime.name, exposure_time))


def set_hdr_exposure(user_set: UserSet, exposure_time: int, proportion1: float, proportion2: float, first_threshold: float, second_threshold: float):
    # Set the "Exposure Mode" parameter to "HDR"
    show_error(user_set.set_enum_value(
        ExposureMode.name, ExposureMode.Value_HDR))

    # Set the total exposure time to {exposure_time} μs
    show_error(user_set.set_int_value(
        ExposureTime.name, exposure_time))

    # Set the proportion of the first exposure phase to {proportion1}%
    show_error(user_set.set_float_value(
        HdrExposureTimeProportion1.name, proportion1))

    # Set the proportion of the first + second exposure phases to {proportion2}% (that is, the
    # second exposure phase occupies {proportion2 - proportion1}%, and the third exposure phase
    # occupies {100 - proportion2}% of the total exposure time)
    show_error(user_set.set_float_value(
        HdrExposureTimeProportion2.name, proportion2))

    # Set the first threshold to {first_threshold}. This limits the maximum grayscale value to
    # {first_threshold} after the first exposure phase is completed.
    show_error(user_set.set_float_value(
        HdrFirstThreshold.name, first_threshold))

    # Set the second threshold to {second_threshold}. This limits the maximum grayscale value to
    # {second_threshold} after the second exposure phase is completed.
    show_error(user_set.set_float_value(
        HdrSecondThreshold.name, second_threshold))


def set_encoder_trigger(user_set: UserSet, trigger_direction: int, trigger_signal_counting_mode: int, trigger_interval: int):
    # Set the trigger source to Encoder
    show_error(user_set.set_enum_value(
        LineScanTriggerSource.name, LineScanTriggerSource.Value_Encoder))
    # Set the encoder trigger direction to {trigger_direction}
    show_error(user_set.set_enum_value(
        EncoderTriggerDirection.name, trigger_direction))
    # Set the encoder signal counting mode to be {trigger_signal_counting_mode}
    show_error(user_set.set_enum_value(
        EncoderTriggerSignalCountingMode.name, trigger_signal_counting_mode))
    # Set the encoder trigger interval to {trigger_interval}
    show_error(user_set.set_int_value(
        EncoderTriggerInterval.name, trigger_interval))


def set_parameters(profiler: Profiler):
    user_set = profiler.current_user_set()

    # Set the exposure mode to timed
    # Set the exposure time to 100 μs
    set_timed_exposure(user_set, 100)

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
    # set_hdr_exposure(user_set, 100, 40, 80, 10, 60)

    # Set the "Data Acquisition Trigger Source" parameter to "Software"
    show_error(user_set.set_enum_value(
        DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_Software))

    # # Set the "Data Acquisition Trigger Source" parameter to "External"
    # show_error(user_set.set_enum_value(
    # DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_External))

    # Set the "Line Scan Trigger Source" parameter to "Fixed rate"
    show_error(user_set.set_enum_value(
        LineScanTriggerSource.name, LineScanTriggerSource.Value_FixedRate))
    # Set the " Software Trigger Rate" to 1000 Hz
    show_error(user_set.set_float_value(
        SoftwareTriggerRate.name, 1000))

    # # Set the "Line Scan Trigger Source" parameter to "Encoder"
    # # Set the (encoder) "Trigger Direction" parameter to "Both"
    # # Set the (encoder) "Trigger Signal Counting Mode" parameter to "1×"
    # # Set the (encoder) "Trigger Interval" parameter to 10
    # set_encoder_trigger(user_set, EncoderTriggerDirection.Value_Both,
    #  EncoderTriggerSignalCountingMode.Value_Multiple_1, 10)

    # Set the "Scan Line Count" parameter (the number of lines to be scanned) to 1600
    show_error(user_set.set_int_value(ScanLineCount.name, 1600))

    # Set the "Laser Power" parameter to 100
    show_error(user_set.set_int_value(LaserPower.name, 100))
    # Set the "Analog Gain" parameter to "Gain_2"
    show_error(user_set.set_enum_value(
        AnalogGain.name, AnalogGain.Value_Gain_2))
    # Set the "Digital Gain" parameter to 0
    show_error(user_set.set_int_value(DigitalGain.name, 0))

    # Set the "Minimum Grayscale Value" parameter to 50
    show_error(user_set.set_int_value(MinGrayscaleValue.name, 50))
    # Set the "Minimum Laser Line Width" parameter to 2
    show_error(user_set.set_int_value(MinLaserLineWidth.name, 2))
    # Set the "Maximum Laser Line Width" parameter to 20
    show_error(user_set.set_int_value(MaxLaserLineWidth.name, 20))
    # Set the "Spot Selection" parameter to "Strongest"
    show_error(user_set.set_enum_value(
        SpotSelection.name, SpotSelection.Value_Strongest))

    # This parameter is only effective for firmware 2.2.1 and below. For firmware 2.3.0 and above,
    # adjustment of this parameter does not take effect.
    # Set the minimum laser line intensity to 10
    show_error(user_set.set_int_value(MinSpotIntensity.name, 51))
    # This parameter is only effective for firmware 2.2.1 and below. For firmware 2.3.0 and above,
    # adjustment of this parameter does not take effect.
    # Set the maximum laser line intensity to 205
    show_error(user_set.set_int_value(MaxSpotIntensity.name, 205))

    """
        Set the "Gap Filling" parameter to 16, which controls the size of the gaps that can be filled
        in the profile. When the number of consecutive data points in a gap in the profile is no
        greater than 16, this gap will be filled.
        """
    show_error(user_set.set_int_value(GapFilling.name, 16))
    """
        Set the "Filter" parameter to "Mean". The "Mean Filter Window Size" parameter needs to be set
        as well. This parameter controls the window size of mean filter. If the "Filter" parameter is
        set to "Median", the "Median Filter Window Size" parameter needs to be set. This parameter
        controls the window size of median filter.
        """
    show_error(user_set.set_enum_value(
        Filter.name, Filter.Value_Mean))
    # Set the "Mean Filter Window Size" parameter to 2
    show_error(user_set.set_enum_value(
        MeanFilterWindowSize.name, MeanFilterWindowSize.Value_WindowSize_2))

    error, data_width = user_set.get_int_value(
        DataPointsPerProfile.name)
    show_error(error)

    error, capture_line_count = user_set.get_int_value(
        ScanLineCount.name)
    show_error(error)

    error, data_acquisition_trigger_source = user_set.get_enum_value(
        DataAcquisitionTriggerSource.name)
    show_error(error)
    is_software_trigger = data_acquisition_trigger_source == DataAcquisitionTriggerSource.Value_Software
    return data_width, capture_line_count, is_software_trigger


def acquire_profile_data(profiler: Profiler, profile_batch: ProfileBatch, is_software_trigger: bool, capture_line_count: int, data_width: int) -> bool:
    """
    Call start_acquisition() to enter the laser profiler into the acquisition ready status, and
    then call trigger_software() to start the data acquisition (triggered by software).
    """
    print("Start data acquisition.")
    status = profiler.start_acquisition()
    if not status.is_ok():
        show_error(status)
        return False

    if is_software_trigger:
        status = profiler.trigger_software()
        if (not status.is_ok()):
            show_error(status)
            return False

    profile_batch.clear()
    profile_batch.reserve(capture_line_count)

    while profile_batch.height() < capture_line_count:
        # Retrieve the profile data
        batch = ProfileBatch(data_width)
        status = profiler.retrieve_batch_data(batch)
        if status.is_ok():
            profile_batch.append(batch)
            sleep(0.2)
        else:
            show_error(status)
            return False

    print("Stop data acquisition.")
    status = profiler.stop_acquisition()
    if not status.is_ok():
        show_error(status)
    return status.is_ok()


def save_depth_and_intensity(profile_batch: ProfileBatch, depth_file_name: str, intensity_file_name: str):
    cv2.imwrite(depth_file_name,
                profile_batch.get_depth_map().data())
    print(f"Saved the depth map to {depth_file_name}")
    cv2.imwrite(intensity_file_name,
                profile_batch.get_intensity_image().data())
    print(f"Saved the intensity image to {intensity_file_name}")


def capture_task(ip_address: str, sensor_sn: str):
    profiler = Profiler()
    if not profiler.connect(ip_address).is_ok():
        return

    # Set the parameters of the profiler and get necessary parameters
    data_width, capture_line_count, is_software_trigger = set_parameters(
        profiler)

    # Create a ProfileBatch object to store the profile data
    profile_batch = ProfileBatch(data_width)
    if not acquire_profile_data(profiler, profile_batch, is_software_trigger, capture_line_count, data_width):
        return

    # Check if the batch's data is complete
    if profile_batch.check_flag(ProfileBatch.BatchFlag_Incomplete):
        print(f"Part of the batch's data of profiler {sensor_sn} is lost, the number of valid profiles is:",
              profile_batch.valid_height())

    # Save the depth map and intensity image
    save_depth_and_intensity(
        profile_batch, f"depth_{sensor_sn}.png", f"intensity_{sensor_sn}.png")

    profiler.disconnect()
    print("Disconnected from the Mech-Eye Profiler successfully")


class TriggerMultipleProfilersSimultaneously(object):
    def __init__(self):
        self.profilers = find_and_connect_multi_profiler()

    def connect_device_and_capture(self):
        if not self.profilers:
            print("No profilers connected.")
            return

        if not confirm_capture():
            return

        # Create a process for each profiler
        processes = []
        for profiler in self.profilers:
            profiler_info = ProfilerInfo()
            show_error(profiler.get_profiler_info(profiler_info))
            process = multiprocessing.Process(
                target=capture_task, args=(profiler_info.ip_address, profiler_info.sensor_sn))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

    def main(self):
        self.connect_device_and_capture()


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    a = TriggerMultipleProfilersSimultaneously()
    a.main()
