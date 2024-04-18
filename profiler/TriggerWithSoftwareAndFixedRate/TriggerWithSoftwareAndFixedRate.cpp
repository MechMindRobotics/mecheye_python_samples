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
With this sample, you can acquire the profile data triggered with software in a fixed rate, generate
and save the intensity image, depth map, and point cloud.
*/

#include <opencv2/imgcodecs.hpp>
#include <iostream>
#include <fstream>
#include <thread>
#include <regex>
#include <cstdio>
#include <cmath>
#include <chrono>
#include <mutex>
#include "profiler/Profiler.h"
#include "profiler/api_util.h"
#include "profiler/parameters/ProfileProcessingParameters.h"
#include "profiler/parameters/ProfileExtractionParameters.h"
#include "profiler/parameters/RawImageParameters.h"
#include "profiler/parameters/ScanParameters.h"

namespace {
std::mutex kMutex;
constexpr double kPitch = 1e-3;
constexpr long long kInitEncoderValue = 0x0FFFFFFF;

void setTimedExposure(mmind::eye::UserSet& userSet, int exposureTime)
{
    // Set the "Exposure Mode" parameter to "Timed"
    showError(userSet.setEnumValue(
        mmind::eye::brightness_settings::ExposureMode::name,
        static_cast<int>(mmind::eye::brightness_settings::ExposureMode::Value::Timed)));

    // Set the "Exposure Time" parameter to {exposureTime} μs
    showError(
        userSet.setIntValue(mmind::eye::brightness_settings::ExposureTime::name, exposureTime));
}

void setHDRExposure(mmind::eye::UserSet& userSet, int exposureTime, double proportion1,
                    double proportion2, double firstThreshold, double secondThreshold)
{
    // Set the "Exposure Mode" parameter to "HDR"
    showError(userSet.setEnumValue(
        mmind::eye::brightness_settings::ExposureMode::name,
        static_cast<int>(mmind::eye::brightness_settings::ExposureMode::Value::HDR)));

    // Set the total exposure time to {exposureTime} μs
    showError(
        userSet.setIntValue(mmind::eye::brightness_settings::ExposureTime::name, exposureTime));

    // Set the proportion of the first exposure phase to {proportion1}%
    showError(userSet.setFloatValue(
        mmind::eye::brightness_settings::HdrExposureTimeProportion1::name, proportion1));

    // Set the proportion of the first + second exposure phases to {proportion2}% (that is, the
    // second exposure phase occupies {proportion2 - proportion1}%, and the third exposure phase
    // occupies {100 - proportion2}% of the total exposure time)
    showError(userSet.setFloatValue(
        mmind::eye::brightness_settings::HdrExposureTimeProportion2::name, proportion2));

    // Set the first threshold to {firstThreshold}. This limits the maximum grayscale value to
    // {firstThreshold} after the first exposure phase is completed.
    showError(userSet.setFloatValue(mmind::eye::brightness_settings::HdrFirstThreshold::name,
                                    firstThreshold));

    // Set the second threshold to {secondThreshold}. This limits the maximum grayscale value to
    // {secondThreshold} after the second exposure phase is completed.
    showError(userSet.setFloatValue(mmind::eye::brightness_settings::HdrSecondThreshold::name,
                                    secondThreshold));
}

void setParameters(mmind::eye::UserSet& userSet)
{
    // Set the "Exposure Mode" parameter to "Timed"
    // Set the "Exposure Time" parameter to 100 μs
    setTimedExposure(userSet, 100);

    /*You can also use the HDR exposure mode, in which the laser profiler exposes in three phases
    while acquiring one profile. In this mode, you need to set the total exposure time, the
    proportions of the three exposure phases, as well as the two thresholds of grayscale values. The
    code for setting the relevant parameters for the HDR exposure mode is given in the following
    comments.*/
    // // Set the "Exposure Mode" parameter to "HDR"
    // // Set the total exposure time to 100 μs
    // // Set the proportion of the first exposure phase to 40%
    // // Set the proportion of the first + second exposure phases to 80% (that is, the second
    // // exposure phase occupies 40%, and the third exposure phase occupies 20% of the total
    // // exposure
    // // Set the first threshold to 10. This limits the maximum grayscale value to 10 after the
    // // first exposure phase is completed.
    // // Set the second threshold to 60. This limits the maximum grayscale value to 60 after the
    // // second exposure phase is completed.
    // setHDRExposure(userSet, 100, 40, 80, 10, 60);

    // Set the "Data Acquisition Trigger Source" parameter to "Software"
    showError(userSet.setEnumValue(
        mmind::eye::trigger_settings::DataAcquisitionTriggerSource::name,
        static_cast<int>(
            mmind::eye::trigger_settings::DataAcquisitionTriggerSource::Value::Software)));

    // Set the "Line Scan Trigger Source" parameter to "Fixed rate"
    showError(userSet.setEnumValue(
        mmind::eye::trigger_settings::LineScanTriggerSource::name,
        static_cast<int>(mmind::eye::trigger_settings::LineScanTriggerSource::Value::FixedRate)));
    // Set the "Software Trigger Rate" to 1000 Hz
    showError(userSet.setFloatValue(mmind::eye::trigger_settings::SoftwareTriggerRate::name, 1000));

    // Set the "Scan Line Count" parameter (the number of lines to be scanned) to 1600
    showError(userSet.setIntValue(mmind::eye::scan_settings::ScanLineCount::name, 1600));

    // Set the "Laser Power" parameter to 100
    showError(userSet.setIntValue(mmind::eye::brightness_settings::LaserPower::name, 100));
    // Set the "Analog Gain" parameter to "Gain_2"
    showError(userSet.setEnumValue(
        mmind::eye::brightness_settings::AnalogGain::name,
        static_cast<int>(mmind::eye::brightness_settings::AnalogGain::Value::Gain_2)));
    // Set the "Digital Gain" parameter to 0
    showError(userSet.setIntValue(mmind::eye::brightness_settings::DigitalGain::name, 0));

    // Set the "Minimum Grayscale Value" parameter to 50
    showError(userSet.setIntValue(mmind::eye::profile_extraction::MinGrayscaleValue::name, 50));
    // Set the "Minimum Laser Line Width" parameter to 2
    showError(userSet.setIntValue(mmind::eye::profile_extraction::MinLaserLineWidth::name, 2));
    // Set the "Maximum Laser Line Width" parameter to 20
    showError(userSet.setIntValue(mmind::eye::profile_extraction::MaxLaserLineWidth::name, 20));
    // Set the "Spot Selection" parameter to "Strongest"
    showError(userSet.setEnumValue(
        mmind::eye::profile_extraction::SpotSelection::name,
        static_cast<int>(mmind::eye::profile_extraction::SpotSelection::Value::Strongest)));

    // This parameter is only effective for firmware 2.2.1 and below. For firmware 2.3.0 and above,
    // adjustment of this parameter does not take effect.
    // Set the "Minimum Spot Intensity" parameter to 51
    showError(userSet.setIntValue(mmind::eye::profile_extraction::MinSpotIntensity::name, 51));
    // This parameter is only effective for firmware 2.2.1 and below. For firmware 2.3.0 and above,
    // adjustment of this parameter does not take effect.
    // Set the "Maximum Spot Intensity" parameter to 205
    showError(userSet.setIntValue(mmind::eye::profile_extraction::MaxSpotIntensity::name, 205));

    /* Set the "Gap Filling" parameter to 16, which controls the size of the gaps that can be filled
     * in the profile. When the number of consecutive data points in a gap in the profile is no
     * greater than 16, this gap will be filled. */
    showError(userSet.setIntValue(mmind::eye::profile_processing::GapFilling::name, 16));
    /* Set the "Filter" parameter to "Mean". The "Mean Filter Window Size" parameter needs to be set
     * as well. This parameter controls the window size of mean filter. If the "Filter" parameter is
     * set to "Median", the "Median Filter Window Size" parameter needs to be set. This parameter
     * controls the window size of median filter.*/
    showError(userSet.setEnumValue(
        mmind::eye::profile_processing::Filter::name,
        static_cast<int>(mmind::eye::profile_processing::Filter::Value::Mean)));
    // Set the "Mean Filter Window Size" parameter to 2
    showError(userSet.setEnumValue(
        mmind::eye::profile_processing::MeanFilterWindowSize::name,
        static_cast<int>(
            mmind::eye::profile_processing::MeanFilterWindowSize::Value::WindowSize_2)));
}

bool acquireProfileData(mmind::eye::Profiler& profiler, mmind::eye::ProfileBatch& totalBatch,
                        int captureLineCount, int dataWidth, bool isSoftwareTrigger)
{
    /* Call startAcquisition() to enter the laser profiler into the acquisition ready status, and
    then call triggerSoftware() to start the data acquisition (triggered by software).*/
    std::cout << "Start data acquisition." << std::endl;
    auto status = profiler.startAcquisition();
    if (!status.isOK()) {
        showError(status);
        return false;
    }

    if (isSoftwareTrigger) {
        status = profiler.triggerSoftware();
        if (!status.isOK()) {
            showError(status);
            return false;
        }
    }

    totalBatch.clear();
    totalBatch.reserve(captureLineCount);
    while (totalBatch.height() < captureLineCount) {
        // Retrieve the profile data
        mmind::eye::ProfileBatch batch(dataWidth);
        status = profiler.retrieveBatchData(batch);
        if (status.isOK()) {
            if (!totalBatch.append(batch))
                break;
            std::this_thread::sleep_for(std::chrono::milliseconds(200));
        } else {
            showError(status);
            return false;
        }
    }

    std::cout << "Stop data acquisition." << std::endl;
    status = profiler.stopAcquisition();
    if (!status.isOK())
        showError(status);
    return status.isOK();
}

// Define the callback function for retrieving the profile data
void callbackFunc(const mmind::eye::ProfileBatch& batch, void* pUser)
{
    std::unique_lock<std::mutex> lock(kMutex);
    auto* outPutBatch = static_cast<mmind::eye::ProfileBatch*>(pUser);
    outPutBatch->append(batch);
}

bool acquireProfileDataUsingCallback(mmind::eye::Profiler& profiler,
                                     mmind::eye::ProfileBatch& profileBatch, bool isSoftwareTrigger)
{
    profileBatch.clear();

    // Set a large CallbackRetrievalTimeout
    showError(profiler.currentUserSet().setIntValue(
        mmind::eye::scan_settings::CallbackRetrievalTimeout::name, 60000));

    // Register the callback function
    auto status = profiler.registerAcquisitionCallback(callbackFunc, &profileBatch);
    if (!status.isOK()) {
        showError(status);
        return false;
    }

    // Call the startAcquisition to take the laser profiler into the acquisition ready status
    std::cout << "Start data acquisition." << std::endl;
    status = profiler.startAcquisition();
    if (!status.isOK()) {
        showError(status);
        return false;
    }

    // Call the triggerSoftware() to start the data acquisition
    if (isSoftwareTrigger) {
        status = profiler.triggerSoftware();
        if (!status.isOK()) {
            showError(status);
            return false;
        }
    }

    while (true) {
        std::unique_lock<std::mutex> lock(kMutex);
        if (profileBatch.isEmpty()) {
            lock.unlock();
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        } else
            break;
    }

    std::cout << "Stop data acquisition." << std::endl;
    status = profiler.stopAcquisition();
    if (!status.isOK())
        showError(status);
    return status.isOK();
}

void saveDepthMap(const mmind::eye::ProfileBatch& batch, int lineCount, int width,
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

void saveIntensityImage(const mmind::eye::ProfileBatch& batch, int lineCount, int width,
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

int shiftEncoderValsAroundZero(unsigned int oriVal, long long initValue = kInitEncoderValue)
{
    return static_cast<int>(oriVal - initValue);
}

bool saveDataToPly(float* data, int* yValues, int captureLineCount, int dataWidth, float xUnit,
                   float yUnit, const std::string& fileName, bool isOrganized)
{
    FILE* fp = fopen(fileName.c_str(), "w");

    if (!fp)
        return false;

    unsigned validPointCount{0};
    if (!isOrganized) {
        for (int y = 0; y < captureLineCount; ++y) {
            for (int x = 0; x < dataWidth; ++x) {
                if (!std::isnan(data[y * dataWidth + x]))
                    validPointCount++;
            }
        }
    }

    fprintf(fp, "ply\n");
    fprintf(fp, "format ascii 1.0\n");
    fprintf(fp, "comment File generated\n");
    fprintf(fp, "comment x y z data unit in mm\n");
    fprintf(fp, "element vertex %u\n",
            isOrganized ? static_cast<unsigned>(captureLineCount * dataWidth) : validPointCount);
    fprintf(fp, "property float x\n");
    fprintf(fp, "property float y\n");
    fprintf(fp, "property float z\n");
    fprintf(fp, "end_header\n");

    for (int y = 0; y < captureLineCount; ++y) {
        for (int x = 0; x < dataWidth; ++x) {
            if (!std::isnan(data[y * dataWidth + x]))
                fprintf(fp, "%f %f %f\n", static_cast<float>(x * xUnit * kPitch),
                        static_cast<float>(yValues[y] * yUnit * kPitch), data[y * dataWidth + x]);
            else if (isOrganized)
                fprintf(fp, "nan nan nan\n");
        }
    }

    fclose(fp);
    return true;
}

bool saveDataToCsv(float* data, int* yValues, int captureLineCount, int dataWidth, float xUnit,
                   float yUnit, const std::string& fileName, bool isOrganized)
{
    FILE* fp = fopen(fileName.c_str(), "w");

    if (!fp)
        return false;

    fprintf(fp, "X,Y,Z\n");

    for (int y = 0; y < captureLineCount; ++y) {
        for (int x = 0; x < dataWidth; ++x) {
            if (!std::isnan(data[y * dataWidth + x]))
                fprintf(fp, "%f,%f,%f\n", static_cast<float>(x * xUnit * kPitch),
                        static_cast<float>(yValues[y] * yUnit * kPitch), data[y * dataWidth + x]);
            else if (isOrganized)
                fprintf(fp, "nan,nan,nan\n");
        }
    }

    fclose(fp);
    return true;
}

void savePointCloud(const mmind::eye::ProfileBatch& batch, const mmind::eye::UserSet& userSet,
                    bool savePLY = true, bool saveCSV = true, bool isOrganized = true)
{
    if (batch.isEmpty())
        return;

    // Get the X-axis resolution
    double xUnit = 0.0;
    showError(
        userSet.getFloatValue(mmind::eye::point_cloud_resolutions::XAxisResolution::name, xUnit));

    // Get the Y resolution
    double yUnit;
    showError(userSet.getFloatValue(mmind::eye::point_cloud_resolutions::YResolution::name, yUnit));
    // // Uncomment the following lines for custom Y Unit
    // // Prompt to enter the desired encoder resolution, which is the travel distance corresponding
    // // to
    // // one quadrature signal.
    // std::cout << "Please enter the desired encoder resolution (integer, unit: μm, min: "
    //  "1, max: 65535): ";
    // while (true) {
    //     std::string str;
    //     std::cin >> str;
    //     if (std::regex_match(str.begin(), str.end(), std::regex{"[0-9]+"})) {
    //         yUnit = atoi(str.c_str());
    //         break;
    //     }
    //     std::cout << "Input invalid! Please enter the desired encoder resolution (integer, unit:
    //     "
    //                  "μm, min: 1, max: 65535): ";
    // }

    int lineScanTriggerSource{};
    showError(userSet.getEnumValue(mmind::eye::trigger_settings::LineScanTriggerSource::name,
                                   lineScanTriggerSource));
    bool useEncoderValues =
        lineScanTriggerSource ==
        static_cast<int>(mmind::eye::trigger_settings::LineScanTriggerSource::Value::Encoder);

    // Shift the encoder values around zero
    std::vector<int> encoderVals;
    encoderVals.reserve(batch.height());
    auto encoder = batch.getEncoderArray();
    for (int r = 0; r < batch.height(); ++r)
        encoderVals.push_back(useEncoderValues ? shiftEncoderValsAroundZero(encoder[r], encoder[0])
                                               : r);

    std::cout << "Save the point cloud." << std::endl;
    if (saveCSV)
        saveDataToCsv(batch.getDepthMap().data(), encoderVals.data(), batch.height(), batch.width(),
                      xUnit, yUnit, "PointCloud.csv", isOrganized);
    if (savePLY)
        saveDataToPly(batch.getDepthMap().data(), encoderVals.data(), batch.height(), batch.width(),
                      xUnit, yUnit, "PointCloud.ply", isOrganized);
}
} // namespace

int main()
{
    mmind::eye::Profiler profiler;
    if (!findAndConnect(profiler))
        return -1;

    if (!confirmCapture()) {
        profiler.disconnect();
        return -1;
    }

    mmind::eye::UserSet userSet = profiler.currentUserSet();

    // Set the parameters
    setParameters(userSet);

    int dataWidth = 0;
    // Get the number of data points in each profile
    showError(
        userSet.getIntValue(mmind::eye::scan_settings::DataPointsPerProfile::name, dataWidth));
    int captureLineCount = 0;
    // Get the current value of the "Scan Line Count" parameter
    userSet.getIntValue(mmind::eye::scan_settings::ScanLineCount::name, captureLineCount);

    // Define a ProfileBatch object to store the profile data
    mmind::eye::ProfileBatch profileBatch(dataWidth);

    int dataAcquisitionTriggerSource{};
    showError(userSet.getEnumValue(mmind::eye::trigger_settings::DataAcquisitionTriggerSource::name,
                                   dataAcquisitionTriggerSource));
    bool isSoftwareTrigger =
        dataAcquisitionTriggerSource ==
        static_cast<int>(
            mmind::eye::trigger_settings::DataAcquisitionTriggerSource::Value::Software);

    // Acquire profile data without using callback
    if (!acquireProfileData(profiler, profileBatch, captureLineCount, dataWidth, isSoftwareTrigger))
        return -1;

    // // Acquire profile data using callback
    // if (!acquireProfileDataUsingCallback(profiler, profileBatch, isSoftwareTrigger))
    // return -1;

    std::cout << "Save the depth map and intensity image." << std::endl;
    saveDepthMap(profileBatch, captureLineCount, dataWidth, "DepthMap.tiff");
    saveIntensityImage(profileBatch, captureLineCount, dataWidth, "IntensityImage.png");
    savePointCloud(profileBatch, userSet);

    // Uncomment the following line to save a virtual device file using the ProfileBatch profileBatch
    // acquired.
    // profiler.saveVirtualDeviceFile(profileBatch, "test.mraw");

    // Disconnect from the laser profiler
    profiler.disconnect();
    return 0;
}
