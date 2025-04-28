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

        # Set the exposure times for acquiring depth information.
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
        # mode: DEEP, DEEP-GL, LSR S/L/XL, LSR S-GL/L-GL/XL-GL, PRO XS/S/M, PRX XS-GL/S-GL/M-GL, NANO, NANO-GL, NANO ULTRA, NANO ULTRA-GL. Uncomment the following lines to set
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
        # print("\n2D image gain: ", scan2DGain)value(Scanning2DGain.name,2.0))
        # show_error(error)et_float_value(Scanning2DGain.name)
        # error, scan2DGain = current_user_set.get_float_value(Scanning2DGain.name)
        # show_error(current_user_set.set_float_value(Scanning2DGain.name,2.6))

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
