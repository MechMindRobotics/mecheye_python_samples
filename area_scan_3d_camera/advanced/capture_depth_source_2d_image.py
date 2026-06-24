# With this sample, you can obtain and save the depth-source 2D image.

import cv2

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect


class CaptureDepthSource2DImage(object):
    def __init__(self):
        self.camera = Camera()

    def capture_depth_source_2d_image(self):
        frame_2d = Frame2D()
        error = self.camera.capture_depth_source_2d(frame_2d)
        if not error.is_ok():
            show_error(error)
            return

        if frame_2d.color_type() == ColorTypeOf2DCamera_Monochrome:
            image_2d = frame_2d.get_gray_scale_image()
            file_name = "DepthSourceGrayScale2DImage.png"
            print("Capture and save the depth-source gray scale 2D image: {}".format(file_name))
        elif frame_2d.color_type() == ColorTypeOf2DCamera_Color:
            image_2d = frame_2d.get_color_image()
            file_name = "DepthSourceColor2DImage.png"
            print("Capture and save the depth-source color 2D image: {}".format(file_name))
        else:
            print("The acquired depth-source 2D image has an unsupported color type.")
            return

        cv2.imwrite(file_name, image_2d.data())

    def main(self):
        if find_and_connect(self.camera):
            self.capture_depth_source_2d_image()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = CaptureDepthSource2DImage()
    a.main()