# With this sample, you can perform hand-eye calibration and obtain the extrinsic parameters.
# This document contains instructions for building the sample program and using the sample program to
# complete hand-eye calibration.

import cv2
import time
from math import sin, cos

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, confirm_capture_3d


def get_input_int(min: int, max: int, warning_message: str):
    while True:
        user_input = input()
        if user_input.isdigit() and min <= int(user_input) <= max:
            return int(user_input)
        print(warning_message)


def get_input_float():
    while True:
        user_input = input()
        try:
            return float(user_input)
        except:
            print("Please enter a number.")


def show_and_save_image(image, file_name: str, window_name: str):
    if image.is_empty():
        return
    # cv2.namedWindow(window_name, 0)
    # cv2.resizeWindow(window_name, int(image.width() /
    #                  2), int(image.height() / 2))
    # cv2.imshow(window_name, image.data())
    # print("Press any key to close the image")
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite(file_name, image.data())
    print("Save the image to file", file_name)


def save_extrinsic_parameters(extrinsic_parameters: str):
    # Generate a timestamped file name
    curr_time = time.localtime()
    file_name = "ExtrinsicParameters{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}.txt".format(
        curr_time.tm_year, curr_time.tm_mon, curr_time.tm_mday,
        curr_time.tm_hour, curr_time.tm_min, curr_time.tm_sec
    )

    # Write the extrinsic parameters to the file
    with open(file_name, "w") as out_file:
        out_file.write("ExtrinsicParameters:\n")
        out_file.write(extrinsic_parameters)

    print(f"Save result in file {file_name}")


