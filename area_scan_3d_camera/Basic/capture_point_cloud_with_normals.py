# With this sample, you can calculate normals and save the point cloud with normals. The normals can be calculated on the camera or the computer.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, confirm_capture_3d


class CapturePointCloudWithNormals(object):
    def __init__(self):
        self.camera = Camera()
        self.frame_3d = Frame3D()

    # Calculate the normals of the points on the camera and save the point cloud with normals to file
    def capture_point_cloud_with_normals_calculated_on_camera(self):
        point_cloud_file = "PointCloud_1.ply"
        if self.camera.capture_3d_with_normal(self.frame_3d).is_ok():
            show_error(
                self.frame_3d.save_untextured_point_cloud_with_normals(FileFormat_PLY, point_cloud_file))
            return True
        else:
            print("Failed to capture the point cloud.")
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")
            return False

    # Calculate the normals of the points on the computer and save the point cloud with normals to file
    def capture_point_cloud_with_normals_calculated_locally(self):
        point_cloud_file = "PointCloud_2.ply"
        if self.camera.capture_3d(self.frame_3d).is_ok():
            show_error(
                self.frame_3d.save_untextured_point_cloud_with_normals(FileFormat_PLY, point_cloud_file))
            return True
        else:
            print("Failed to capture the point cloud.")
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")
            return False

    def main(self):
        if find_and_connect(self.camera):
            if not confirm_capture_3d():
                return
            if not self.capture_point_cloud_with_normals_calculated_on_camera():
                return
            if not self.capture_point_cloud_with_normals_calculated_locally():
                return
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = CapturePointCloudWithNormals()
    a.main()
