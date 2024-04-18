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
With this sample, you can set the parameters specific to laser cameras (the DEEP and LSR series).
*/

#include "area_scan_3d_camera/Camera.h"
#include "area_scan_3d_camera/parameters/Laser.h"
#include "area_scan_3d_camera/api_util.h"

int main()
{
    mmind::eye::Camera camera;
    if (!findAndConnect(camera))
        return -1;

    mmind::eye::UserSet& currentUserSet = camera.currentUserSet();

    // Set the "Laser Power" parameter, which is the output power of the projector as a percentage of the maximum output power. This affects the
    // intensity of the projected structured light.

    const int laserPowerLevel = 80;
    std::cout << "Set the output power of the laser projector to: " << laserPowerLevel
              << " percent of the maximum output power." << std::endl;
    showError(
        currentUserSet.setIntValue(mmind::eye::laser_setting::PowerLevel::name, laserPowerLevel));

    // Set the "Fringe Coding Mode" parameter, which controls the pattern of the structured light. The "Fast" mode enhances the 
    // capture speed but provides lower depth data accuracy. The "Accurate" mode provides better depth data accuracy but reduces the capture speed.

    std::cout << "Set the fringe coding mode of the projector to \"Accurate\"." << std::endl;
    const mmind::eye::laser_setting::FringeCodingMode::Value laserFringeCodingMode =
        mmind::eye::laser_setting::FringeCodingMode::Value::Accurate;

    showError(currentUserSet.setEnumValue(mmind::eye::laser_setting::FringeCodingMode::name,
                                          static_cast<int>(laserFringeCodingMode)));

    // Set the laser scan range. The entire projector FOV is from 0 to 100.
    const mmind::eye::Range<int> laserFrameRange{20, 80};
    std::cout << "Set the laser scan range from " << laserFrameRange.min << " to "
              << laserFrameRange.max << "." << std::endl;
    showError(
        currentUserSet.setRangeValue(mmind::eye::laser_setting::FrameRange::name, laserFrameRange));

    // Set the laser scan partition count. If the set value is greater than 1, the scan of the entire FOV 
    // will be partitioned into multiple parts. It is recommended to use multiple parts for
    // extremely dark objects.
    const int laserFramePartitionCount = 2;
    std::cout << "Set the laser scan partition count to " << laserFramePartitionCount << "."
              << std::endl;
    showError(currentUserSet.setIntValue(mmind::eye::laser_setting::FramePartitionCount::name,
                                         laserFramePartitionCount));

    camera.disconnect();
    std::cout << "Disconnected from the camera successfully." << std::endl;
    return 0;
}
