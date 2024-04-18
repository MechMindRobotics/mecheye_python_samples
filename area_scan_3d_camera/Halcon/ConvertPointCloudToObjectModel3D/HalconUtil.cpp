#include "HalconUtil.h"

void savePointCloud(const HalconCpp::HObjectModel3D& model, const std::string& fileName)
{
    model.WriteObjectModel3d(HalconCpp::HString{"ply"}, HalconCpp::HString{fileName.c_str()},
                             HalconCpp::HString{"invert_normals"}, HalconCpp::HString{"false"});
}

HalconCpp::HObjectModel3D mecheyeToHalconPointCloud(const mmind::eye::PointCloud& pointCloud)
{
    const auto width = pointCloud.width();
    const auto height = pointCloud.height();

    Hlong numberOfValidPoints = width * height;

    HalconCpp::HTuple tuplePointsX, tuplePointsY, tuplePointsZ, tupleXYZMapping;

    tuplePointsX[numberOfValidPoints - 1] = (float)0.0;
    tuplePointsY[numberOfValidPoints - 1] = (float)0.0;
    tuplePointsZ[numberOfValidPoints - 1] = (float)0.0;

    tupleXYZMapping[2 * numberOfValidPoints + 2 - 1] = (Hlong)0;
    tupleXYZMapping[0] = (Hlong)width;
    tupleXYZMapping[1] = (Hlong)height;
    // color
    // Hlong == INT4_8
    // mmind  uint8_t
    int validPointIndex = 0;
    // std::cout << sizeof(tuplePointsX.DArr()) << std::endl;
    for (size_t i = 0; i < height; ++i) {
        for (size_t j = 0; j < width; ++j) {
            tuplePointsX.DArr()[validPointIndex] = 0.001 * pointCloud[validPointIndex].x; // mm to m
            tuplePointsY.DArr()[validPointIndex] = 0.001 * pointCloud[validPointIndex].y; // mm to m
            tuplePointsZ.DArr()[validPointIndex] = 0.001 * pointCloud[validPointIndex].z; // mm to m
            tupleXYZMapping.LArr()[2 + validPointIndex] = i;
            tupleXYZMapping.LArr()[2 + numberOfValidPoints + validPointIndex] = j;
            validPointIndex++;
        }
    }

    std::cout << "Constructing ObjectModel3D based on XYZ data" << std::endl;
    HalconCpp::HObjectModel3D objectModel3D(tuplePointsX, tuplePointsY, tuplePointsZ);

    std::cout << "Mapping ObjectModel3D data" << std::endl;
    HalconCpp::SetObjectModel3dAttribMod(objectModel3D, "xyz_mapping", "object", tupleXYZMapping);
    return objectModel3D;
}

HalconCpp::HObjectModel3D mecheyeToHalconPointCloud(
    const mmind::eye::TexturedPointCloud& pointCloud)
{
    const auto width = pointCloud.width();
    const auto height = pointCloud.height();

    Hlong numberOfValidPoints = width * height;

    HalconCpp::HTuple tuplePointsX, tuplePointsY, tuplePointsZ, tupleColorsR, tupleColorsB,
        tupleColorsG, tupleXYZMapping;

    tuplePointsX[numberOfValidPoints - 1] = (float)0.0;
    tuplePointsY[numberOfValidPoints - 1] = (float)0.0;
    tuplePointsZ[numberOfValidPoints - 1] = (float)0.0;

    tupleColorsR[numberOfValidPoints - 1] = (Hlong)0;
    tupleColorsG[numberOfValidPoints - 1] = (Hlong)0;
    tupleColorsB[numberOfValidPoints - 1] = (Hlong)0;

    tupleXYZMapping[2 * numberOfValidPoints + 2 - 1] = (Hlong)0;
    tupleXYZMapping[0] = (Hlong)width;
    tupleXYZMapping[1] = (Hlong)height;
    // color
    // Hlong == INT4_8
    // mmind  uint8_t
    int validPointIndex = 0;

    for (size_t i = 0; i < height; ++i) {
        for (size_t j = 0; j < width; ++j) {
            tuplePointsX.DArr()[validPointIndex] = 0.001 * pointCloud[validPointIndex].x; // mm to m
            tuplePointsY.DArr()[validPointIndex] = 0.001 * pointCloud[validPointIndex].y; // mm to m
            tuplePointsZ.DArr()[validPointIndex] = 0.001 * pointCloud[validPointIndex].z; // mm to m
            tupleColorsR.LArr()[validPointIndex] = pointCloud[validPointIndex].r;
            tupleColorsG.LArr()[validPointIndex] = pointCloud[validPointIndex].g;
            tupleColorsB.LArr()[validPointIndex] = pointCloud[validPointIndex].b;
            tupleXYZMapping.LArr()[2 + validPointIndex] = i;
            tupleXYZMapping.LArr()[2 + numberOfValidPoints + validPointIndex] = j;
            validPointIndex++;
        }
    }

    std::cout << "Constructing ObjectModel3D based on XYZ data" << std::endl;
    HalconCpp::HObjectModel3D objectModel3D(tuplePointsX, tuplePointsY, tuplePointsZ);

    std::cout << "Mapping ObjectModel3D data" << std::endl;
    HalconCpp::SetObjectModel3dAttribMod(objectModel3D, "xyz_mapping", "object", tupleXYZMapping);

    std::cout << "Adding RGB to ObjectModel3D" << std::endl;
    HalconCpp::SetObjectModel3dAttribMod(objectModel3D, "red", "points", tupleColorsR);
    HalconCpp::SetObjectModel3dAttribMod(objectModel3D, "green", "points", tupleColorsG);
    HalconCpp::SetObjectModel3dAttribMod(objectModel3D, "blue", "points", tupleColorsB);

    return objectModel3D;
}
