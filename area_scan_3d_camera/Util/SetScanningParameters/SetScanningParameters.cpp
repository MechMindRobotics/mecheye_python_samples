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
With this sample, you can set the parameters in the "3D Parameters", "2D Parameters", and "ROI"
categories.
*/
#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"
#include "area_scan_3d_camera/parameters/Scanning3D.h"
#include "area_scan_3d_camera/parameters/Scanning2D.h"

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

    // Set the exposure times for acquiring depth information.
    showError(currentUserSet.setFloatArrayValue(
        mmind::eye::scanning3d_setting::ExposureSequence::name, std::vector<double>{5, 10}));

    // Obtain the current exposure times for acquiring depth information to check if the setting was
    // successful.
    std::vector<double> exposureSequence;
    showError(currentUserSet.getFloatArrayValue(
        mmind::eye::scanning3d_setting::ExposureSequence::name, exposureSequence));
    std::cout << "3D scanning exposure multiplier : " << exposureSequence.size() << "."
              << std::endl;
    for (size_t i = 0; i < exposureSequence.size(); i++) {
        std::cout << "3D scanning exposure time " << i + 1 << ": " << exposureSequence[i] << " ms."
                  << std::endl;
    }

    // Set the ROI for the depth map and point cloud, and then obtain the parameter value to check
    // if the setting was successful.
    mmind::eye::ROI roi(0, 0, 500, 500);
    showError(currentUserSet.setRoiValue(mmind::eye::scanning3d_setting::ROI::name, roi));
    mmind::eye::ROI curRoi;
    showError(currentUserSet.getRoiValue(mmind::eye::scanning3d_setting::ROI::name, curRoi));
    std::cout << "3D scanning ROI topLeftX: " << curRoi.upperLeftX
              << ", topLeftY: " << curRoi.upperLeftY << ", width: " << curRoi.width
              << ", height: " << curRoi.height << std::endl;

    // Set the exposure mode and exposure time for capturing the 2D image, and then obtain the
    // parameter values to check if the setting was successful.
    showError(currentUserSet.setEnumValue(
        mmind::eye::scanning2d_setting::ExposureMode::name,
        static_cast<int>(mmind::eye::scanning2d_setting::ExposureMode::Value::Timed)));

    showError(
        currentUserSet.setFloatValue(mmind::eye::scanning2d_setting::ExposureTime::name, 100));

    int exposureMode2D = 0;
    showError(currentUserSet.getEnumValue(mmind::eye::scanning2d_setting::ExposureMode::name,
                                          exposureMode2D));
    double scan2DExposureTime = 0;
    showError(currentUserSet.getFloatValue(mmind::eye::scanning2d_setting::ExposureTime::name,
                                           scan2DExposureTime));
    std::cout << "2D scanning exposure mode: " << exposureMode2D
              << ", exposure time: " << scan2DExposureTime << " ms." << std::endl;

    // Save all the parameter settings to the currently selected user sets.
    showError(currentUserSet.saveAllParametersToDevice());
    std::cout << "Save all parameters to the current user set." << std::endl;

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
