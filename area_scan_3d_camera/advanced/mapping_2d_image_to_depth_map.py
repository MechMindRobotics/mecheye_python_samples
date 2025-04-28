# With this sample, you can generate untextured and textured point clouds from a masked 2D image and a depth map.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, confirm_capture_3d


class Mapping2DImageToDepthMap(object):
    def __init__(self):
        self.camera = Camera()

    def contains(self, row, col, roi):
        return roi[1] <= row <= roi[1] + roi[3] and roi[0] <= col <= roi[0] + roi[2]

    def generate_texture_mask(self, color: Color2DImage, roi1: ROI, roi2: ROI):
        mask = GrayScale2DImage()
        height = color.height()
        width = color.width()
        mask.resize(width, height)

        for i in range(height):
            for j in range(width):
                if not self.contains(i, j, roi1) and not self.contains(i, j, roi2):
                    mask.at(i, j).gray = 255
        return mask

    def mapping_2d_image_to_depth_map(self):
        # capture frame
        frame_all_2d_3d = Frame2DAnd3D()
        show_error(self.camera.capture_2d_and_3d(frame_all_2d_3d))
        color = frame_all_2d_3d.frame_2d().get_color_image()
        depth = frame_all_2d_3d.frame_3d().get_depth_map()
        intrinsics = CameraIntrinsics()
        show_error(self.camera.get_camera_intrinsics(intrinsics))

        roi1 = (color.width() / 5, color.height() / 5,
                color.width() / 2, color.height() / 2)
        roi2 = (color.width() * 2 / 5, color.height() * 2 /
                5, color.width() / 2, color.height() / 2)
        #
        #  Generate a mask of the following shape:
        #   ______________________________
        #  |                              |
        #  |                              |
        #  |   *****************          |
        #  |   *****************          |
        #  |   ************************   |
        #  |   ************************   |
        #  |          *****************   |
        #  |          *****************   |
        #  |                              |
        #  |______________________________|
        #
        mask = self.generate_texture_mask(color, roi1, roi2)

        points_xyz = UntexturedPointCloud()
        show_error(get_point_cloud_after_mapping(
            depth, mask, intrinsics, points_xyz))
        point_cloud_file = "UntexturedPointCloud.ply"
        success_message = "Save the untextured point cloud to file:" + point_cloud_file
        show_error(
            Frame3D.save_point_cloud(points_xyz, FileFormat_PLY, point_cloud_file), success_message)

        # generate colored point cloud
        points_xyz_bgr = TexturedPointCloud()
        show_error(
            get_point_cloud_after_mapping(depth, mask, color, intrinsics, points_xyz_bgr))
        point_cloud_file = "TexturedPointCloud.ply"
        success_message = "Save the textured point cloud to file:" + point_cloud_file
        show_error(
            Frame2DAnd3D.save_point_cloud(points_xyz_bgr, FileFormat_PLY,
                                          point_cloud_file), success_message)

    def main(self):
        if find_and_connect(self.camera):
            if not confirm_capture_3d():
                return
            self.mapping_2d_image_to_depth_map()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = Mapping2DImageToDepthMap()
    a.main()
