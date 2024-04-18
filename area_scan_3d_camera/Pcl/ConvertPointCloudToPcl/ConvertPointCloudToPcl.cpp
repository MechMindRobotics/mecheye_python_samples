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
With this sample, you can obtain the point cloud data from the camera and convert it to the PCL data
structure.
*/

#include <pcl/point_types.h>
#include <pcl/io/ply_io.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <vtkOutputWindow.h>
#include <thread>
#include "area_scan_3d_camera/api_util.h"
#include "area_scan_3d_camera/Camera.h"

namespace {

template <typename T,
          typename = std::enable_if_t<(std::is_same<T, mmind::eye::PointCloud>::value ||
                                       std::is_same<T, mmind::eye::TexturedPointCloud>::value)>>
bool containsInvalidPoint(const T& cloud)
{
    return std::any_of(
        cloud.data(), cloud.data() + cloud.width() * cloud.height() - 1, [](const auto& point) {
            return std::isnan(point.x) || std::isnan(point.y) || std::isnan(point.z) ||
                   std::isinf(point.x) || std::isinf(point.y) || std::isinf(point.z);
        });
}

void convertToPCL(const mmind::eye::PointCloud& cloud,
                  pcl::PointCloud<pcl::PointXYZ>& pclPointCloud)
{
    // write PointXYZ data
    uint32_t size = cloud.height() * cloud.width();
    pclPointCloud.resize(size);
    pclPointCloud.is_dense = !containsInvalidPoint<mmind::eye::PointCloud>(cloud);

    for (size_t i = 0; i < size; i++) {
        pclPointCloud[i].x = 0.001 * cloud[i].x; // mm to m
        pclPointCloud[i].y = 0.001 * cloud[i].y; // mm to m
        pclPointCloud[i].z = 0.001 * cloud[i].z; // mm to m
    }

    return;
}

void convertToPCL(const mmind::eye::TexturedPointCloud& texturedCloud,
                  pcl::PointCloud<pcl::PointXYZRGB>& pclTexturedPointCloud)
{
    // write PointXYZRGB data
    uint32_t size = texturedCloud.height() * texturedCloud.width();
    pclTexturedPointCloud.resize(size);
    pclTexturedPointCloud.is_dense =
        !containsInvalidPoint<mmind::eye::TexturedPointCloud>(texturedCloud);

    for (size_t i = 0; i < size; i++) {
        pclTexturedPointCloud[i].x = 0.001 * texturedCloud[i].x; // mm to m
        pclTexturedPointCloud[i].y = 0.001 * texturedCloud[i].y; // mm to m
        pclTexturedPointCloud[i].z = 0.001 * texturedCloud[i].z; // mm to m

        pclTexturedPointCloud[i].r = texturedCloud[i].r;
        pclTexturedPointCloud[i].g = texturedCloud[i].g;
        pclTexturedPointCloud[i].b = texturedCloud[i].b;
    }

    return;
}

void showPointCloud(const pcl::PointCloud<pcl::PointXYZ>& pointCloud)
{
    vtkOutputWindow::SetGlobalWarningDisplay(0);
    if (pointCloud.empty())
        return;

    pcl::visualization::PCLVisualizer cloudViewer("Point Cloud Viewer");
    cloudViewer.setShowFPS(false);
    cloudViewer.setBackgroundColor(0, 0, 0);
    cloudViewer.addPointCloud(pointCloud.makeShared());
    cloudViewer.addCoordinateSystem(0.01);
    cloudViewer.addText("Point cloud size: " + std::to_string(pointCloud.size()), 0, 25, 20, 1, 1,
                        1, "cloudSize");
    cloudViewer.addText("Press r/R to reset camera view point to center.", 0, 0, 16, 1, 1, 1,
                        "help");
    cloudViewer.initCameraParameters();
    while (!cloudViewer.wasStopped()) {
        cloudViewer.spinOnce(20);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

void showPointCloud(const pcl::PointCloud<pcl::PointXYZRGB>& colorPointCloud)
{
    vtkOutputWindow::SetGlobalWarningDisplay(0);
    if (colorPointCloud.empty())
        return;

    pcl::visualization::PCLVisualizer cloudViewer("Point Cloud Viewer");
    cloudViewer.setShowFPS(false);
    cloudViewer.setBackgroundColor(0, 0, 0);
    cloudViewer.addPointCloud(colorPointCloud.makeShared());
    cloudViewer.addCoordinateSystem(0.01);
    cloudViewer.addText("Point cloud size: " + std::to_string(colorPointCloud.size()), 0, 25, 20, 1,
                        1, 1, "cloudSize");
    cloudViewer.addText("Press r/R to reset camera view point to center.", 0, 0, 16, 1, 1, 1,
                        "help");
    cloudViewer.initCameraParameters();
    while (!cloudViewer.wasStopped()) {
        cloudViewer.spinOnce(20);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

} // namespace

int main()
{
    mmind::eye::Camera camera;
    if (!findAndConnect(camera))
        return -1;

    if (!confirmCapture3D()) {
        camera.disconnect();
        return 0;
    }
    mmind::eye::Frame2DAnd3D frame2DAnd3D;
    showError(camera.capture2DAnd3D(frame2DAnd3D));

    const mmind::eye::PointCloud pointCloud = frame2DAnd3D.frame3D().getUntexturedPointCloud();

    const std::string pointCloudFile = "UntexturedPointCloud.ply";
    pcl::PointCloud<pcl::PointXYZ> pointCloudPCL(pointCloud.width(), pointCloud.height());
    convertToPCL(pointCloud, pointCloudPCL);

    showPointCloud(pointCloudPCL);

    pcl::PLYWriter writer;
    writer.write(pointCloudFile, pointCloudPCL, true);
    std::cout << "The point cloud has: " << pointCloudPCL.width * pointCloudPCL.height
              << " data points." << std::endl;
    std::cout << "Save the untextured point cloud to file: " << pointCloudFile << std::endl;

    const mmind::eye::TexturedPointCloud texturedPointCloud = frame2DAnd3D.getTexturedPointCloud();

    std::string texturedPointCloudFile = "TexturedPointCloud.ply";
    pcl::PointCloud<pcl::PointXYZRGB> texturedPointCloudPCL(texturedPointCloud.width(),
                                                            texturedPointCloud.height());
    convertToPCL(texturedPointCloud, texturedPointCloudPCL);

    showPointCloud(texturedPointCloudPCL);
    writer.write(texturedPointCloudFile, texturedPointCloudPCL, true);
    std::cout << "The point cloud has: "
              << texturedPointCloudPCL.width * texturedPointCloudPCL.height << " data points."
              << std::endl;
    std::cout << "Save the textured point cloud to file: " << texturedPointCloudFile << std::endl;

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;

    return 0;
}
