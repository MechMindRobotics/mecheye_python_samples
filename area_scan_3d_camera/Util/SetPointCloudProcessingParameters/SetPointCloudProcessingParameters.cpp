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
With this sample, you can set the "Point Cloud Processing" parameters.
*/
#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"
#include "area_scan_3d_camera/parameters/PointCloudProcessing.h"

int main()
{
    // List all available cameras and connect to a camera by the displayed index.
    mmind::eye::Camera camera;
    if (!findAndConnect(camera))
        return -1;

    // Obtain the basic information of the connected camera.
    mmind::eye::CameraInfo cameraInfo;
    showError(camera.getCameraInfo(cameraInfo));
    printCameraInfo(cameraInfo);

    mmind::eye::UserSet& currentUserSet = camera.currentUserSet();

    // Set the "Point Cloud Processing" parameters, and then obtain the parameter values to check if
    // the setting was successful.
    showError(currentUserSet.setEnumValue(
        mmind::eye::pointcloud_processing_setting::SurfaceSmoothing::name,
        static_cast<int>(
            mmind::eye::pointcloud_processing_setting::SurfaceSmoothing::Value::Normal)));
    showError(currentUserSet.setEnumValue(
        mmind::eye::pointcloud_processing_setting::NoiseRemoval::name,
        static_cast<int>(mmind::eye::pointcloud_processing_setting::NoiseRemoval::Value::Normal)));
    showError(currentUserSet.setEnumValue(
        mmind::eye::pointcloud_processing_setting::OutlierRemoval::name,
        static_cast<int>(
            mmind::eye::pointcloud_processing_setting::OutlierRemoval::Value::Normal)));
    showError(currentUserSet.setEnumValue(
        mmind::eye::pointcloud_processing_setting::EdgePreservation::name,
        static_cast<int>(
            mmind::eye::pointcloud_processing_setting::EdgePreservation::Value::Normal)));
    showError(currentUserSet.setBoolValue(
        mmind::eye::pointcloud_processing_setting::EnableDistortionCorrection::name, true));
    showError(currentUserSet.setIntValue(
        mmind::eye::pointcloud_processing_setting::DistortionCorrection::name, 3));

    int surfaceSmoothing = 0;
    int noiseRemoval = 0;
    int outlierRemoval = 0;
    int edgePreservation = 0;
    bool distortionCorrectionEnabled = false;
    int distortionCorrection = 0;
    showError(currentUserSet.getEnumValue(
        mmind::eye::pointcloud_processing_setting::SurfaceSmoothing::name, surfaceSmoothing));
    showError(currentUserSet.getEnumValue(
        mmind::eye::pointcloud_processing_setting::NoiseRemoval::name, noiseRemoval));
    showError(currentUserSet.getEnumValue(
        mmind::eye::pointcloud_processing_setting::OutlierRemoval::name, outlierRemoval));
    showError(currentUserSet.getEnumValue(
        mmind::eye::pointcloud_processing_setting::EdgePreservation::name, edgePreservation));
    showError(currentUserSet.getBoolValue(
        mmind::eye::pointcloud_processing_setting::EnableDistortionCorrection::name,
        distortionCorrectionEnabled));
    showError(currentUserSet.getIntValue(
        mmind::eye::pointcloud_processing_setting::DistortionCorrection::name,
        distortionCorrection));

    std::cout << "Point Cloud Surface Smoothing: " << surfaceSmoothing
              << " (0: Off, 1: Weak, 2: Normal, 3: Strong)" << std::endl;
    std::cout << "Point Cloud Noise Removal: " << noiseRemoval
              << " (0: Off, 1: Weak, 2: Normal, 3: Strong)" << std::endl;
    std::cout << "Point Cloud Outlier Removal: " << outlierRemoval
              << " (0: Off, 1: Weak, 2: Normal, 3: Strong)" << std::endl;
    std::cout << "Point Cloud Edge Preservation: " << edgePreservation
              << " (0: Sharp, 1: Normal, 2: Smooth)" << std::endl;
    std::cout << "Distortion Correction Enabled ? " << distortionCorrectionEnabled << std::endl;
    std::cout << "Distortion Correction: " << distortionCorrection << std::endl;

    // Save all the parameter settings to the currently selected user set.
    showError(currentUserSet.saveAllParametersToDevice());
    std::cout << "Save all parameters to the current user set." << std::endl;

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
