# With this sample, you can set the parameters in the "3D Parameters", "2D Parameters", and "ROI" categories.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, print_camera_info


class SetScanningParameters(object):
    def __init__(self):
        self.camera = Camera()

    def set_scanning_parameters(self):

        # Obtain the basic information of the connected camera.
        cameraInfo = CameraInfo()
        show_error(self.camera.get_camera_info(cameraInfo))
        print_camera_info(cameraInfo)

        # Obtain the name of the currently selected user set.
        current_user_set = self.camera.current_user_set()
        error, user_set_name = current_user_set.get_name()
        show_error(error)
        print("\ncurrent_user_set: " + user_set_name)
        error, available_params = current_user_set.get_available_parameter_names()
        show_error(error)

        # Set the exposure times for acquiring depth information.
        if Scanning3DExposureCount.name in available_params:
            error = current_user_set.set_int_value(Scanning3DExposureCount.name, 1)
            show_error(error)
            error, exposure_count = current_user_set.get_int_value(
                Scanning3DExposureCount.name)
            show_error(error)
            print("\n3D scanning exposure count: {}".format(exposure_count))
        error = current_user_set.set_float_array_value(
            Scanning3DExposureSequence.name, [5])
        # error = current_user_set.set_float_array_value(
        #     Scanning3DExposureSequence.name, [5, 10])
        show_error(error)
        error, exposure_sequence = current_user_set.get_float_array_value(
            Scanning3DExposureSequence.name)
        show_error(error)
        print("\nThe 3D scanning exposure multiplier: {}".format(
            len(exposure_sequence)))
        for i in exposure_sequence:
            print("3D scanning exposure time: {}".format(i))

        # Some models provide exposure group parameters. Use "GroupExposureSelector" to select the
        # target group, and then set the group exposure time, gain, and power level.
        if (Scanning3DGroupExposureSelector.name in available_params and
                Scanning3DGroupExposureTime.name in available_params and
                Scanning3DGroupGain.name in available_params and
                Scanning3DGroupDlpPowerLevel.name in available_params):
            error = current_user_set.set_enum_value(
                Scanning3DGroupExposureSelector.name,
                Scanning3DGroupExposureSelector.Value_Exposure1)
            show_error(error)
            error = current_user_set.set_float_value(
                Scanning3DGroupExposureTime.name, 10)
            show_error(error)
            error = current_user_set.set_float_value(
                Scanning3DGroupGain.name, 2.0)
            show_error(error)
            error = current_user_set.set_int_value(
                Scanning3DGroupDlpPowerLevel.name, 80)
            show_error(error)

            error, group_exposure_time = current_user_set.get_float_value(
                Scanning3DGroupExposureTime.name)
            show_error(error)
            error, group_gain = current_user_set.get_float_value(
                Scanning3DGroupGain.name)
            show_error(error)
            error, group_dlp_power_level = current_user_set.get_int_value(
                Scanning3DGroupDlpPowerLevel.name)
            show_error(error)
            print("Group Exposure1: exposure time {}, gain {}, DLP power level {}.".format(
                group_exposure_time, group_gain, group_dlp_power_level))

            error = current_user_set.set_enum_value(
                Scanning3DGroupExposureSelector.name,
                Scanning3DGroupExposureSelector.Value_Exposure2)
            show_error(error)
            error = current_user_set.set_float_value(
                Scanning3DGroupExposureTime.name, 5)
            show_error(error)
            error = current_user_set.set_float_value(
                Scanning3DGroupGain.name, 0.0)
            show_error(error)
            error = current_user_set.set_int_value(
                Scanning3DGroupDlpPowerLevel.name, 60)
            show_error(error)

            error, group_exposure_time = current_user_set.get_float_value(
                Scanning3DGroupExposureTime.name)
            show_error(error)
            error, group_gain = current_user_set.get_float_value(
                Scanning3DGroupGain.name)
            show_error(error)
            error, group_dlp_power_level = current_user_set.get_int_value(
                Scanning3DGroupDlpPowerLevel.name)
            show_error(error)
            print("Group Exposure2: exposure time {}, gain {}, DLP power level {}.".format(
                group_exposure_time, group_gain, group_dlp_power_level))

        # Set the ROI for the depth map and point cloud, and then obtain the parameter values for checking.
        roi = ROI(0, 0, 500, 500)
        error = current_user_set.set_roi_value(Scanning3DROI.name, roi)
        show_error(error)
        error, roi = current_user_set.get_roi_value(Scanning3DROI.name)
        show_error(error)
        print("\n3D scanning ROI topLeftX: {}, topLeftY: {}, width: {}, height: {}".
              format(roi.upper_left_x, roi.upper_left_y, roi.width, roi.height))

        # Set the exposure mode and exposure time for capturing the 2D image, and then obtain the
        # parameter values to check if the setting was successful.
        exposure_mode_2d = Scanning2DExposureMode.Value_Timed
        error = current_user_set.set_enum_value(
            Scanning2DExposureMode.name, exposure_mode_2d)
        show_error(error)
        exposure_time_2d = 100
        error = current_user_set.set_float_value(
            Scanning2DExposureTime.name, exposure_time_2d)
        show_error(error)

        # The DEEP and LSR series also provide a "Scan2DPatternRoleExposureMode" parameter for
        # adjusting the exposure mode for acquiring the 2D images (depth source). Uncomment the
        # following lines to set this parameter to "Timed".
        depth_source_exposure_mode_2d = Scanning2DDepthSourceExposureMode.Value_Timed
        error = current_user_set.set_enum_value(
            Scanning2DDepthSourceExposureMode.name, depth_source_exposure_mode_2d)
        show_error(error)

        # You can also use the projector for supplemental light when acquiring the 2D image / 2D images
        # (depth source).
        # Models other than the DEEP and LSR series: Uncomment the following lines to set the exposure
        # mode to "Flash" for supplemental light.
        # exposure_mode_2d = Scanning2DExposureMode.Value_Flash
        # error = current_user_set.set_enum_value(
        #     Scanning2DExposureMode.name, exposure_mode_2d)
        # show_error(error)

        # DEEP and LSR series: Uncomment the following lines to set the exposure mode to "Flash" for
        # supplemental light.
        # depth_source_exposure_mode_2d = Scanning2DDepthSourceExposureMode.Value_Flash
        # error = current_user_set.set_enum_value(
        #     Scanning2DDepthSourceExposureMode.name, depth_source_exposure_mode_2d)
        # show_error(error)

        # The following models also provide a "FlashAcquisitionMode" when using the flash exposure
        # mode: DEEP, DEEP-GL, LSR S/L/XL, LSR S-GL/L-GL/XL-GL, PRO XS/S/M, PRO XS-GL/S-GL/M-GL, NANO, NANO-GL, NANO ULTRA, NANO ULTRA-GL. Uncomment the following lines to set
        # the "FlashAcquisitionMode" parameter to "Responsive".
        # flash_acquisition_mode_2d=Scanning2DFlashAcquisitionMode.Value_Responsive
        # error = current_user_set.set_enum_value(
        #     Scanning2DFlashAcquisitionMode.name, flash_acquisition_mode_2d)
        # show_error(error)

        # When using the responsive acquisition mode, you can adjust the exposure time for the flash
        # exposure mode. Uncomment the following lines to set the exposure time to 20 ms.
        # flash_exposure_time_2d = 20
        # error = current_user_set.set_float_value(
        #     Scanning2DFlashExposureTime.name, flash_exposure_time_2d)
        # show_error(error)

        # Uncomment the following lines to check the values of the "FlashAcquisitionMode" and "FlashExposureTime" parameters.
        # error, flash_acquisition_mode_2d = current_user_set.get_enum_value_string(
        #     Scanning2DFlashAcquisitionMode.name)
        # show_error(error)
        # error, flash_exposure_time_2d = current_user_set.get_float_value(
        #     Scanning2DFlashExposureTime.name)
        # show_error(error)
        # print("\n2D scanning flash acquisition mode: {}, flash exposure time: {}".
        #       format(flash_acquisition_mode_2d, flash_exposure_time_2d))

        # Uncomment the following line to set the camera gain when capturing 2D images.
        # For DEEP and LSR series cameras, the camera gain for capturing 2D images (texture) can be
        # adjusted by setting the "Scan2DGain" parameter.
        # For other camera series, the camera gain for capturing 2D images can be adjusted by
        # setting the "Scan2DGain" parameter when the exposure mode is set to fixed exposure, auto
        # exposure, HDR, or flash mode, and the flash acquisition mode is set to
        # responsive.
        # error = current_user_set.set_float_value(Scanning2DGain.name, 2.0)
        # show_error(error)
        # error, scan2DGain = current_user_set.get_float_value(Scanning2DGain.name)
        # show_error(error)
        # print("\n2D image gain: ", scan2DGain)


        # The following parameters are only available on some models. Uncomment to set and read values.
        # error = current_user_set.set_float_value(
        #     Scanning2DPatternRoleGain.name, 2.0)
        # show_error(error)
        # error, pattern_role_gain = current_user_set.get_float_value(
        #     Scanning2DPatternRoleGain.name)
        # show_error(error)
        # print("\n2D pattern role gain: {}".format(pattern_role_gain))
        #
        # error = current_user_set.set_float_value(
        #     Scanning2DFlashGain.name, 2.0)
        # show_error(error)
        # error, flash_gain = current_user_set.get_float_value(
        #     Scanning2DFlashGain.name)
        # show_error(error)
        # print("\n2D flash gain: {}".format(flash_gain))
        #
        # error = current_user_set.set_int_value(
        #     Scanning2DFlashPowerLevel.name, 80)
        # show_error(error)
        # error, flash_power_level = current_user_set.get_int_value(
        #     Scanning2DFlashPowerLevel.name)
        # show_error(error)
        # print("\n2D flash power level: {} %".format(flash_power_level))
        
        error, exposure_mode_2d = current_user_set.get_enum_value_string(
            Scanning2DExposureMode.name)
        show_error(error)
        error, exposure_time_2d = current_user_set.get_float_value(
            Scanning2DExposureTime.name)
        show_error(error)
        print("\n2D scanning exposure mode enum: {}, exposure time: {}".
              format(exposure_mode_2d, exposure_time_2d))

        # Save all the parameter settings to the currently selected user set.
        success_message = "\nSave the current parameter settings to the selected user set."
        show_error(current_user_set.save_all_parameters_to_device(), success_message)

    def main(self):
        if find_and_connect(self.camera):
            self.set_scanning_parameters()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = SetScanningParameters()
    a.main()
