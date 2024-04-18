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
With this sample, you can manage user sets, such as obtaining the names of all parameter
groups, adding a user set, switching the user set, and saving parameter settings to
the user set.
*/

#include "profiler/Profiler.h"
#include "profiler/api_util.h"
#include <iostream>

int main()
{
    mmind::eye::Profiler profiler;
    if (!findAndConnect(profiler))
        return -1;

    mmind::eye::UserSetManager& userSetManager = profiler.userSetManager();

    // Obtain the names of all user sets.
    std::vector<std::string> userSets;
    showError(userSetManager.getAllUserSetNames(userSets));

    std::cout << "All user sets: ";
    for (size_t i = 0; i < userSets.size(); i++)
        std::cout << userSets[i] << "  ";
    std::cout << std::endl;

    mmind::eye::UserSet& curSettings = userSetManager.currentUserSet();

    // Obtain the name of the currently selected user set.
    std::string currentName;
    showError(curSettings.getName(currentName));
    std::cout << "The current user set: " << currentName << std::endl;

    // Add a user set.
    const std::string newSetting{"NewSettings"};
    showError(userSetManager.addUserSet(newSetting));
    std::cout << "Add a new user set with the name of \"" << newSetting << "\"." << std::endl;

    // Select a user set by its name.
    showError(userSetManager.selectUserSet(newSetting));
    std::cout << "Select the \"" << newSetting << "\" user set." << std::endl;

    showError(curSettings.saveAllParametersToDevice());
    std::cout << "Save all parameters to the current user set." << std::endl;

    profiler.disconnect();
    std::cout << "Disconnected from the laser profiler successfully." << std::endl;
    return 0;
}
