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
With this sample, you can acquire the profile data stored in a virtual device, generate the
intensity image and depth map, and save the images.
*/

#include <opencv2/imgcodecs.hpp>
#include <iostream>
#include <thread>
#include <chrono>
#include <mutex>
#include "profiler/VirtualProfiler.h"
#include "profiler/api_util.h"
#include "profiler/parameters/ScanParameters.h"

namespace {
std::mutex kMutex;

// Define the callback function for retrieving the profile data
void callbackFunc(const mmind::eye::ProfileBatch& batch, void* pUser)
{
    std::unique_lock<std::mutex> lock(kMutex);
    auto* outPutBatch = static_cast<mmind::eye::ProfileBatch*>(pUser);
    outPutBatch->append(batch);
}

void saveMap(const mmind::eye::ProfileBatch& batch, int lineCount, int width,
             const std::string& path)
{
    if (batch.isEmpty()) {
        std::cout
            << "The depth map cannot be saved because the batch does not contain any profile data."
            << std::endl;
        return;
    }
    cv::imwrite(path, cv::Mat(lineCount, width, CV_32FC1, batch.getDepthMap().data()));
}

void saveIntensity(const mmind::eye::ProfileBatch& batch, int lineCount, int width,
                   const std::string& path)
{
    if (batch.isEmpty()) {
        std::cout
            << "The intensity cannot be saved because the batch does not contain any profile data."
            << std::endl;
        return;
    }
    cv::imwrite(path, cv::Mat(lineCount, width, CV_8UC1, batch.getIntensityImage().data()));
}
} // namespace

bool acquireProfileDataWithoutCallback(mmind::eye::VirtualProfiler& profiler)
{
    mmind::eye::VirtualUserSet currentUserSet = profiler.currentUserSet();
    int dataPoints = 0;
    // Get the number of data points in each profile
    mmind::eye::showError(currentUserSet.getIntValue(
        mmind::eye::scan_settings::DataPointsPerProfile::name, dataPoints));
    int captureLineCount = 0;
    // Get the value of the "Scan Line Count" parameter
    currentUserSet.getIntValue(mmind::eye::scan_settings::ScanLineCount::name, captureLineCount);

    // Define a ProfileBatch object to store the profile data
    mmind::eye::ProfileBatch profileBatch(dataPoints);

    // Acquire data without using callback
    auto status = profiler.startAcquisition();
    if (!status.isOK()) {
        mmind::eye::showError(status);
        return false;
    }

    while (profileBatch.height() < captureLineCount) {
        // Retrieve the profile data
        mmind::eye::ProfileBatch batch(dataPoints);
        status = profiler.retrieveBatchData(batch);
        if (status.isOK()) {
            if (!profileBatch.append(batch))
                break;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        } else {
            mmind::eye::showError(status);
            break;
        }
    }

    mmind::eye::showError(profiler.stopAcquisition());
    std::cout << "Save the depth map and intensity image." << std::endl;
    saveMap(profileBatch, profileBatch.height(), profileBatch.width(), "DepthMap.tiff");
    saveIntensity(profileBatch, profileBatch.height(), profileBatch.width(), "IntensityImage.png");
    return true;
}

bool acquireProfileDataWithCallback(mmind::eye::VirtualProfiler& profiler)
{
    mmind::eye::VirtualUserSet currentUserSet = profiler.currentUserSet();
    int dataPoints = 0;
    // Get the number of data points in each profile
    mmind::eye::showError(currentUserSet.getIntValue(
        mmind::eye::scan_settings::DataPointsPerProfile::name, dataPoints));
    int captureLineCount = 0;
    // Get the value of the "Scan Line Count" parameter
    currentUserSet.getIntValue(mmind::eye::scan_settings::ScanLineCount::name, captureLineCount);

    // Define a ProfileBatch object to store the profile data
    mmind::eye::ProfileBatch profileBatch(dataPoints);

    // Acquire data with the callback function
    auto status = profiler.registerAcquisitionCallback(callbackFunc, &profileBatch);
    if (!status.isOK()) {
        mmind::eye::showError(status);
        return false;
    }

    // Call startAcquisition() to enter the virtual device into the acquisition ready status
    status = profiler.startAcquisition();
    if (!status.isOK()) {
        mmind::eye::showError(status);
        return false;
    }

    while (true) {
        std::unique_lock<std::mutex> lock(kMutex);
        if (profileBatch.isEmpty()) {
            lock.unlock();
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        } else
            break;
    }

    mmind::eye::showError(profiler.stopAcquisition());
    std::cout << "Save the depth map and intensity image." << std::endl;
    saveMap(profileBatch, profileBatch.height(), profileBatch.width(),
            "DepthMapUsingCallback.tiff");
    saveIntensity(profileBatch, profileBatch.height(), profileBatch.width(),
                  "IntensityImageUsingCallback.png");
    return true;
}

int main()
{
    try {
        mmind::eye::VirtualProfiler profiler("test.mraw");
        if (!acquireProfileDataWithoutCallback(profiler))
            return -1;
        if (!acquireProfileDataWithCallback(profiler))
            return -1;
    } catch (mmind::eye::ErrorStatus error) {
        mmind::eye::showError(error);
        return -1;
    }
}
