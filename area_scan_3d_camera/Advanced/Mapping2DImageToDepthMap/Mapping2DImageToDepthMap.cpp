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
With this sample, you can generate untextured and textured point clouds from a masked 2D image and a depth map.
*/

#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"
#include "area_scan_3d_camera/Mapping2DToDepth.h"
#include "area_scan_3d_camera/Frame3D.h"
#include "area_scan_3d_camera/Frame2DAnd3D.h"

namespace {
bool contains(const mmind::eye::ROI& roi, int x, int y)
{
    return x >= roi.upperLeftX && x < roi.upperLeftX + roi.width && y >= roi.upperLeftY &&
           y < roi.upperLeftY + roi.height;
}

mmind::eye::GrayScale2DImage generateTextureMask(const mmind::eye::Color2DImage& color,
                                                 const mmind::eye::ROI& roi1,
                                                 const mmind::eye::ROI& roi2)
{
    mmind::eye::GrayScale2DImage mask;
    const int width = color.width();
    const int height = color.height();
    mask.resize(width, height);
    for (int r = 0; r < height; ++r) {
        for (int c = 0; c < width; ++c) {
            if (contains(roi1, c, r) || contains(roi2, c, r))
                mask.at(r, c).gray = 255;
        }
    }
    return mask;
}
} // namespace

int main()
{
    mmind::eye::Camera camera;
    if (!findAndConnect(camera))
        return -1;

    mmind::eye::Frame2D frame2D;
    mmind::eye::Color2DImage color2DImage;
    showError(camera.capture2D(frame2D));
    color2DImage = frame2D.getColorImage();

    if (!confirmCapture3D()) {
        camera.disconnect();
        return 0;
    }
    mmind::eye::Frame3D frame3D;
    mmind::eye::DepthMap depthMap;
    showError(camera.capture3D(frame3D));
    depthMap = frame3D.getDepthMap();

    mmind::eye::CameraIntrinsics cameraIntrinsics;
    showError(camera.getCameraIntrinsics(cameraIntrinsics));
    printCameraIntrinsics(cameraIntrinsics);

    const int width = color2DImage.width();
    const int height = color2DImage.height();
    mmind::eye::ROI roi1(width / 5, height / 5, width / 2, height / 2);
    mmind::eye::ROI roi2(width * 2 / 5, height * 2 / 5, width / 2, height / 2);

    /**
     *  Generate a mask of the following shape:
     *   ______________________________
     *  |                              |
     *  |                              |
     *  |   *****************          |
     *  |   *****************          |
     *  |   ************************   |
     *  |   ************************   |
     *  |          *****************   |
     *  |          *****************   |
     *  |                              |
     *  |______________________________|
     */
    mmind::eye::GrayScale2DImage validMask = generateTextureMask(color2DImage, roi1, roi2);

    mmind::eye::PointCloud pointCloud;
    showError(
        mmind::eye::getPointCloudAfterMapping(depthMap, validMask, cameraIntrinsics, pointCloud));

    std::string pointCloudFile = "UntexturedPointCloud.ply";
    showError(mmind::eye::Frame3D::savePointCloud(pointCloud, mmind::eye::FileFormat::PLY,
                                                  pointCloudFile));
    std::cout << "Save the untextured point cloud to file: " << pointCloudFile << std::endl;

    mmind::eye::TexturedPointCloud texturedPointCloud;
    showError(mmind::eye::getPointCloudAfterMapping(depthMap, validMask, color2DImage,
                                                    cameraIntrinsics, texturedPointCloud));

    std::string texturedPointCloudFile = "TexturedPointCloud.ply";
    showError(mmind::eye::Frame2DAnd3D::savePointCloud(
        texturedPointCloud, mmind::eye::FileFormat::PLY, texturedPointCloudFile));
    std::cout << "Save the textured point cloud to file: " << texturedPointCloudFile << std::endl;

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;

    return 0;
}
