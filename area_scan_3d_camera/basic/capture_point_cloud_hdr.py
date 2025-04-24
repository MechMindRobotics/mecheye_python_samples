# With this sample, you can set multiple exposure times, and then obtain and save the point cloud.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, confirm_capture_3d


class CapturePointCloudHDR(object):
    def __init__(self):
        self.camera = Camera()
        self.frame_2d_and_3d = Frame2DAnd3D()

    def capture_point_cloud(self):
        point_cloud_file = "PointCloud.ply"
        success_message = "Capture and save the untextured point cloud to {}.".format(point_cloud_file)
        show_error(
            self.frame_2d_and_3d.frame_3d().save_untextured_point_cloud(FileFormat_PLY, point_cloud_file), success_message)

    def capture_textured_point_cloud(self):
        textured_point_cloud_file = "TexturedPointCloud.ply"
        success_message = "Capture and save the textured point cloud to {}".format(textured_point_cloud_file)
        show_error(self.frame_2d_and_3d.save_textured_point_cloud(FileFormat_PLY,
                                                                  textured_point_cloud_file),success_message)
        
    def capture_point_cloud_hdr(self):
        # Set 3D Exposure Sequence.
        current_user_set = self.camera.current_user_set()
        error = current_user_set.set_float_array_value(
            Scanning3DExposureSequence.name, [5, 10])
        show_error(error)
        self.capture_point_cloud()
        self.capture_textured_point_cloud()

    def main(self):
        if find_and_connect(self.camera):
            if not confirm_capture_3d():
                return
            show_error(self.camera.capture_2d_and_3d(self.frame_2d_and_3d))
            self.capture_point_cloud_hdr()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = CapturePointCloudHDR()
    a.main()
