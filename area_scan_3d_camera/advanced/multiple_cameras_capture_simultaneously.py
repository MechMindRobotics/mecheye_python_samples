# With this sample, you can obtain and save 2D images, depth maps and point clouds
# simultaneously from multiple cameras.

import cv2
import multiprocessing

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *


def capture_task(ip_address, serial_number):
    camera = Camera()
    if not camera.connect(ip_address).is_ok():
        return
    print(f"Camera {ip_address} start capturing.")

    frame_all_2d_3d = Frame2DAnd3D()
    show_error(camera.capture_2d_and_3d(frame_all_2d_3d))

    # Save the obtained data with the set filenames.
    color_file = f"2DImage_{serial_number}.png"
    depth_file = f"DepthMap_{serial_number}.tiff"
    point_cloud_file = f"TexturedPointCloud_{serial_number}.ply"

    color_image = frame_all_2d_3d.frame_2d().get_color_image()
    cv2.imwrite(color_file, color_image.data())
    print(f"Capture and save the 2D image: {color_file}")

    depth_image = frame_all_2d_3d.frame_3d().get_depth_map()
    cv2.imwrite(depth_file, depth_image.data())
    print(f"Capture and save the depth map: {depth_file}")

    success_message = f"Capture and save the textured point cloud: {point_cloud_file}"
    show_error(
        frame_all_2d_3d.save_textured_point_cloud(
            FileFormat_PLY, point_cloud_file), success_message
    )

    camera.disconnect()
    print("Disconnected from the camera successfully.")


class MultipleCamerasCaptureSimultaneously:
    def __init__(self):
        self.cameras = find_and_connect_multi_camera()

    def connect_device_and_capture(self):
        if not self.cameras:
            print("No cameras connected.")
            return

        if not confirm_capture_3d():
            return

        # Create a process for each camera
        processes = []
        for camera in self.cameras:
            camera_info = CameraInfo()
            show_error(camera.get_camera_info(camera_info))
            ip_address = camera_info.ip_address
            serial_number = camera_info.serial_number
            process = multiprocessing.Process(
                target=capture_task, args=(ip_address, serial_number))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

    def main(self):
        self.connect_device_and_capture()


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    a = MultipleCamerasCaptureSimultaneously()
    a.main()
