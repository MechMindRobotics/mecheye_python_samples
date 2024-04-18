/*******************************************************************************
 *BSD 3-Clause License
 *
 *Copyright (c) 2016-2024, Mech-Mind Robotics
 *All rights reserved.
 *
 *Redistribution and use in source and binary forms, with or without
 *modification, are permitted provided that the following conditions are met:
 *
 *1. Redistributions of source code must retain the above copyright notice, this
 *   list of conditions and the following disclaimer.
 *
 *2. Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 *
 *3. Neither the name of the copyright holder nor the names of its
 *   contributors may be used to endorse or promote products derived from
 *   this software without specific prior written permission.
 *
 *THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 *DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 *FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 *DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 *SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 *CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 *OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 *OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 ******************************************************************************/

/*
With this sample, you can perform hand-eye calibration and obtain the extrinsic parameters.
This document contains instructions for building the sample program and using the sample program to
complete hand-eye calibration.
*/

#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"
#include "HandEyeCalibrationUtil.h"
#include <opencv2/highgui/highgui.hpp>

int main()

{
    mmind::eye::Camera camera;
    mmind::eye::HandEyeCalibration calibration;
    if (!findAndConnect(camera))
        return -1;

    // Set the camera mounting mode.
    mmind::eye::HandEyeCalibration::CameraMountingMode mountingMode;
    bool setCalibrationTypeSuccess = inputCalibType(mountingMode);
    while (!setCalibrationTypeSuccess) {
        setCalibrationTypeSuccess = inputCalibType(mountingMode);
    }
    // Set the model of the calibration board.
    mmind::eye::HandEyeCalibration::CalibrationBoardModel boardModel;
    bool setboardTypeSuccess = inputBoardType(boardModel);
    while (!setboardTypeSuccess) {
        setboardTypeSuccess = inputBoardType(boardModel);
    };
    showError(calibration.initializeCalibration(camera, mountingMode, boardModel));

    // Set the Euler angle convention.
    auto eulerType = getEulerType();
    while (eulerType == 0) // Prompt to enter again if the entered number is invalid.
    {
        std::cout << "Invalid Euler angle convention. Please enter again." << std::endl;
        eulerType = getEulerType();
    }

    std::cout << "\n******************************************************************************"
                 "\nExtrinsic parameter calculation requires at least 15 robot poses."
                 "\nDuring the hand-eye calibration, please make sure you enter enough robot poses"
                 "\nat which the feature detection of the 2D image is successful."
                 "\n******************************************************************************"
              << std::endl;
    int poseIndex = 1;
    mmind::eye::HandEyeCalibration::Transformation cameraToBase;
    bool calibrate{false};
    do {
        switch (enterCommand()) {
        case CommandType::GetOriginImg: // Obtain the original 2D image.
        {
            mmind::eye::Frame2D frame2D;
            showError(camera.capture2D(frame2D));
            if (!frame2D.isEmpty()) {
                std::string colorFile = "Original2DImage_" + std::to_string(poseIndex);
                colorFile += ".png";
                cv::Mat testImg = cv::Mat(frame2D.imageSize().height, frame2D.imageSize().width,
                                          CV_8UC3, frame2D.getColorImage().data());
                //                cv::namedWindow("Original 2D Image", 0);
                //                cv::resizeWindow("Original 2D Image", frame2D.imageSize().width /
                //                2,
                //                                 frame2D.imageSize().height / 2);
                //                cv::imshow("Original 2D Image", testImg);
                //                std::cout << "Press any key to close the image." << std::endl;
                //                cv::waitKey(0);
                //                cv::destroyAllWindows();
                cv::imwrite(colorFile, testImg);
                std::cout << "Save the image to file " << colorFile << std::endl;
            }
            break;
        }
        case CommandType::GetPatternImg: // Obtain the 2D image with feature point recognition
                                         // results.
        {
            mmind::eye::Color2DImage color2DImage;
            showError(calibration.testRecognition(camera, color2DImage));
            if (!color2DImage.isEmpty()) {
                std::string colorFile =
                    "FeatureRecognitionResultForTest_" + std::to_string(poseIndex);
                colorFile += ".png";
                cv::Mat testImg = cv::Mat(color2DImage.height(), color2DImage.width(), CV_8UC3,
                                          color2DImage.data());
                //                cv::namedWindow("Feature Recognition Result", 0);
                //                cv::resizeWindow("Feature Recognition Result",
                //                color2DImage.width() / 2,
                //                                 color2DImage.height() / 2);
                //                cv::imshow("Feature Recognition Result", testImg);
                //                std::cout << "Press any key to close the image." << std::endl;
                //                cv::waitKey(0);
                //                cv::destroyAllWindows();
                cv::imwrite(colorFile, testImg);
                std::cout << "Save the image to file " << colorFile << std::endl;
            }
            break;
        }
        case CommandType::AddPose: // Input the current robot pose. The unit of the translational
                                   // components is mm, and the unit of the Euler angles is degrees.

        {
            auto robotPose = enterRobotPose(eulerType);
            std::cout << "\nThe current pose index is " << poseIndex
                      << "\nIf the above pose is correct, enter y; otherwise, press any key to "
                         "enter the pose again."
                      << std::endl;
            std::string key;
            std::cin >> key;
            while (key != "y") {
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                std::cout << std::endl;
                std::cout << "Enter the pose again:" << std::endl;
                robotPose = enterRobotPose(eulerType);
                std::cout << "\nThe current pose index is " << poseIndex
                          << "\nIf the above pose is correct, enter y; otherwise, press any key to "
                             "enter the pose again."
                          << std::endl;
                std::cin >> key;
            }
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            mmind::eye::Color2DImage color2DImage;
            auto errStatus = calibration.addPoseAndDetect(camera, robotPose, color2DImage);
            showError(errStatus);
            if (!color2DImage.isEmpty()) {
                std::string colorFile = "FeatureRecognitionResult_" + std::to_string(poseIndex);
                colorFile += ".png";
                cv::Mat testImg = cv::Mat(color2DImage.height(), color2DImage.width(), CV_8UC3,
                                          color2DImage.data());
                //                cv::namedWindow("Feature Recognition Result", 0);
                //                cv::resizeWindow("Feature Recognition Result",
                //                color2DImage.width() / 2,
                //                                 color2DImage.height() / 2);
                //                cv::imshow("Feature Recognition Result", testImg);
                //                std::cout << "Press any key to close the image." << std::endl;
                //                cv::waitKey(0);
                //                cv::destroyAllWindows();
                cv::imwrite(colorFile, testImg);
                std::cout << "Save the image to file " << colorFile << std::endl;
                std::cout << "Successfully added the pose." << std::endl;
            }
            if (errStatus.isOK()) {
                poseIndex++;
            }
            break;
        }
        case CommandType::Calibrate: // Calculate extrinsic parameters.
        {
            calibrate = true;
            mmind::eye::ErrorStatus status = calibration.calculateExtrinsics(camera, cameraToBase);
            showError(status);
            if (status.isOK()) {
                std::cout << "The extrinsic parameters are:" << std::endl;
                std::cout << cameraToBase.toString() << std::endl;
                saveExtrinsicParameters(cameraToBase.toString());
            }
            break;
        }
        case CommandType::Unknown:
        {
            std::cout << "Error: Unknown command" << std::endl;
            break;
        }
        }
    } while (!calibrate);
    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
