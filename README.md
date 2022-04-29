# Python Samples

This repository contains Python samples for Mech-Eye Industrial 3D Camera.

## Installation

### Ubuntu 
1. Clone this repository to a specific folder.
2. Install [Mech-Eye API_1.5.2 for Ubuntu](https://github.com/MechMindRobotics/mecheye_python_samples/blob/master/Mech-Eye%20API_1.5.2_Ubuntu_Amd64/MechEyeApi_1.5.2_amd64.deb).
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
2. Install [Mech-Eye SDK_1.5.2 for Windows](https://www.mech-mind.com/download/camera-sdk.html).
3. Install Mech-Eye API python wrapper by pip.

```Python
pip install MechEyeAPI
```
4. Open and run one of the samples.

```Python
python ConnectAndCaptureImage.py
```


## Sample list

There are four categories of samples: **Basic**, **Advanced**, **Util**, and **Laser**.  

- The category **Basic** contains samples that are related to basic connecting and capturing.  
- The category **Advanced** contains samples that use advanced capturing tricks.  
- The category **Util** contains samples that get and print information and set parameters.  
- The category **Laser** contains samples that can only be used on Mech-Eye Laser cameras.  

The samples marked with `(Open3D)` require [open3d](https://pypi.org/project/open3d/) to be installed via pip.
The samples marked with `(OpenCV)` require [opencv-python](https://pypi.org/project/opencv-python/) and [opencv-contrib-python](https://pypi.org/project/opencv-contrib-python/) to be installed via pip.

- **Basic**
  - [ConnectToCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/ConnectToCamera.py)  
    Connect to a Mech-Eye Industrial 3D Camera.
  - [ConnectAndCaptureImage](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/ConnectAndCaptureImage.py)  
    Connect to a Mech-Eye Industrial 3D Camera and capture 2D and 3D data.
  - [CaptureColorMap](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CaptureColorMap.py) `(OpenCV)`  
    Capture color image data with OpenCV data structure from a camera.
  - [CaptureDepthMap](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CaptureDepthMap.py) `(OpenCV)`  
    Capture depth map data with OpenCV data structure from a camera.
  - [CapturePointCloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CapturePointCloud.py) `(Open3D)`  
    Capture monochrome and color point clouds with PCL data structure from a camera.
  - [CaptureHDRPointCloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CaptureHDRPointCloud.py) `(Open3D)`  
    Capture monochrome and color point clouds in HDR mode with PCL data structure from a camera.
  - [CapturePointCloudROI](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Basic/CapturePointCloudROI.py) `(Open3D)`  
    Capture monochrome and color point clouds in ROI with PCL data structure from a camera.
- **Advanced**
  - [CaptureCloudFromDepth](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureCloudFromDepth.py) `(Open3D)`  
    Construct point clouds from depth map and color image captured from a camera.
  - [CaptureSequentiallyMultiCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureSequentiallyMultiCamera.py)
    Capture sequentially from multiple cameras.
  - [CaptureSimultaneouslyMultiCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureSimultaneouslyMultiCamera.py)
    Capture simultaneously from multiple cameras.
  - [CaptureTimedAndPeriodically](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Advanced/CaptureTimedAndPeriodically.py)
    Capture periodically for a specific time from a camera.
- **Util**
  - [GetCameraIntri](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/GetCameraIntri.py)  
    Get and print a camera's intrinsic parameters.
  - [PrintDeviceInfo](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/PrintDeviceInfo.py)  
    Get and print a camera's information.
  - [SetDepthRange](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/SetDepthRange.py)  
    Set the depth range of a camera.
  - [SetParameters](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/SetParameters.py)  
    Set specified parameters to a camera.
  - [SetUserSets](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Util/SetUserSets.py)  
    Get the current userset name and available usersets of parameter settings, and save the settings to a specific userset. The User Set feature allows the user to customize and store the individual settings.
- **Laser**
  - [SetLaserFramePartitionCount](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Laser/SetLaserFramePartitionCount.py)  
    Set the laser scan partition count for a Mech-Eye Laser camera.
  - [SetLaserFrameRange](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Laser/SetLaserFrameRange.py)  
    Set the laser scan range for a Mech-Eye Laser camera.
  - [SetLaserFringeCodingMode](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Laser/SetLaserFringeCodingMode.py)  
    Set the fringe coding mode for a Mech-Eye Laser camera.
  - [SetLaserPowerLevel](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/source/Laser/SetLaserPowerLevel.py)  
    Set the laser power level for a Mech-Eye Laser camera.
