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
With this sample, you can connect to a camera.
*/

#include <regex>
#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"

int main()
{
    std::cout << "Discovering all available cameras..." << std::endl;
    std::vector<mmind::eye::CameraInfo> cameraInfoList = mmind::eye::Camera::discoverCameras();

    if (cameraInfoList.empty()) {
        std::cout << "No cameras found." << std::endl;
        return -1;
    }

    // Display the information of all available cameras.
    for (int i = 0; i < cameraInfoList.size(); i++) {
        std::cout << "Camera index: " << i << std::endl;
        printCameraInfo(cameraInfoList[i]);
    }

    std::cout << "Please enter the index of the camera that you want to connect: ";
    unsigned inputIndex;

    // Enter the index of the camera to be connected and check if the index is valid.
    while (1) {
        std::string str;
        std::cin >> str;
        if (std::regex_match(str.begin(), str.end(), std::regex{"[0-9]+"}) &&
            atoi(str.c_str()) < cameraInfoList.size()) {
            inputIndex = atoi(str.c_str());
            break;
        }
        std::cout
            << "Input invalid! Please enter the index of the camera that you want to connect: ";
    }

    mmind::eye::Camera camera;
    showError(camera.connect(cameraInfoList[inputIndex]));
    std::cout << "Connected to the camera successfully." << std::endl;

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
