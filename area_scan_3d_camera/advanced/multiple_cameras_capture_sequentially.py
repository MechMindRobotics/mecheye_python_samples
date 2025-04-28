# With this sample, you can obtain and save 2D images, depth maps and point clouds
# sequentially from multiple cameras.

import cv2

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *


class MultipleCamerasCaptureSequentially(object):

    def __init__(self):
        self.cameras = find_and_connect_multi_camera()

    def connect_device_and_capture(self):
        # Start capturing images.
        if (len(self.cameras) == 0):
            print("No cameras connected.")
            return

        if not confirm_capture_3d():
            return

        for camera in self.cameras:
            camera_info = CameraInfo()
            show_error(camera.get_camera_info(camera_info))
            print_camera_info(camera_info)

            print("Camera {} start capturing.".format(camera_info.ip_address))
            frame_all_2d_3d = Frame2DAnd3D()
            show_error(camera.capture_2d_and_3d(frame_all_2d_3d))

            # Save the obtained data with the set filenames.
            color_file = "2DImage_" + camera_info.serial_number + ".png"
            depth_file = "DepthMap_" + camera_info.serial_number + ".png"
            point_cloud_file = "TexturedPointCloud_" + camera_info.serial_number + "ply"

            color_image = frame_all_2d_3d.frame_2d().get_color_image()
            cv2.imwrite(color_file, color_image.data())
            print("Capture and save the 2D image:", color_file)

            depth_image = frame_all_2d_3d.frame_3d().get_depth_map()
            cv2.imwrite(depth_file, depth_image.data())
            print("Capture and save the depth map:", depth_file)

            success_message = "Capture and save the textured point cloud:" + point_cloud_file
            show_error(
                frame_all_2d_3d.save_textured_point_cloud(FileFormat_PLY, point_cloud_file), success_message)

            camera.disconnect()
            print("Disconnected from the camera successfully.")

    def main(self):
        self.connect_device_and_capture()


if __name__ == '__main__':
    a = MultipleCamerasCaptureSequentially()
    a.main()
