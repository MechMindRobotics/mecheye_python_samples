from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *
import cv2
from time import sleep


class AcquireProfileData(object):
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

        # Set the analog gain to level 2
        show_error(current_user_set.set_enum_value(
            AnalogGain.name, AnalogGain.Value_Gain_2))

        # Set the digital gain to 0
        show_error(current_user_set.set_int_value(DigitalGain.name, 0))
        # Set the grayscale value threshold to 50
        show_error(current_user_set.set_int_value(MinGrayscaleValue.name, 50))
        # Set the minimum laser line width to 2
        show_error(current_user_set.set_int_value(MinLaserLineWidth.name, 2))
        # Set the maximum laser line width to 20
        show_error(current_user_set.set_int_value(MaxLaserLineWidth.name, 20))
        # This parameter is only effective for firmware 2.2.1 and below. For firmware 2.3.0 and above,
        # adjustment of this parameter does not take effect.
        # Set the minimum laser line intensity to 10
        show_error(current_user_set.set_int_value(MinSpotIntensity.name, 10))
        # This parameter is only effective for firmware 2.2.1 and below. For firmware 2.3.0 and above,
        # adjustment of this parameter does not take effect.
        # Set the maximum laser line intensity to 205
        show_error(current_user_set.set_int_value(MaxSpotIntensity.name, 205))
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

        self.size = self.capture_line_count * self.data_width

    def capture(self):
        print("Start scanning")
        self.total_batch = ProfileBatch(self.data_width)
        if self.profiler.start_acquisition().is_ok() and self.profiler.trigger_software().is_ok():
            self.total_batch.reserve(self.capture_line_count)
            while self.total_batch.height() < self.capture_line_count:
                batch = ProfileBatch(self.data_width)
                status = self.profiler.retrieve_batch_data(batch)
                if status.is_ok():
                    self.total_batch.append(batch)
                    sleep(0.2)
                else:
                    show_error(status)
                    break

    def save(self, depth_file_name, intensity_file_name):
        cv2.imwrite(depth_file_name, self.total_batch.get_depth_map().data())
        cv2.imwrite(intensity_file_name,
                    self.total_batch.get_intensity_image().data())

    def main(self):
        if find_and_connect(self.profiler) and confirm_capture():
            self.set_parameters()
            self.capture()
            self.save("depth.tiff", "intensity.tiff")
            self.profiler.disconnect()
            print("Disconnected form the Mech-Eye Profiler successfully")


if __name__ == '__main__':
    a = AcquireProfileData()
    a.main()
