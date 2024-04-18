# With this sample, you can connect to a camera and obtain the 2D image, depth map, and point cloud data.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *


class ConnectAndCaptureImages(object):
    def __init__(self):
        self.camera = Camera()

    def connect_and_capture(self):

        # Obtain the 2D image resolution and the depth map resolution of the camera.
        resolution = CameraResolutions()
        show_error(self.camera.get_camera_resolutions(resolution))
        print_camera_resolution(resolution)

        # Obtain the 2D image.
        frame2d = Frame2D()
        show_error(self.camera.capture_2d(frame2d))
        row, col = 222, 222
        color_map = frame2d.get_color_image()
        print("The size of the 2D image is {} (width) * {} (height).".format(
            color_map.width(), color_map.height()))
        rgb = color_map[row * color_map.width() + col]
        print("The RGB values of the pixel at ({},{}) is R:{},G:{},B{}\n".
              format(row, col, rgb.b, rgb.g, rgb.r))

        if not confirm_capture_3d():
            return

        # Obtain the depth map.
        frame3d = Frame3D()
        show_error(self.camera.capture_3d(frame3d))
        depth_map = frame3d.get_depth_map()
        print("The size of the depth map is {} (width) * {} (height).".format(
            depth_map.width(), depth_map.height()))
        depth = depth_map[row * depth_map.width() + col]
        print("The depth value of the pixel at ({},{}) is depth :{}mm\n".
              format(row, col, depth.z))

        # Obtain the point cloud.
        point_cloud = frame3d.get_untextured_point_cloud()
        print("The size of the point cloud is {} (width) * {} (height).".format(
            point_cloud.width(), point_cloud.height()))
        point_xyz = point_cloud[row * depth_map.width() + col]
        print("The coordinates of the point corresponding to the pixel at ({},{}) is X: {}mm , Y: {}mm, Z: {}mm\n".
              format(row, col, point_xyz.x, point_xyz.y, point_xyz.z))

    def main(self):
        # List all available cameras and connect to a camera by the displayed index.
        if find_and_connect(self.camera):
            self.connect_and_capture()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = ConnectAndCaptureImages()
    a.main()