class HandEyeCalibrationSample:
    def __init__(self):
        self.camera = Camera()
        self.calibration = HandEyeCalibration()

    def input_calib_type(self):
        print("\nEnter the number that represents the camera mounting method.")
        print("1: eye-in-hand")
        print("2: eye-to-hand")
        input_type = get_input_int(
            1, 2, "Unknown calibrateType, please enter correct calibrateType number.")
        if input_type == 1:
            self.mounting_mode = HandEyeCalibration.CameraMountingMode_EyeInHand
        elif input_type == 2:
            self.mounting_mode = HandEyeCalibration.CameraMountingMode_EyeToHand

    def input_board_type(self):
        print("\nEnter the number that represent the model of your calibration board (the model is labeled on the calibration board)")
        print("1: BDB-5\n2:BDB-6\n3:BDB-7")
        print("4: CGB-020\n5: CGB-035\n6: CGB-050")
        print("7: OCB-005\n8: OCB-010\n9: OCB-015\n10: OCB-020")
        input_type = get_input_int(
            1, 10, "Unknown boardType, please enter correct boardType number.")
        if input_type == 1:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_BDB_5
        elif input_type == 2:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_BDB_6
        elif input_type == 3:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_BDB_7
        elif input_type == 4:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_CGB_20
        elif input_type == 5:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_CGB_35
        elif input_type == 6:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_CGB_50
        elif input_type == 7:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_OCB_5
        elif input_type == 8:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_OCB_10
        elif input_type == 9:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_OCB_15
        elif input_type == 10:
            self.board_model = HandEyeCalibration.CalibrationBoardModel_OCB_20

    def input_euler_type(self):
        print(
            "\nEnter the number that represents the Euler angle convention of your robot.")
        print("1: Z-Y'-X'' (intrinsic rotations) : the intrinsic rotations are known as: yaw, pitch and roll")
        print("2: Z-Y'-Z''/OAT (intrinsic rotations) ")
        print("3: X-Y'-Z''(intrinsic rotations) ")
        print("4: Z-X'-Z'' (intrinsic rotations) ")
        print("5: X-Y-Z/WPR (extrinsic rotations) ")
        input_type = get_input_int(
            1, 5, "Unknown eulerType, please enter correct eulerType number.")
        self.euler_type_code = input_type

    def input_command(self):
        print("\nEnter the letter that represents the action you want to perform.")
        print("P: obtain the original 2D image")
        print("T: obtain the 2D image with feature recognition result")
        print("A: enter the current robot pose")
        print("C: calculate extrinsic parameters")
        while True:
            user_input = input()
            if user_input == "P" or user_input == "p":
                return "P"
            elif user_input == "T" or user_input == "t":
                return "T"
            elif user_input == "A" or user_input == "a":
                return "A"
            elif user_input == "C" or user_input == "c":
                return "C"
            else:
                print("Unknown command, please enter correct command type")

    def euler_to_quad(self):
        a1 = self.pose_r1 * PI / 180 / 2
        a2 = self.pose_r2 * PI / 180 / 2
        a3 = self.pose_r3 * PI / 180 / 2
        if self.euler_type_code == 1:  # Z-Y'-X''
            quad_w = sin(a1) * sin(a2) * sin(a3) + cos(a1) * cos(a2) * cos(a3)
            quad_x = -sin(a1) * sin(a2) * cos(a3) + sin(a3) * cos(a1) * cos(a2)
            quad_y = sin(a1) * sin(a3) * cos(a2) + sin(a2) * cos(a1) * cos(a3)
            quad_z = sin(a1) * cos(a2) * cos(a3) - sin(a2) * sin(a3) * cos(a1)
        elif self.euler_type_code == 2:  # Z-Y'-Z''
            quad_w = cos(a2) * cos(a1 + a3)
            quad_x = -sin(a2) * sin(a1 - a3)
            quad_y = sin(a2) * cos(a1 - a3)
            quad_z = cos(a2) * sin(a1 + a3)
        elif self.euler_type_code == 3:  # X-Y'-Z''
            quad_w = -sin(a1) * sin(a2) * sin(a3) + cos(a1) * cos(a2) * cos(a3)
            quad_x = sin(a1) * cos(a2) * cos(a3) + sin(a2) * sin(a3) * cos(a1)
            quad_y = -sin(a1) * sin(a3) * cos(a2) + sin(a2) * cos(a1) * cos(a3)
            quad_z = sin(a1) * sin(a2) * cos(a3) + sin(a3) * cos(a1) * cos(a2)
        elif self.euler_type_code == 4:  # Z-X'-Z''
            quad_w = cos(a2) * cos(a1 + a3)
            quad_x = sin(a2) * cos(a1 - a3)
            quad_y = sin(a2) * sin(a1 - a3)
            quad_z = cos(a2) * sin(a1 + a3)
        elif self.euler_type_code == 5:  # X-Y-Z
            a1 = self.pose_r3 * PI / 180 / 2
            a3 = self.pose_r1 * PI / 180 / 2
            quad_w = sin(a1) * sin(a2) * sin(a3) + cos(a1) * cos(a2) * cos(a3)
            quad_x = -sin(a1) * sin(a2) * cos(a3) + sin(a3) * cos(a1) * cos(a2)
            quad_y = sin(a1) * sin(a3) * cos(a2) + sin(a2) * cos(a1) * cos(a3)
            quad_z = sin(a1) * cos(a2) * cos(a3) - sin(a2) * sin(a3) * cos(a1)
        print("\nThe entered pose is:")
        print(self.pose_x, self.pose_y, self.pose_z,
              self.pose_r1, self.pose_r2, self.pose_r3, sep=',')
        print("The converted pose (Euler angles --> quaternions) is: ")
        print(self.pose_x, self.pose_y, self.pose_z,
              quad_w, quad_x, quad_y, quad_z, sep=',')
        return HandEyeTransformation(self.pose_x, self.pose_y, self.pose_z, quad_w, quad_x, quad_y, quad_z)

    def input_robot_pose(self):
        while True:
            print("\nEnter the X translational component of the robot pose (in mm): ")
            self.pose_x = get_input_float()
            print("\nEnter the Y translational component of the robot pose (in mm): ")
            self.pose_y = get_input_float()
            print("\nEnter the Z translational component of the robot pose (in mm): ")
            self.pose_z = get_input_float()
            if self.euler_type_code == 1:  # Prompts for Z-Y'-X'' Euler angles
                print(
                    "\nEnter the Z rotational component of the robot pose (in degrees): ")
                self.pose_r1 = get_input_float()
                print(
                    "\nEnter the Y' rotational component of the robot pose (in degrees): ")
                self.pose_r2 = get_input_float()
                print(
                    "\nEnter the X'' rotational component of the robot pose (in degrees): ")
                self.pose_r3 = get_input_float()
            # Prompts for Z-Y'-Z'' (OAT) Euler angles
            elif self.euler_type_code == 2:
                print(
                    "\nEnter the Z(O) rotational component of the robot pose (in degrees): ")
                self.pose_r1 = get_input_float()
                print(
                    "\nEnter the Y'(A) rotational component of the robot pose (in degrees): ")
                self.pose_r2 = get_input_float()
                print(
                    "\nEnter the Z''(T) rotational component of the robot pose (in degrees): ")
                self.pose_r3 = get_input_float()
            elif self.euler_type_code == 3:  # Prompts for X-Y'-Z'' Euler angles
                print(
                    "\nEnter the X rotational component of the robot pose (in degrees): ")
                self.pose_r1 = get_input_float()
                print(
                    "\nEnter the Y' rotational component of the robot pose (in degrees): ")
                self.pose_r2 = get_input_float()
                print(
                    "\nEnter the Z'' rotational component of the robot pose (in degrees): ")
                self.pose_r3 = get_input_float()
            elif self.euler_type_code == 4:  # Prompts for Z-X'-Z'' Euler angles
                print(
                    "\nEnter the Z rotational component of the robot pose (in degrees): ")
                self.pose_r1 = get_input_float()
                print(
                    "\nEnter the X' rotational component of the robot pose (in degrees): ")
                self.pose_r2 = get_input_float()
                print(
                    "\nEnter the Z'' rotational component of the robot pose (in degrees): ")
                self.pose_r3 = get_input_float()
            # Prompts for X-Y-Z (WPR) Euler angles
            elif self.euler_type_code == 5:
                print(
                    "\nEnter the X rotational component of the robot pose (in degrees): ")
                self.pose_r1 = get_input_float()
                print(
                    "\nEnter the Y rotational component of the robot pose (in degrees): ")
                self.pose_r2 = get_input_float()
                print(
                    "\nEnter the Z rotational component of the robot pose (in degrees): ")
                self.pose_r3 = get_input_float()
            robot_pose = self.euler_to_quad()
            print("The current pose index is", self.pose_index)
            print(
                "If the above pose is correct, enter y; otherwise, press any key to enter the pose again.")
            user_input = input()
            if user_input == "y" or user_input == "Y":
                return robot_pose
            else:
                print("Enter the pose again:")

    def calibrate(self):
        print("\n******************************************************************************")
        print("Extrinsic parameter calculation requires at least 15 robot poses.")
        print(
            "During the hand-eye calibration, please make sure you enter enough robot poses")
        print("at which the feature detection of the 2D image is successful.")
        print(
            "******************************************************************************")
        self.pose_index = 1
        camera_to_base = HandEyeTransformation()
        calibrate = False
        while not calibrate:
            command = self.input_command()
            if command == "P":  # Obtain the original 2D image
                frame_2d = Frame2D()
                show_error(self.camera.capture_2d(frame_2d))
                show_and_save_image(frame_2d.get_color_image(
                ), file_name="Original2DImage_" + str(self.pose_index) + ".png", window_name="Original 2D Image")
            elif command == "T":  # Obtain the 2D image with feature point recognition results.
                frame_3d = Frame3D()
                show_error(self.camera.capture_3d(frame_3d))
                show_and_save_image(frame_3d.get_depth_map(
                ), file_name="DepthMap_" + str(self.pose_index) + ".tiff", window_name="Depth")
                color_image = Color2DImage()
                show_error(self.calibration.test_recognition(
                    self.camera, color_image))
                show_and_save_image(color_image, file_name="FeatureRecognitionResultForTest_" + str(
                    self.pose_index) + ".png", window_name="Feature Recognition Result For Test")
            elif command == "A":  # Input the current robot pose. The unit of the translational component is mm, and the unit of the Euler angles is degrees.
                robot_pose = self.input_robot_pose()
                color_image = Color2DImage()
                error_status = self.calibration.add_pose_and_detect(
                    self.camera, robot_pose, color_image)
                show_error(error_status)
                show_and_save_image(color_image, file_name="FeatureRecognitionResult_" + str(
                    self.pose_index) + ".png", window_name="Feature Recognition Result")
                if error_status.is_ok():
                    self.pose_index = self.pose_index + 1
            elif command == "C":  # Calculate extrinsic parameters.
                calibrate = True
                error_status = self.calibration.calculate_extrinsics(
                    self.camera, camera_to_base)
                show_error(error_status)
                if error_status.is_ok():
                    print("The extrinsic parameters are:")
                    print(camera_to_base.to_string())
                    save_extrinsic_parameters(camera_to_base.to_string())

    def main(self):
        if not find_and_connect(self.camera):
            return
        self.input_calib_type()
        self.input_board_type()
        show_error(self.calibration.initialize_calibration(
            self.camera, self.mounting_mode, self.board_model))
        self.input_euler_type()
        self.calibrate()
        self.camera.disconnect()
        print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = HandEyeCalibrationSample()
    a.main()
