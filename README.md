# Python Samples

This repository contains Python samples for Mech-Eye SDK.

If you have any questions or have anything to share, feel free to post on the [Mech-Mind Online Community](https://community.mech-mind.com/). The community also contains a [specific category for development with Mech-Eye SDK](https://community.mech-mind.com/c/mech-eye-sdk-development/19).

## Installation

### Ubuntu 

1. Clone this repository to a specific folder.
2. Install [Mech-Eye API for Ubuntu](https://community.mech-mind.com/c/latest-product-downloads/10).
3. Install Mech-Eye API python wrapper by pip3.

    ```Python
    sudo pip3 install MechEyeAPI
    ```

4. (Optional) Install OpenCV and Open3D if you will run the samples marked with `(OpenCV)` and `(Open3D)` below.
    * Install OpenCV:

      ```Python
      sudo apt-get install libopencv-dev
      sudo apt-get install python3-opencv
      ```

    * Install Open3D:

      ```Python
      python3 -m pip install --upgrade pip
      sudo pip install open3d
      ```

5. Open and run one of the samples.

    ```Python
    cd ~/mecheye_python_samples/source/Basic
    python3 ConnectAndCaptureImage.py
    ```

> Note:: When writing your own program, use the import command to import Mech-Eye API first. Please import Mech-Eye API before importing Open3D.

### Windows

> Attention
>
> Please check if the following two directories are added to the **Path** environment variable:
>
> - xxx\\AppData\\Local\Programs\Python\\Python36\\
> - xxx\\AppData\\Local\Programs\Python\\Python36\\Scripts\\

1. Clone this repository to a specific folder.
2. Install [Mech-Eye SDK for Windows](https://community.mech-mind.com/c/latest-product-downloads/10).
3. Install Mech-Eye API python wrapper by pip.

    ```Python
    pip install MechEyeAPI
    ```

4. (Optional) Install OpenCV if you will run the samples marked with `(OpenCV)` below.

    ```Python
    pip install opencv-python
    ```

5. Open and run one of the samples.

    ```Python
    cd  xxx\mecheye_python_samples\source\Basic
    python ConnectAndCaptureImage.py
    ```


## Sample List

Samples are divided into five categories, **Basic**, **Advanced**, **Util**, **Laser** and **UHP**.

- **Basic**: camera connection and basic capturing functions.
- **Advanced**: advanced capturing functions.
- **Util**: obtain information from a camera and set camera parameters.
- **Laser**: for Laser, LSR and DEEP series cameras only. 
- **UHP**: for UHP series cameras only. 

The samples marked with `(Open3D)` require [open3d](https://pypi.org/project/open3d/) to be installed via pip (On Windows, installing Mech-Eye SDK will also install Open3D).
The samples marked with `(OpenCV)` require [opencv-python](https://pypi.org/project/opencv-python/) and [opencv-contrib-python](https://pypi.org/project/opencv-contrib-python/) to be installed via pip.

- **Basic**
  - [ConnectToCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/ConnectToCamera.py)  
    Connect to a Mech-Eye Industrial 3D Camera.
  - [ConnectAndCaptureImage](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/ConnectAndCaptureImage.py)  
    Connect to a camera and obtain the 2D image, depth map and point cloud data.
  - [CaptureColorMap](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CaptureColorMap.py) `(OpenCV)`  
    Obtain and save the 2D image in OpenCV format from a camera.
  - [CaptureDepthMap](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CaptureDepthMap.py) `(OpenCV)`  
    Obtain and save the depth map in OpenCV format from a camera.
  - [CapturePointCloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CapturePointCloud.py) `(Open3D)`  
    Obtain and save untextured and textured point clouds generated from images captured with a single exposure time.
  - [CaptureHDRPointCloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CaptureHDRPointCloud.py) `(Open3D)`  
    Obtain and save untextured and textured point clouds generated from images captured with multiple exposure times.
  - [CapturePointCloudROI](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CapturePointCloudROI.py) `(Open3D)`  
    Obtain and save untextured and textured point clouds of the objects in the ROI from a camera.
  - [CapturePointCloudFromTextureMask](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CapturePointCloudFromTextureMask.py) `(Open3D)`  
    Construct and save untextured and textured point clouds generated from a depth map and masked 2D image.
- **Advanced**
  - [CaptureCloudFromDepth](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureCloudFromDepth.py) `(Open3D)`  
    Construct and save point clouds from the depth map and 2D image obtained from a camera.
  - [CaptureSequentiallyMultiCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureSequentiallyMultiCamera.py)
    Obtain and save 2D images, depth maps and point clouds sequentially from multiple cameras.
  - [CaptureSimultaneouslyMultiCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureSimultaneouslyMultiCamera.py)
    Obtain and save 2D images, depth maps and point clouds simultaneously from multiple cameras.
  - [CaptureTimedAndPeriodically](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureTimedAndPeriodically.py)
    Obtain and save 2D images, depth maps and point clouds periodically for the specified duration from a camera.
- **Util**
  - [GetCameraIntri](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/GetCameraIntri.py)  
    Get and print a camera's intrinsic parameters.
  - [PrintDeviceInfo](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/PrintDeviceInfo.py)  
    Get and print a camera's information such as model, serial number and firmware version.
  - [SetDepthRange](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/SetDepthRange.py)  
    Set the range of depth values to be retained by a camera.
  - [SetParameters](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/SetParameters.py)  
    Set specified parameters to a camera.
  - [SetUserSets](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/SetUserSets.py)  
    Perform functions related to parameter groups, such as getting the names of available parameter groups, switching parameter group, and save the current parameter values to a specific parameter group. The parameter group feature allows user to save and quickly apply a set of parameter values.
- **Laser**
  - [SetLaserFramePartitionCount](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Laser/SetLaserFramePartitionCount.py)  
    Divide the projector FOV into partitions and project structured light in one partition at a time. The output of the entire FOV is composed from images of all partitions.
  - [SetLaserFrameRange](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Laser/SetLaserFrameRange.py)  
    Set the projection range of the structured light. The entire projector FOV is from 0 to 100.
  - [SetLaserFringeCodingMode](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Laser/SetLaserFringeCodingMode.py)  
    Set the coding mode of the structured light pattern for a camera.
  - [SetLaserPowerLevel](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Laser/SetLaserPowerLevel.py)  
    Set the output power of the laser projector in percentage of max power. This affects the intensity of the laser light.
- **UHP**
  - [SetUHPCaptureMode](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/UHP/SetUHPCaptureMode.py)  
    Set the capture mode (capture images with camera 1, with camera 2, or with both 2D cameras and compose the outputs.py).
  - [SetUHPFringeCodingMode](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/UHP/SetUHPFringeCodingMode.py)  
    Set the coding mode of the structured light pattern.
