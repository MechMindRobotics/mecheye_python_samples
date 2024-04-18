# GetCameraIntrinsics Sample

With this sample, you can obtain and print the camera intrinsic parameters.

If you have any questions or have anything to share, feel free to post on the [Mech-Mind Online Community](https://community.mech-mind.com/). The community also contains a [specific category for development with Mech-Eye SDK](https://community.mech-mind.com/c/mech-eye-sdk-development/19).

## Build the Sample

Prerequisites and instructions for building the sample on Windows and Ubuntu are provided.

### Windows

#### Prerequisites

The following software are required to build this sample. Please download and install these software.

* [Mech-Eye SDK (latest version)](https://downloads.mech-mind.com/?tab=tab-sdk)
* [Visual Studio (version 2017 or above)](https://visualstudio.microsoft.com/vs/community/)
* [CMake (version 3.2 or above)](https://cmake.org/download/)

#### Instructions

1. Make sure that the sample is stored in a location with read and write permissions.
2. Run Cmake and set the source and build paths:

   | Field                       | Path                          |
   | :----                       | :----                         |
   | Where is the source code    | xxx/GetCameraIntrinsics       |
   | Where to build the binaries | xxx/GetCameraIntrinsics/build |

3. Click the **Configure** button. In the pop-up window, set the generator and platform according to the actual situation, and then click the **Finish** button.
4. When the log displays **Configuring done**, click the **Generate** button. When the log displays **Generating done**, click the **Open Project** button.
5. In Visual Studio toolbar, change the solution configuration from **Debug** to **Release**.
6. In the **Solution Explorer** panel, right-click the sample, and select **Set as Startup Project**.
7. Click the **Local Windows Debugger** button in the toolbar to run the sample.
8. Enter the index of the camera to which you want to connect, and press the Enter key. The obtained files are saved to the `build` folder.

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

#### Instructions

1. Navigate to the directory of the sample.

   ```bash
   cd xxx/area_scan_3d_camera/Util/GetCameraIntrinsics/
   ```

2. Configure and build the sample.

   ```bash
   sudo mkdir build && cd build
   sudo cmake ..
   sudo make
   ```

3. Run the sample.

   ```bash
   sudo ./GetCameraIntrinsics
   ```

4. Enter the index of the camera to which you want to connect, and press the Enter key.
