from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *
import cv2
from time import sleep
from multiprocessing import Lock

mutex = Lock()


class CustomAcquisitionCallback(AcquisitionCallbackBase):
    def __init__(self, width):
        AcquisitionCallbackBase.__init__(self)
        self.total_batch = ProfileBatch(width)

    def run(self, batch):
        mutex.acquire()
        print("callback called")
        self.total_batch.append(batch)
        mutex.release()


class AcquireProfileDataUsingCallback(object):
    def __init__(self):
        self.profiler = Profiler()

    def set_parameters(self):
        current_user_set = self.profiler.current_user_set()

        # Set the exposure mode to timed
        show_error(current_user_set.set_enum_value(
            ExposureMode.name, ExposureMode.Value_Timed))

        # Set the exposure time to 100 μs
        show_error(current_user_set.set_int_value(ExposureTime.name, 100))

        """
        The other option for the exposure mode is HDR, in which three exposure times and the
        y-coordinates of two knee points must be set.
        The code for setting the relevant parameters for the HDR exposure mode is given in the
        following notes.
        Set the the exposure sequence for the HDR exposure mode. The exposure sequence contains three
        exposure times, 100, 10, and 4. The total exposure time is the sum of the three exposure
        times, which is 114 in this case.
        """

        # show_error(current_user_set.set_enum_value(ExposureMode.name, ExposureMode.Value_HDR))
        # Set the exposure time to 100 μs
        # show_error(current_user_set.set_int_value(ExposureTime.name, 100))
        # show_error(current_user_set.set_float_value(HdrExposureTimeProportion1.name, 40))
        # show_error(current_user_set.set_float_value(HdrExposureTimeProportion2.name, 80))
        # Set HDR first threshold to 10
        # show_error(current_user_set.set_float_value(HdrFirstThreshold.name, 10))
        # Set HDR second threshold to 60
        # show_error(current_user_set.set_float_value(HdrSecondThreshold.name, 60))

        # Set the data acquisition trigger source to be Software
        show_error(current_user_set.set_enum_value(
            DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_Software))
        # Set the data acquisition trigger source to be External
        # show_error(current_user_set.set_enum_value(DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_External))

        # Set the trigger source to FixedRate
        show_error(current_user_set.set_enum_value(
            LineScanTriggerSource.name, LineScanTriggerSource.Value_FixedRate))
        # Set the trigger source to Encoder
        # show_error(current_user_set.set_enum_value(LineScanTriggerSource.name, LineScanTriggerSource.Value_Encoder))
        # Set the encoder trigger direction to both
        # show_error(current_user_set.set_enum_value(EncoderTriggerDirection.name, EncoderTriggerDirection.Value_Both))
        # Set the encoder signal counting mode to be Multiple_1
        # show_error(current_user_set.set_enum_value(EncoderTriggerSignalCountingMode.name, EncoderTriggerSignalCountingMode.Value_Multiple_1))
        # Set the encoder trigger interval to 10
        # show_error(current_user_set.set_int_value(EncoderTriggerInterval.name, 10))

        # Set the maximum number of lines to be scanned to 1600
        show_error(current_user_set.set_int_value(ScanLineCount.name, 1600))

        # Set the laser power level to 100
        show_error(current_user_set.set_int_value(LaserPower.name, 100))

        profiler_info = ProfilerInfo()
        if self.profiler.get_profiler_info(profiler_info).is_ok():
            # Set the analog gain to 1.3
            if profiler_info.model == "Mech-Eye LNX 8030":
                show_error(current_user_set.set_enum_value(
                    AnalogGainFor8030.name, AnalogGainFor8030.Value_Gain_1_3))
            else:
                show_error(current_user_set.set_enum_value(
                    AnalogGain.name, AnalogGain.Value_Gain_1_3))

        # Set the digital gain to 0
        show_error(current_user_set.set_int_value(DigitalGain.name, 0))
        # Set the grayscale value threshold to 50
        show_error(current_user_set.set_int_value(MinGrayscaleValue.name, 50))
        # Set the minimum laser line width to 2
        show_error(current_user_set.set_int_value(MinLaserLineWidth.name, 2))
        # Set the maximum laser line width to 20
        show_error(current_user_set.set_int_value(MaxLaserLineWidth.name, 20))
        # Set the minimum laser line intensity to 10
        show_error(current_user_set.set_int_value(MinSpotIntensity.name, 10))
        # Set the maximum laser line intensity to 205
        show_error(current_user_set.set_int_value(MaxSpotIntensity.name, 204))
        # Set the maximum number of invalid points to be interpolated to 16. If the number of continuous invalid points is less than or equal to 16, these points will be filled
        show_error(current_user_set.set_int_value(GapFilling.name, 16))
        # Set the profile extraction strategy to Strongest
        show_error(current_user_set.set_enum_value(
            SpotSelection.name, SpotSelection.Value_Strongest))
        """
        Set the filter type to Mean. When the filter type is set to Mean, setLnxMeanFilterWindow can be called to set the window size for
        mean filtering. When the filter type is set to Median,
        """
        show_error(current_user_set.set_enum_value(
            Filter.name, Filter.Value_Mean))
        # Set the window size for mean filtering to WindowSize_2
        show_error(current_user_set.set_enum_value(
            MeanFilterWindowSize.name, MeanFilterWindowSize.Value_WindowSize_2))

        # Get the line width in the x direction
        error, self.data_width = current_user_set.get_int_value(
            DataPointsPerProfile.name)
        show_error(error)

        error, self.capture_line_count = current_user_set.get_int_value(
            ScanLineCount.name)
        show_error(error)

    def capture(self):
        print("Start scanning")
        self.callback = CustomAcquisitionCallback(self.data_width).__disown__()
        status = self.profiler.register_acquisition_callback(
            self.callback)

        if not status.is_ok():
            show_error(status)
            return

        status = self.profiler.start_acquisition()
        if not status.is_ok():
            show_error(status)
            return

        status = self.profiler.trigger_software()
        if not status.is_ok():
            show_error(status)
            return

        while True:
            mutex.acquire()
            if self.callback.total_batch.is_empty():
                mutex.release()
                print("empty")
                sleep(0.5)
            else:
                break

    def save(self, depth_file_name, intensity_file_name):
        cv2.imwrite(depth_file_name,
                    self.callback.total_batch.get_depth_map().data())
        cv2.imwrite(intensity_file_name,
                    self.callback.total_batch.get_intensity_image().data())

    def main(self):
        if find_and_connect(self.profiler) and confirm_capture():
            self.set_parameters()
            self.capture()
            print("capture finished")
            self.save("depth.tiff", "intensity.tiff")
            self.profiler.disconnect()
            print("Disconnected form the Mech-Eye Profiler successfully")


if __name__ == '__main__':
    a = AcquireProfileDataUsingCallback()
    a.main()
