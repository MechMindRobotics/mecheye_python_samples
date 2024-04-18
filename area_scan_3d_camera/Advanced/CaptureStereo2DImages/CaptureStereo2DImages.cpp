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
With this sample, you can obtain and save the stereo 2D images.
*/

#include <opencv2/highgui.hpp>
#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/api_util.h"

int main()
{
    mmind::eye::Camera camera;
    if (!findAndConnect(camera))
        return -1;

    mmind::eye::Frame2D stereoLeft, stereoRight;
    auto errorStatus = camera.captureStereo2D(stereoLeft, stereoRight, false);
    if (!errorStatus.isOK()) {
        showError(errorStatus);
        return -1;
    }

    cv::Mat cvMatLeft, cvMatRight;

    switch (stereoLeft.colorType()) {
    case mmind::eye::ColorTypeOf2DCamera::Monochrome:
    {
        mmind::eye::GrayScale2DImage grayImageLeft = stereoLeft.getGrayScaleImage();
        cvMatLeft =
            cv::Mat(grayImageLeft.height(), grayImageLeft.width(), CV_8UC1, grayImageLeft.data());

        mmind::eye::GrayScale2DImage grayImageRight = stereoRight.getGrayScaleImage();
        cvMatRight = cv::Mat(grayImageRight.height(), grayImageRight.width(), CV_8UC1,
                             grayImageRight.data());
        break;
    }
    case mmind::eye::ColorTypeOf2DCamera::Color:
    {
        mmind::eye::Color2DImage colorImageLeft = stereoLeft.getColorImage();
        cvMatLeft = cv::Mat(colorImageLeft.height(), colorImageLeft.width(), CV_8UC3,
                            colorImageLeft.data());

        mmind::eye::Color2DImage colorImageRight = stereoRight.getColorImage();
        cvMatRight = cv::Mat(colorImageRight.height(), colorImageRight.width(), CV_8UC3,
                             colorImageRight.data());
        break;
    }
    default:
        break;
    }

    const std::string imageFileLeft = "stereo2D_left.png";
    const std::string imageFileRight = "stereo2D_right.png";
    // cv::imshow(imageFileLeft, cvMatLeft);
    // cv::imshow(imageFileRight, cvMatRight);

    cv::imwrite(imageFileLeft, cvMatLeft);
    cv::imwrite(imageFileRight, cvMatRight);
    std::cout << "Capture and save the stereo 2D image: " << imageFileLeft << " and "
              << imageFileRight << std::endl;
    // cv::waitKey(0);

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
