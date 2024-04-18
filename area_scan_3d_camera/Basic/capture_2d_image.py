# With this sample, you can obtain and save the 2D image.

import cv2

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect


class Capture2DImage(object):
    def __init__(self):
        self.camera = Camera()

    def capture_2d_image(self):
        frame_2d = Frame2D()
        show_error(self.camera.capture_2d(frame_2d))
        if frame_2d.color_type() == ColorTypeOf2DCamera_Monochrome:
            image2d = frame_2d.get_gray_scale_image()
        elif frame_2d.color_type() == ColorTypeOf2DCamera_Color:
            image2d = frame_2d.get_color_image()

        file_name = "2DImage.png"
        cv2.imwrite(file_name, image2d.data())
        print("Capture and save the 2D image: {}".format(file_name))

    def main(self):
        if find_and_connect(self.camera):
            self.capture_2d_image()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = Capture2DImage()
    a.main()
