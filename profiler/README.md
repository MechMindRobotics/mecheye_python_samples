# C++ Samples for Mech-Eye 3D Laser Profiler

This documentation provides descriptions of Mech-Eye API C++ samples for Mech-Eye 3D Laser Profiler and instructions for building all the samples at once.

If you have any questions or have anything to share, feel free to post on the [Mech-Mind Online Community](https://community.mech-mind.com/). The community also contains a [specific category for development with Mech-Eye SDK](https://community.mech-mind.com/c/mech-eye-sdk-development/19).

## Sample List

Currently, the following samples are provided.

The samples marked with `(OpenCV)` require [OpenCV](https://opencv.org/releases/) to be installed.  

* [TriggerWithSoftwareAndFixedRate](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/profiler/TriggerWithSoftwareAndFixedRate) `(OpenCV)`  
  Trigger data acquisition with signals input from software, trigger line scans at a fixed rate, and then retrieve and save the acquired data.
* [TriggerWithExternalDeviceAndFixedRate](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/profiler/TriggerWithExternalDeviceAndFixedRate) `(OpenCV)`  
  Trigger data acquisition with signals input from the external device, trigger line scans at a fixed rate, and then retrieve and save the acquired data.
* [TriggerWithSoftwareAndEncoder](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/profiler/TriggerWithSoftwareAndEncoder) `(OpenCV)`  
  Trigger data acquisition with signals input from software, trigger line scans with signals input from the encoder, and then retrieve and save the acquired data.
* [TriggerWithExternalDeviceAndEncoder](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/profiler/TriggerWithExternalDeviceAndEncoder) `(OpenCV)`  
  Trigger data acquisition with signals input from the external device, trigger line scans with signals input from the encoder, and then retrieve and save the acquired data.
* [TriggerMultipleProfilersSimultaneously](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/profiler/TriggerMultipleProfilersSimultaneously) `(OpenCV)`  
  Trigger multiple laser profilers to acquire data asynchronously and retrieve the acquired data.
* [ManageUserSets](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/profiler/ManageUserSets)  
  Manage parameter groups, such as obtaining the names of all parameter groups, adding a parameter group, switching the parameter group, and saving parameter settings to the parameter group.
* [RegisterProfilerEvent](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/profiler/RegisterProfilerEvent)  
Define and register the callback function for monitoring the laser profiler connection status.
* [UseVirtualDevice](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/profiler/UseVirtualDevice) `(OpenCV)`  
Acquire the profile data stored in a virtual device, generate the intensity image and depth map, and save the images.

## Build the Samples

The instructions provided here allow you to build all the samples at once.

### Windows

#### Prerequisites

Please download and install the required software listed below.

* [Mech-Eye SDK (latest version)](https://downloads.mech-mind.com/?tab=tab-sdk)
* [Visual Studio (version 2017 or above)](https://visualstudio.microsoft.com/vs/community/)
* [CMake (version 3.2 or above)](https://cmake.org/download/)

Optional software: If you need to build the samples dependent on third-party software (refer to the Sample List above), please install the corresponding software.

* [OpenCV (version 3.4.5 or above)](https://opencv.org/releases/)

#### Instructions

1. Make sure that the samples are stored in a location with read and write permissions.
2. If OpenCV is installed, add the following directories to the **Path** environment variable:

   * `xxx/opencv/build/x64/vc14/bin`
   * `xxx/opencv/build/x64/vc14/lib`

3. (Optional) Disable unneeded samples: if OpenCV is installed, this step must be performed.

   Open the CMakeLists file in `xxx/profiler`, and change **ON** to **OFF** in the line that starts with `option(USE_OPENCV`.

4. Run Cmake and set the source and build paths:

   | Field                       | Path                 |
   | :----                       | :----                |
   | Where is the source code    | xxx/profiler         |
   | Where to build the binaries | xxx/profiler/build   |

5. Click the **Configure** button. In the pop-up window, set the generator and platform according to the actual situation, and then click the **Finish** button.
6. When the log displays **Configuring done**, click the **Generate** button. When the log displays **Generating done**, click the **Open Project** button.
7. In Visual Studio toolbar, change the solution configuration from **Debug** to **Release**.
8. In the menu bar, select **Build** > **Build Solution**. An EXE format executable file is generated for each sample. The executable files are saved to the `Release` folder, located in the **Where to build the binaries** directory.
9. In the **Solution Explorer** panel, right-click a sample, and select **Set as Startup Project**.
10. Click the **Local Windows Debugger** button in the toolbar to run the sample.
11. Enter the index of the camera to which you want to connect, and press the Enter key. The obtained files are saved to the `Release` folder.

### Ubuntu

Ubuntu 18 or above is required.

#### Prerequisites

* Update the software source list.

  ```bash
  sudo apt-get update
  ```

* Check your gcc and g++ version

   ```bash
   gcc --version
   g++ --version
   ```

* If your gcc or g++ version is below 9.4.0, please upgrade them to 9.4.0 or above

   ```bash
   sudo apt-get install -y software-properties-common
   sudo add-apt-repository ppa:ubuntu-toolchain-r/test
   sudo apt-get update
   sudo apt-get install -y gcc-9 g++-9
   sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 60
   sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 60
   ```

* Install required tools.
  
  ```bash
  sudo apt-get install -y build-essential pkg-config cmake
  ```

* Install [Mech-Eye SDK (latest version)](https://downloads.mech-mind.com/?tab=tab-sdk).

  >Note: If you have installed Mech-Eye SDK before, please uninstall it first with the following command:
  >
  >```bash
  >sudo dpkg -P MechEyeApi
  >```
  
  * If the system architecture is AMD64, execute the following command:

    ```bash
    sudo dpkg -i 'Mech-Eye_API_x.x.x_amd64.deb'
    ```

  * If the system architecture is ARM64, execute the following command:

    ```bash
    sudo dpkg -i 'Mech-Eye_API_x.x.x_arm64.deb'
    ```

* Install optional third-party libraries: If you need to build the samples dependent on third-party software (refer to the Sample List above), please install the corresponding software.

  * Install OpenCV (latest version):

    ```bash
    sudo apt update && sudo apt install -y unzip
    wget -O opencv.zip https://github.com/opencv/opencv/archive/4.x.zip
    unzip opencv.zip
    mkdir build && cd build
    cmake ../opencv-4.x
    cmake --build .
    sudo make install
    ```

#### Instructions

1. Navigate to the directory of the sample.

   ```bash
   cd xxx/profiler/
   ```

2. (Optional) Disable unneeded samples: if any of the optional software is not installed, this step must be performed.

   Open the CMakeLists file in `xxx/profiler/`, and change **ON** to **OFF** in the options of the unneeded samples.

3. Configure and build the samples.

   ```bash
   sudo mkdir build && cd build
   sudo cmake ..
   sudo make
   ```

4. Run a sample. Replace `SampleName` with the name of the sample that you want to run.

   ```bash
   sudo ./SampleName
   ```

5. Enter the index of the camera to which you want to connect, and press the Enter key. The obtained files are saved to `xxx/profiler/build`.

## License

Mech-Eye Samples are distributed under the [BSD license](https://github.com/MechMindRobotics/mecheye_cpp_samples/blob/master/LICENSE).
