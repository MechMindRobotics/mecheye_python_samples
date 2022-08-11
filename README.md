# Python Samples

This repository contains Python samples for Mech-Eye SDK.

## Installation

### Ubuntu 
1. Clone this repository to a specific folder.
2. Install [Mech-Eye API for Ubuntu](https://www.mech-mind.com/download/camera-sdk.html).
3. Install Mech-Eye API python wrapper by pip3.

```Python
pip3 install MechEyeAPI
```

4. Open and run one of the samples.

```Python
python3 ConnectAndCaptureImage.py
```


### Windows
1. Clone this repository to a specific folder.
2. Install [Mech-Eye SDK for Windows](https://www.mech-mind.com/download/camera-sdk.html).
3. Install Mech-Eye API python wrapper by pip.

```Python
pip install MechEyeAPI
```
4. Open and run one of the samples.

```Python
python ConnectAndCaptureImage.py
```


## Sample List

Samples are divided into five categories, **Basic**, **Advanced**, **Util**, **Laser** and **UHP**.

- **Basic**: camera connection and basic capturing functions.
- **Advanced**: advanced capturing functions.
- **Util**: obtain information from a camera and set camera parameters.
- **Laser**: for Laser/LSR Series cameras only. 
- **UHP**: for UHP series cameras only. 

The samples marked with `(Open3D)` require [open3d](https://pypi.org/project/open3d/) to be installed via pip.
The samples marked with `(OpenCV)` require [opencv-python](https://pypi.org/project/opencv-python/) and [opencv-contrib-python](https://pypi.org/project/opencv-contrib-python/) to be installed via pip.

- **Basic**
  - [ConnectToCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/ConnectToCamera.py)  
    Connect to a Mech-Eye Industrial 3D Camera.
  - [ConnectAndCaptureImage](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/ConnectAndCaptureImage.py)  
    Connect to a camera and obtain 2D image, depth map and 3D image.
  - [CaptureColorMap](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CaptureColorMap.py) `(OpenCV)`  
    Obtain 2D image in OpenCV format from a camera.
  - [CaptureDepthMap](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CaptureDepthMap.py) `(OpenCV)`  
    Obtain depth map in OpenCV format from a camera.
  - [CapturePointCloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CapturePointCloud.py) `(Open3D)`  
    Obtain untextured and textured point clouds (PCL format) generated from images captured with a single exposure time.
  - [CaptureHDRPointCloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CaptureHDRPointCloud.py) `(Open3D)`  
    Obtain untextured and textured point clouds (PCL format) generated from images captured with multiple exposure times.
  - [CapturePointCloudROI](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CapturePointCloudROI.py) `(Open3D)`  
    Obtain untextured and textured point clouds (PCL format) of the objects in the ROI from a camera.
- **Advanced**
  - [CaptureCloudFromDepth](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureCloudFromDepth.py) `(Open3D)`  
    Construct point clouds from depth map and 2D image captured from a camera.
  - [CaptureSequentiallyMultiCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureSequentiallyMultiCamera.py)
    Obtain 2D image, depth map and 3D images sequentially from multiple cameras.
  - [CaptureSimultaneouslyMultiCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureSimultaneouslyMultiCamera.py)
    Obtain 2D image, depth map and 3D images simultaneously from multiple cameras.
  - [CaptureTimedAndPeriodically](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureTimedAndPeriodically.py)
    Obtain 2D image, depth map and 3D images periodically for the specified duration from a camera.
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
    Functions related to parameter groups, such as getting the names of available parameter groups, switching parameter group, and save the current parameter values to a specific parameter group. The parameter group feature allows user to save and quickly apply a set of parameter values.
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
