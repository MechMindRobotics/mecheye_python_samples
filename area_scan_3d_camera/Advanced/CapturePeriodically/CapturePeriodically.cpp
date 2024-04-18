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
With this sample, you can obtain and save 2D images, depth maps and point clouds
periodically for the specified duration from a camera.
*/

#include <chrono>
#include <thread>
#include <opencv2/imgcodecs.hpp>
#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"

namespace {
void capture(mmind::eye::Camera& camera, std::string suffix)
{
    const std::string colorFile = suffix.empty() ? "2DImage.png" : "2DImage_" + suffix + ".png";
    const std::string depthFile = suffix.empty() ? "DepthMap.tiff" : "DepthMap_" + suffix + ".tiff";
    const std::string pointCloudFile =
        suffix.empty() ? "PointCloud.ply" : "PointCloud_" + suffix + ".ply";
    const std::string texturedPointCloudFile =
        suffix.empty() ? "TexturedPointCloud.ply" : "TexturedPointCloud_" + suffix + ".ply";

    mmind::eye::Frame2DAnd3D frame2DAnd3D;
    showError(camera.capture2DAnd3D(frame2DAnd3D));

    // Save the obtained data with the set filenames.
    mmind::eye::Color2DImage colorImage = frame2DAnd3D.frame2D().getColorImage();
    cv::Mat color8UC3 =
        cv::Mat(colorImage.height(), colorImage.width(), CV_8UC3, colorImage.data());
    cv::imwrite(colorFile, color8UC3);
    std::cout << "Capture and save the 2D image: " << colorFile << std::endl;

    mmind::eye::DepthMap depthMap = frame2DAnd3D.frame3D().getDepthMap();
    cv::Mat depth32F = cv::Mat(depthMap.height(), depthMap.width(), CV_32FC1, depthMap.data());
    cv::imwrite(depthFile, depth32F);
    std::cout << "Capture and save the depth map: " << depthFile << std::endl;

    showError(frame2DAnd3D.frame3D().saveUntexturedPointCloud(mmind::eye::FileFormat::PLY,
                                                              pointCloudFile));
    std::cout << "Capture and save the untextured point cloud: " << pointCloudFile << std::endl;

    showError(
        frame2DAnd3D.saveTexturedPointCloud(mmind::eye::FileFormat::PLY, texturedPointCloudFile));
    std::cout << "Capture and save the textured point cloud: " << texturedPointCloudFile << std::endl;
}
} // namespace

int main()
{
    // Set the camera capture interval to 10 seconds and the total duration of image capturing to 5
    // minutes.
    const auto captureTime = std::chrono::minutes(5);
    const auto capturePeriod = std::chrono::seconds(10);

    mmind::eye::Camera camera;
    if (!findAndConnect(camera))
        return -1;

    mmind::eye::CameraInfo cameraInfo;
    showError(camera.getCameraInfo(cameraInfo));
    printCameraInfo(cameraInfo);

    if (!confirmCapture3D()) {
        camera.disconnect();
        return 0;
    }
    std::cout << "Start capturing for " << captureTime.count() << " minutes." << std::endl;

    const auto start = std::chrono::high_resolution_clock::now();

    // Perform image capturing periodically according to the set interval for the set total
    // duration.
    while (std::chrono::high_resolution_clock::now() - start < captureTime) {
        const auto before = std::chrono::high_resolution_clock::now();

        std::ostringstream ss;
        ss << (std::chrono::duration_cast<std::chrono::seconds>(before - start)).count();
        std::string time = ss.str();

        capture(camera, time);

        const auto after = std::chrono::high_resolution_clock::now();
        const auto timeUsed = after - before;
        if (timeUsed < capturePeriod)
            std::this_thread::sleep_for(capturePeriod - timeUsed);
        else {
            std::cout << "The actual capture time is longer than the set capture interval. Please increase "
                         "the capture interval."
                      << std::endl;
        }

        const auto timeRemaining =
            captureTime - (std::chrono::high_resolution_clock::now() - start);
        const auto remainingMinutes =
            std::chrono::duration_cast<std::chrono::minutes>(timeRemaining);
        const auto remainingSeconds =
            std::chrono::duration_cast<std::chrono::seconds>(timeRemaining - remainingMinutes);
        std::cout << "Remaining time: " << remainingMinutes.count() << " minutes and "
                  << remainingSeconds.count() << "seconds." << std::endl;
    }

    std::cout << "Capturing for " << captureTime.count() << " minutes is completed." << std::endl;

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
