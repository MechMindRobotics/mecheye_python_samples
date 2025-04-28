# With this sample, you can set the "Point Cloud Processing" parameters.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, print_camera_info


class SetPointCloudProcessingParameters(object):
    def __init__(self):
        self.camera = Camera()

    def set_point_cloud_processing_parameters(self):

        # Obtain the basic information of the connected camera.
        cameraInfo = CameraInfo()
        show_error(self.camera.get_camera_info(cameraInfo))
        print_camera_info(cameraInfo)

        current_user_set = self.camera.current_user_set()

        # Set the "Point Cloud Processing" parameters, and then obtain the parameter values to check if the setting was successful.
        error = current_user_set.set_enum_value(PointCloudSurfaceSmoothing.name,
                                                PointCloudSurfaceSmoothing.Value_Normal)
        show_error(error)
        error = current_user_set.set_enum_value(PointCloudNoiseRemoval.name,
                                                PointCloudNoiseRemoval.Value_Normal)
        show_error(error)
        error = current_user_set.set_enum_value(PointCloudOutlierRemoval.name,
                                                PointCloudOutlierRemoval.Value_Normal)
        show_error(error)
        error = current_user_set.set_enum_value(PointCloudEdgePreservation.name,
                                                PointCloudEdgePreservation.Value_Normal)
        show_error(error)

        error, surface_smoothing = current_user_set.get_enum_value_string(
            PointCloudSurfaceSmoothing.name)
        show_error(error)
        error, noise_removal = current_user_set.get_enum_value_string(
            PointCloudNoiseRemoval.name)
        show_error(error)
        error, outlier_removal = current_user_set.get_enum_value_string(
            PointCloudOutlierRemoval.name)
        show_error(error)
        error, edge_preservation = current_user_set.get_enum_value_string(
            PointCloudEdgePreservation.name)
        show_error(error)

        print("Point Cloud Surface Smoothing:", surface_smoothing,
              "(0: Off, 1: Weak, 2: Normal, 3: Strong)")
        print("Point Cloud Noise Removal:", noise_removal,
              "(0: Off, 1: Weak, 2: Normal, 3: Strong)")
        print("Point Cloud Outlier Removal:", outlier_removal,
              "(0: Off, 1: Weak, 2: Normal, 3: Strong)")
        print("Point Cloud Edge Preservation:", edge_preservation,
              "(0: Sharp, 1: Normal, 2: Smooth)")

        # Save all the parameter settings to the currently selected user set.

        success_message = "\nSave the current parameter settings to the selected user set."
        show_error(current_user_set.save_all_parameters_to_device(), success_message)

    def main(self):
        if find_and_connect(self.camera):
            self.set_point_cloud_processing_parameters()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = SetPointCloudProcessingParameters()
    a.main()
