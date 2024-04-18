#include <thread>
#include <algorithm>
#include <chrono>

#include "area_scan_3d_camera/Camera.h"
#include "halconcpp/HalconCpp.h"

/*************************************************
Function:       // savePointCloud
Description:    // Save Halcon's 3D model locally
Input:          // 1. HObjectModel3D Address
                // 2. File Path (Ends with. ply)
Others:         // You can open and view the ply file through readply.hdev
*************************************************/
void savePointCloud(const HalconCpp::HObjectModel3D& model, const std::string& fileName);

/*************************************************
Function:       // mecheyeToHalconPointCloud  overloaded function
Description:    // Convert the white point cloud data obtained from eye's c++sdk into a 3d model in
halcon
Input:          // Point cloud information defined in eye
Output:         // Point cloud information defined in halcon
*************************************************/
HalconCpp::HObjectModel3D mecheyeToHalconPointCloud(const mmind::eye::PointCloud& pointCloud);

/*************************************************
Function:       // mecheyeToHalconPointCloud  overloaded function
Description:    // Convert color point cloud data obtained from eye's c++sdk to color 3d model in
halcon
Input:          // Color point cloud information defined in eye
Output:         // Point cloud information defined in halcon
*************************************************/
HalconCpp::HObjectModel3D mecheyeToHalconPointCloud(
    const mmind::eye::TexturedPointCloud& pointCloud);
