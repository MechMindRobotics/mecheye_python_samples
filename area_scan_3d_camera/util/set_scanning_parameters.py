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
        error, exposure_mode_2d = current_user_set.get_enum_value_string(
            Scanning2DExposureMode.name)
        show_error(error)
        error, exposure_time_2d = current_user_set.get_float_value(
            Scanning2DExposureTime.name)
        show_error(error)
        print("\n2D scanning exposure mode enum: {}, exposure time: {}".
              format(exposure_mode_2d, exposure_time_2d))

        # Save all the parameter settings to the currently selected user set.
        show_error(current_user_set.save_all_parameters_to_device())
        print("\nSave the current parameter settings to the selected user set.")

    def main(self):
        if find_and_connect(self.camera):
            self.set_scanning_parameters()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = SetScanningParameters()
    a.main()
