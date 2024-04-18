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
With this sample, you can obtain the point cloud data from a camera, and then transform and save
the point clouds using the HALCON C++ interface.
*/

#include <thread>
#include <algorithm>
#include <chrono>
#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"
#include "halconcpp/HalconCpp.h"
#include "HalconUtil.h"

int main()
{
    //  List all available cameras and connect to a camera by the displayed index.
    mmind::eye::Camera camera;
    if (!findAndConnect(camera))
        return -1;

    // Obtain the untextured point cloud data and convert it to a HALCON ObjectModel3D object.
    if (!confirmCapture3D()) {
        camera.disconnect();
        return 0;
    }
    mmind::eye::Frame3D frame3D;
    showError(camera.capture3D(frame3D));
    mmind::eye::UntexturedPointCloud pointCloud = frame3D.getUntexturedPointCloud();

    const auto halconPointCloudXYZ = mecheyeToHalconPointCloud(pointCloud);

    // Save the untextured point cloud.
    const auto pointCloudFileXYZ = "UntexturedPointCloud.ply";
    std::cout << "Save the point cloud to file: " << pointCloudFileXYZ << std::endl;
    savePointCloud(halconPointCloudXYZ, pointCloudFileXYZ);

    // Obtain the textured point cloud data and convert it to a HALCON ObjectModel3D object.
    mmind::eye::Frame2DAnd3D frame2DAnd3D;
    showError(camera.capture2DAnd3D(frame2DAnd3D));
    mmind::eye::TexturedPointCloud texturedPointCloud = frame2DAnd3D.getTexturedPointCloud();

    const auto halconPointCloudXYZRGB = mecheyeToHalconPointCloud(texturedPointCloud);

    // Save the textured point cloud.
    const auto pointCloudFileXYZRGB = "TexturedPointCloud.ply";
    std::cout << "Save the textured point cloud to file: " << pointCloudFileXYZRGB << std::endl;
    savePointCloud(halconPointCloudXYZRGB, pointCloudFileXYZRGB);

    // Disconnect the camera and exit
    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
