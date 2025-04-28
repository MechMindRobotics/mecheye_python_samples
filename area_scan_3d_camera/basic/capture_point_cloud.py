# With this sample, you can obtain and save the untextured and textured point clouds.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, confirm_capture_3d


class CapturePointCloud(object):
    def __init__(self):
        self.camera = Camera()
        self.frame_all_2d_3d = Frame2DAnd3D()

    def capture_point_cloud(self):
        point_cloud_file = "PointCloud.ply"
        success_message = "Capture and save the untextured point cloud: {}.".format(point_cloud_file)
        show_error(
            self.frame_all_2d_3d.frame_3d().save_untextured_point_cloud(FileFormat_PLY, point_cloud_file), success_message)

    def capture_textured_point_cloud(self):
        textured_point_cloud_file = "TexturedPointCloud.ply"
        success_message = "Capture and save the textured point cloud: {}".format(textured_point_cloud_file)
        show_error(self.frame_all_2d_3d.save_textured_point_cloud(FileFormat_PLY, textured_point_cloud_file), success_message)

    def main(self):
        if find_and_connect(self.camera):
            if not confirm_capture_3d():
                return
            show_error(self.camera.capture_2d_and_3d(self.frame_all_2d_3d))
            self.capture_point_cloud()
            self.capture_textured_point_cloud()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = CapturePointCloud()
    a.main()
