# With this sample, you can obtain and save the depth map rendered with the jet color scheme.

import cv2
import numpy as np

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, confirm_capture_3d


class RenderedDepthMap(object):
    def __init__(self):
        self.camera = Camera()

    def render_depth_data(self, depth):
        if depth is None or depth.size == 0:
            return np.array([])

        mask = np.isfinite(depth).astype(np.uint8)
        min_depth_value, max_depth_value, _, _ = cv2.minMaxLoc(depth, mask)

        if np.isclose(max_depth_value - min_depth_value, 0):
            depth8U = depth.astype(np.uint8)
        else:
            depth8U = cv2.convertScaleAbs(depth, alpha=(255.0 / (min_depth_value - max_depth_value)), beta=(
                (max_depth_value * 255.0) / (max_depth_value - min_depth_value) + 1))

        if depth8U.size == 0:
            return np.array([])

        colored_depth = cv2.applyColorMap(depth8U, cv2.COLORMAP_JET)
        colored_depth[depth8U == 0] = [0, 0, 0]

        return colored_depth

    def capture_rendered_depth_map(self):
        frame3d = Frame3D()
        show_error(self.camera.capture_3d(frame3d))

        rendered_depth_map = self.render_depth_data(
            frame3d.get_depth_map().data())
        rendered_depth_file = "RenderedDepthMap.tiff"
        cv2.imwrite(rendered_depth_file, rendered_depth_map)
        print("Capture and save the rendered depth map: {}".format(
            rendered_depth_file))

    def main(self):
        if find_and_connect(self.camera):
            if not confirm_capture_3d():
                return
            self.capture_rendered_depth_map()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = RenderedDepthMap()
    a.main()
