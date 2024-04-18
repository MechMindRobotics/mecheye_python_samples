# C++ Samples for Mech-Eye Industrial 3D Camera

This documentation provides descriptions of Mech-Eye API C++ samples for Mech-Eye Industrial 3D Camera and instructions for building all the samples at once.

If you have any questions or have anything to share, feel free to post on the [Mech-Mind Online Community](https://community.mech-mind.com/). The community also contains a [specific category for development with Mech-Eye SDK](https://community.mech-mind.com/c/mech-eye-sdk-development/19).

## Sample List

Samples are divided into the following categories: **Basic**, **Advanced**, **Util**, **Calibration**, **Pcl**, and **Halcon**.

* **Basic** samples: Connect to the camera and acquire data.
* **Advanced** samples: Acquire data in more complicated manners and set model-specific parameters.
* **Util** samples: Obtain camera information and set common parameters.
* **Calibration** samples: perform hand-eye calibration through {product-eye-api}.
* **Pcl** samples: Use the PCL library to convert data structure and visualize data.
* **Halcon** samples: Obtain HALCON-readable point clouds through {product-eye-api}.

The samples marked with `(OpenCV)` require [OpenCV](https://opencv.org/releases/) to be installed.  
The samples marked with `(PCL)` require [PCL](https://github.com/PointCloudLibrary/pcl/releases) to be installed.  
The sample marked with `(HALCON)` requires [HALCON](https://www.mvtec.com/downloads) to be installed.

* **Basic**
  * [ConnectToCamera](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Basic/ConnectToCamera)  
    Connect to a camera.
  * [ConnectAndCaptureImages](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Basic/ConnectAndCaptureImages)  
    Connect to a camera and obtain the 2D image, depth map, and point cloud data.
  * [Capture2DImage](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Basic/Capture2DImage) `(OpenCV)`  
    Obtain and save the 2D image.
  * [CaptureDepthMap](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Basic/CaptureDepthMap) `(OpenCV)`  
    Obtain and save the depth map.
  * [CapturePointCloud](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Basic/CapturePointCloud)  
    Obtain and save the untextured and textured point clouds.
  * [CapturePointCloudHDR](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Basic/CapturePointCloudHDR)  
    Set multiple exposure times, and then obtain and save the point cloud.
  * [CapturePointCloudWithNormals](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Basic/CapturePointCloudWithNormals)  
    Calculate normals and save the point cloud with normals.
* **Advanced**
  * [ConvertDepthMapToPointCloud](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Advanced/ConvertDepthMapToPointCloud)  
    Generate a point cloud from the depth map and save the point cloud.
  * [MultipleCamerasCaptureSequentially](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Advanced/MultipleCamerasCaptureSequentially) `(OpenCV)`  
    Obtain and save 2D images, depth maps, and point clouds sequentially from multiple cameras.
  * [MultipleCamerasCaptureSimultaneously](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Advanced/MultipleCamerasCaptureSimultaneously) `(OpenCV)`  
    Obtain and save 2D images, depth maps, and point clouds simultaneously from multiple cameras.
  * [CapturePeriodically](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Advanced/CapturePeriodically) `(OpenCV)`  
    Obtain and save 2D images, depth maps, and point clouds periodically for the specified duration from a camera.
  * [Mapping2DImageToDepthMap](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Advanced/Mapping2DImageToDepthMap)  
    Generate untextured and textured point clouds from a masked 2D image and a depth map.
  * [SetParametersOfLaserCameras](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Advanced/SetParametersOfLaserCameras)  
    Set the parameters specific to laser cameras (the DEEP and LSR series).
  * [SetParametersOfUHPCameras](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Advanced/SetParametersOfUHPCameras)  
    Set the parameters specific to the UHP series.
  * [RegisterCameraEvent](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Advanced/RegisterCameraEvent)  
    Define and register the callback function for monitoring the camera connection status.
  * [CaptureStereo2DImages](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Advanced/CaptureStereo2DImages) `(OpenCV)`  
    Obtain and save the 2D images from both 2D cameras.
    > Note: This sample is only applicable to the following models: Deep, Laser L Enhanced, PRO XS, LSR L, LSR S, and DEEP.
* **Util**
  * [GetCameraIntrinsics](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Util/GetCameraIntrinsics)  
    Obtain and print the camera intrinsic parameters.
  * [PrintCameraInfo](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Util/PrintCameraInfo)  
    Obtain and print the camera information, such as model, serial number, firmware version, and temperatures.
  * [SetScanningParameters](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Util/SetScanningParameters)  
    Set the parameters in the **3D Parameters**, **2D Parameters**, and **ROI** categories.
  * [SetDepthRange](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Util/SetDepthRange)  
    Set the **Depth Range** parameter.
  * [SetPointCloudProcessingParameters](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Util/SetPointCloudProcessingParameters)  
    Set the **Point Cloud Processing** parameters.
  * [ManageUserSets](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Util/ManageUserSets)  
    Manage parameter groups, such as obtaining the names of all parameter groups, adding a parameter group, switching the parameter group, and saving parameter settings to the parameter group.
  * [SaveAndLoadUserSet](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Util/SaveAndLoadUserSet)  
    Import and replace all parameter groups from a JSON file, and save all parameter groups to a JSON file.
* **Calibration**
  * [HandEyeCalibration](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Calibration/HandEyeCalibration) `(OpenCV)`  
   Perform hand-eye calibration.
* **Pcl**
  * [ConvertPointCloudToPcl](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Pcl/ConvertPointCloudToPCL) `(PCL)`  
    Obtain the point cloud data from the camera and convert it to the PCL data structure.
  * [ConvertPointCloudWithNormalsToPcl](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Pcl/ConvertPointCloudWithNormalsToPCL) `(PCL)`  
    Obtain the point cloud data with normals from the camera and convert it to the PCL data structure.
* **Halcon**
  * [ConvertPointCloudToObjectModel3D](https://github.com/MechMindRobotics/mecheye_cpp_samples/tree/master/area_scan_3d_camera/Halcon/ConvertPointCloudToObjectModel3D) `(HALCON)`  
    Obtain the point cloud data from a camera, and then transform and save the point clouds using the HALCON C++ interface.
    > Note: This sample is not available for platforms based on the ARM64 architecture.

## Build the Samples

The instructions provided here allow you to build all the samples at once.

### Windows

#### Prerequisites

Please download and install the required software listed below.

* [Mech-Eye SDK (latest version)](https://downloads.mech-mind.com/?tab=tab-sdk)
* [Visual Studio (version 2017 or above)](https://visualstudio.microsoft.com/vs/community/)
* [CMake (version 3.2 or above)](https://cmake.org/download/)

Optional software: If you need to build the samples dependent on third-party software (refer to the Sample List above), please install the corresponding software.

* [HALCON (version 20.11 or above)](https://www.mvtec.com/downloads)

  > Note: HALCON versions below 20.11 are not fully tested.

* [OpenCV (version 3.4.5 or above)](https://opencv.org/releases/)
* [PCL (version 1.8.1 or above)](https://github.com/PointCloudLibrary/pcl/releases): Refer to the following table and determine the version of PCL to install based on the version of Visual Studio. Download the EXE installer from the **Assets** section of the version that you want to install.

   | Visual Studio version | Supported PCL versions |
   | :----                 | :----                  |
   | 2017                  | 1.8.1–1.9.1            |
   | 2019                  | 1.8.1–1.12.1           |
   | 2022                  | 1.8.1 and above        |

  > Note: PCL is not supported in Visual Studio 2017.

#### Instructions

1. Make sure that the samples are stored in a location with read and write permissions.
2. If OpenCV and/or PCL are installed, add the following directories to the **Path** environment variable:

   * For PCL: `C:/Program Files/OpenNI/Tools`
   * For OpenCV: `xxx/opencv/build/x64/vc14/bin`
   * For OpenCV: `xxx/opencv/build/x64/vc14/lib`

3. (Optional) Disable unneeded samples: if any of the optional software is not installed, this step must be performed.

   Open the CMakeLists file in `xxx/area_scan_3d_camera`, and change **ON** to **OFF** in the options of the unneeded samples.

4. Run Cmake and set the source and build paths:

   | Field                       | Path                          |
   | :----                       | :----                         |
   | Where is the source code    | xxx/area_scan_3d_camera       |
   | Where to build the binaries | xxx/area_scan_3d_camera/build |

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

  * Install PCL:

    ```bash
    sudo apt-get install libpcl-dev
    ```

    > Note: On different versions of Ubuntu, this command installs different versions of PCL. On Ubuntu 18.04, PCL 1.8.1 is installed; on Ubuntu 20.04, PCL 1.10.0 is installed.

  * Install HALCON (20.11 or above)

    > Note: HALCON versions below 20.11 are not fully tested.

    ```bash
    tar zxvf halcon-20.11.3.0-linux.tar.gz
    sudo sh install-linux.sh #Note down the installation path of HALCON.
    ```

  * Add persistent environment variables for HALCON: open `/etc/profile` in an editor (such as vi) and paste the following lines to the end of the file. Replace `/opt/halcon` with the actual installation path of HALCON.

    ```bash
    HALCONARCH=x64-linux; export HALCONARCH
    HALCONROOT="/opt/halcon"; export HALCONROOT
    HALCONEXAMPLES=${HALCONROOT}/examples; export HALCONEXAMPLES
    HALCONIMAGES=${HALCONROOT}/examples/images; export HALCONIMAGES
    PATH=${HALCONROOT}/bin/${HALCONARCH}:${PATH}; export PATH
    if [ ${LD_LIBRARY_PATH} ] ; then
       LD_LIBRARY_PATH=${HALCONROOT}/lib/${HALCONARCH}:${LD_LIBRARY_PATH}; export LD_LIBRARY_PATH
    else
       LD_LIBRARY_PATH=${HALCONROOT}/lib/${HALCONARCH}; export LD_LIBRARY_PATH
    fi
    ```

  > Note:
  >
  > * The changes are applied when you log in again. Or, you can `source /etc/profile/` before you configure and build the sample.
  > * For more information, please refer to HALCON's installation guide.

#### Instructions

1. Navigate to the directory of the sample.

   ```bash
   cd xxx/area_scan_3d_camera/
   ```

2. (Optional) Disable unneeded samples: if any of the optional software is not installed, this step must be performed.

   Open the CMakeLists file in `xxx/area_scan_3d_camera/`, and change **ON** to **OFF** in the options of the unneeded samples.

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

5. Enter the index of the camera to which you want to connect, and press the Enter key. The obtained files are saved to `xxx/area_scan_3d_camera/build`.

## License

Mech-Eye Samples are distributed under the [BSD license](https://github.com/MechMindRobotics/mecheye_cpp_samples/blob/master/LICENSE).
