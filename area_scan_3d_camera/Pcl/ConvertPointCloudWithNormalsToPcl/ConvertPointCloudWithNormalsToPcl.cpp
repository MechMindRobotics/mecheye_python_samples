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
With this sample, you can obtain the point cloud data with normals from the camera and convert it to
the PCL data structure.
*/

#include <pcl/point_types.h>
#include <pcl/io/ply_io.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <vtkOutputWindow.h>
#include <thread>
#include "area_scan_3d_camera/api_util.h"
#include "area_scan_3d_camera/Camera.h"

namespace {

bool containsInvalidPoint(const mmind::eye::PointCloudWithNormals& cloud)
{
    return std::any_of(
        cloud.data(), cloud.data() + cloud.width() * cloud.height() - 1,
        [](const auto& pointWithNormals) {
            return std::isnan(pointWithNormals.point.x) || std::isnan(pointWithNormals.point.y) ||
                   std::isnan(pointWithNormals.point.z) || std::isnan(pointWithNormals.normal.x) ||
                   std::isnan(pointWithNormals.normal.y) || std::isnan(pointWithNormals.normal.z) ||
                   std::isinf(pointWithNormals.point.x) || std::isinf(pointWithNormals.point.y) ||
                   std::isinf(pointWithNormals.point.z) || std::isinf(pointWithNormals.normal.x) ||
                   std::isinf(pointWithNormals.normal.y) || std::isinf(pointWithNormals.normal.z);
        });
}

bool containsInvalidPoint(const mmind::eye::TexturedPointCloudWithNormals& cloud)
{
    return std::any_of(cloud.data(), cloud.data() + cloud.width() * cloud.height() - 1,
                       [](const auto& pointWithNormals) {
                           return std::isnan(pointWithNormals.colorPoint.x) ||
                                  std::isnan(pointWithNormals.colorPoint.y) ||
                                  std::isnan(pointWithNormals.colorPoint.z) ||
                                  std::isnan(pointWithNormals.normal.x) ||
                                  std::isnan(pointWithNormals.normal.y) ||
                                  std::isnan(pointWithNormals.normal.z) ||
                                  std::isinf(pointWithNormals.colorPoint.x) ||
                                  std::isinf(pointWithNormals.colorPoint.y) ||
                                  std::isinf(pointWithNormals.colorPoint.z) ||
                                  std::isinf(pointWithNormals.normal.x) ||
                                  std::isinf(pointWithNormals.normal.y) ||
                                  std::isinf(pointWithNormals.normal.z);
                       });
}

void convertToPCL(const mmind::eye::PointCloudWithNormals& cloud,
                  pcl::PointCloud<pcl::PointNormal>& pclPointCloud)
{
    // write PointNormal data
    uint32_t size = cloud.height() * cloud.width();
    pclPointCloud.resize(size);
    pclPointCloud.is_dense = !containsInvalidPoint(cloud);

    for (size_t i = 0; i < size; i++) {
        pclPointCloud[i].x = 0.001 * cloud[i].point.x; // mm to m
        pclPointCloud[i].y = 0.001 * cloud[i].point.y; // mm to m
        pclPointCloud[i].z = 0.001 * cloud[i].point.z; // mm to m
        pclPointCloud[i].normal_x = cloud[i].normal.x;
        pclPointCloud[i].normal_y = cloud[i].normal.y;
        pclPointCloud[i].normal_z = cloud[i].normal.z;
    }

    return;
}

void convertToPCL(const mmind::eye::TexturedPointCloudWithNormals& texturedCloud,
                  pcl::PointCloud<pcl::PointXYZRGBNormal>& pclTexturedPointCloud)
{
    // write PointXYZRGBNormal data
    uint32_t size = texturedCloud.height() * texturedCloud.width();
    pclTexturedPointCloud.resize(size);
    pclTexturedPointCloud.is_dense =
        !containsInvalidPoint(texturedCloud);

    for (size_t i = 0; i < size; i++) {
        pclTexturedPointCloud[i].x = 0.001 * texturedCloud[i].colorPoint.x; // mm to m
        pclTexturedPointCloud[i].y = 0.001 * texturedCloud[i].colorPoint.y; // mm to m
        pclTexturedPointCloud[i].z = 0.001 * texturedCloud[i].colorPoint.z; // mm to m

        pclTexturedPointCloud[i].r = texturedCloud[i].colorPoint.r;
        pclTexturedPointCloud[i].g = texturedCloud[i].colorPoint.g;
        pclTexturedPointCloud[i].b = texturedCloud[i].colorPoint.b;

        pclTexturedPointCloud[i].normal_x = texturedCloud[i].normal.x;
        pclTexturedPointCloud[i].normal_y = texturedCloud[i].normal.y;
        pclTexturedPointCloud[i].normal_z = texturedCloud[i].normal.z;
    }

    return;
}

void showPointCloud(const pcl::PointCloud<pcl::PointNormal>& pointCloud)
{
    vtkOutputWindow::SetGlobalWarningDisplay(0);
    if (pointCloud.empty())
        return;

    pcl::visualization::PCLVisualizer cloudViewer("Point Cloud Viewer");
    cloudViewer.setShowFPS(false);
    cloudViewer.setBackgroundColor(0, 0, 0);
    cloudViewer.addPointCloudNormals<pcl::PointNormal>(pointCloud.makeShared());
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

void showPointCloud(const pcl::PointCloud<pcl::PointXYZRGBNormal>& colorPointCloud)
{
    vtkOutputWindow::SetGlobalWarningDisplay(0);
    if (colorPointCloud.empty())
        return;

    pcl::visualization::PCLVisualizer cloudViewer("Point Cloud Viewer");
    cloudViewer.setShowFPS(false);
    cloudViewer.setBackgroundColor(0, 0, 0);
    cloudViewer.addPointCloudNormals<pcl::PointXYZRGBNormal>(colorPointCloud.makeShared());
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
    showError(camera.capture2DAnd3DWithNormal(frame2DAnd3D));

    const mmind::eye::PointCloudWithNormals pointCloud =
        frame2DAnd3D.frame3D().getUntexturedPointCloudWithNormals();

    const std::string pointCloudFile = "UntexturedPointCloudWithNormals.ply";
    pcl::PointCloud<pcl::PointNormal> pointCloudPCL(pointCloud.width(), pointCloud.height());
    convertToPCL(pointCloud, pointCloudPCL);

    showPointCloud(pointCloudPCL);

    pcl::PLYWriter writer;
    writer.write(pointCloudFile, pointCloudPCL, true);
    std::cout << "The point cloud has: " << pointCloudPCL.width * pointCloudPCL.height
              << " data points." << std::endl;
    std::cout << "Save the untextured point cloud with normals to file:" << pointCloudFile
              << std::endl;

    const mmind::eye::TexturedPointCloudWithNormals texturedPointCloud =
        frame2DAnd3D.getTexturedPointCloudWithNormals();

    std::string texturedPointCloudFile = "TexturedPointCloudWithNormals.ply";
    pcl::PointCloud<pcl::PointXYZRGBNormal> texturedPointCloudPCL(texturedPointCloud.width(),
                                                                  texturedPointCloud.height());
    convertToPCL(texturedPointCloud, texturedPointCloudPCL);

    showPointCloud(texturedPointCloudPCL);
    writer.write(texturedPointCloudFile, texturedPointCloudPCL, true);
    std::cout << "The point cloud has: "
              << texturedPointCloudPCL.width * texturedPointCloudPCL.height << " data points."
              << std::endl;
    std::cout << "Save the textured point cloud with normals to file: " << texturedPointCloudFile
              << std::endl;

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;

    return 0;
}
