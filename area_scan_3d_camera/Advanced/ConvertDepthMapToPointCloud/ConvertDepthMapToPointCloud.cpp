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
With this sample, you can generate a point cloud from the depth map and save the point cloud.
*/

#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"

void convertDepthToPointCloud(const mmind::eye::DepthMap& depth,
                              const mmind::eye::CameraIntrinsics& intrinsics,
                              mmind::eye::PointCloud& pointCloud)
{
    pointCloud.resize(depth.width(), depth.height());

    for (int i = 0; i < depth.width() * depth.height(); i++) {
        const unsigned row = i / depth.width();
        const unsigned col = i - row * depth.width();
        pointCloud[i].z = depth[i].z;
        pointCloud[i].x =
            static_cast<float>(pointCloud[i].z * (col - intrinsics.depth.cameraMatrix.cx) /
                               intrinsics.depth.cameraMatrix.fx);
        pointCloud[i].y =
            static_cast<float>(pointCloud[i].z * (row - intrinsics.depth.cameraMatrix.cy) /
                               intrinsics.depth.cameraMatrix.fy);
    }
}

int main()
{
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

    mmind::eye::Frame3D frame3D;
    showError(camera.capture3D(frame3D));
    mmind::eye::DepthMap depth = frame3D.getDepthMap();

    mmind::eye::CameraIntrinsics cameraIntrinsics;
    showError(camera.getCameraIntrinsics(cameraIntrinsics));

    std::string pointCloudFile = "PointCloud.ply";
    mmind::eye::PointCloud pointCloud;
    convertDepthToPointCloud(depth, cameraIntrinsics, pointCloud);
    mmind::eye::Frame3D::savePointCloud(pointCloud, mmind::eye::FileFormat::PLY, pointCloudFile);

    std::cout << "The point cloud contains: " << pointCloud.width() * pointCloud.height() << " data points."
              << std::endl;
    std::cout << "Save the point cloud to file: " << pointCloudFile << std::endl;

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
