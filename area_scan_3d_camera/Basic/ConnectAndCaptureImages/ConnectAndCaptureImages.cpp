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
With this sample, you can connect to a camera and obtain the 2D image, depth map, and point cloud data.
*/

#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"

int main()
{
    // List all available cameras and connect to a camera by the displayed index.
    mmind::eye::Camera camera;
    if (!findAndConnect(camera))
        return -1;

    // Obtain the 2D image and depth map resolutions of the camera.
    mmind::eye::CameraResolutions cameraResolutions;
    showError(camera.getCameraResolutions(cameraResolutions));
    printCameraResolutions(cameraResolutions);

    // Obtain the 2D image.
    mmind::eye::Frame2D frame2D;
    unsigned row = 0;
    unsigned col = 0;
    showError(camera.capture2D(frame2D));
    std::cout << "The size of the 2D image is: " << frame2D.imageSize().width
              << " (width) * " << frame2D.imageSize().height << " (height)." << std::endl;
    try {
        mmind::eye::ColorBGR colorBGR = frame2D.getColorImage().at(row, col);
        std::cout << "The RGB values of the pixel at (" << row << ", " << col
                  << ") is R: " << unsigned(colorBGR.r) << "; G: " << unsigned(colorBGR.g)
                  << "; B: " << unsigned(colorBGR.b) << "." << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << std::endl;
        camera.disconnect();
        return 0;
    }

    // Obtain the depth map.

    if (!confirmCapture3D()) {
        camera.disconnect();
        return 0;
    }
    mmind::eye::Frame3D frame3D;
    showError(camera.capture3D(frame3D));
    mmind::eye::DepthMap depthMap = frame3D.getDepthMap();

    std::cout << "The size of the depth map is: " << depthMap.width() << " (width) * " << depthMap.height()
              << " (height)." << std::endl;
    try {
        mmind::eye::PointZ depthElem = depthMap.at(row, col);
        std::cout << "The depth value of the pixel at (" << row << ", " << col << ") is " << depthElem.z
                  << " mm." << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << std::endl;
        camera.disconnect();
        return 0;
    }

    // Obtain the point cloud.
    mmind::eye::PointCloud pointCloud = frame3D.getUntexturedPointCloud();
    std::cout << "The size of the point cloud is" << pointCloud.width()
              << " (width) * " << pointCloud.height() << " (height)." << std::endl;
    try {
        mmind::eye::PointXYZ pointCloudElem = pointCloud.at(row, col);
        std::cout << "The coordinates of the point corresponding to the pixel at (" << row << ", " << col
                  << ") is X: " << pointCloudElem.x << " mm; Y: " << pointCloudElem.y
                  << " mm; Z:" << pointCloudElem.z << " mm." << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << std::endl;
        camera.disconnect();
        return 0;
    }

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
