# Python Samples

This repository contains Python samples for Mech-Eye SDK.

## Installation

### Dependencies

1. Download and install [Mech-Eye SDK_1.5.2](https://www.mech-mind.com/download/CameraSDK.html)
2. Clone this repository to a specific folder.
3. Add MechEyeApi to the path of environment variables of the system.

We ran and tested interfaces on Python3.6. Make sure to install Python 3.6 or higher.

These python libraries are needed:

* opencv-python
* opencv-contrib-python
* open3d
* numpy

opencv-python, opencv-contrib-python, open3d and numpy can be installed with pip by the following command:

```Python
pip install opencv-python opencv-contrib-python open3d numpy
```

### Installing official version of Mech-Eye Python API from PyPI using pip

Use pip to install the latest official version of Mech-Eye Python API from PyPI:

```Python
pip install MechEyeAPI
```

On some systems Python 3 `pip` is called `pip3`. In this guide we just call it `pip`.  
When using pip version 19 or higher, build dependencies are handled automatically.

## Sample list

There are four categoires of samples: **Basic**, **Advanced**, **Util**, and **Laser**.  

The category **Basic** contains samples that are related to basic connecting and capturing.  
The category **Advanced** contains samples that use advanced capturing tricks.  
The category **Util** contains samples that get and print information and set parameters.  
The category **Laser** contains samples that can only be used on laser cameras.  

The samples marked with `(Open3D)` require [open3d](https://pypi.org/project/open3d/) to be installed via pip.
The samples marked with `(OpenCV)` require [opencv-python](https://pypi.org/project/opencv-python/) and [opencv-contrib-python](https://pypi.org/project/opencv-contrib-python/) to be installed via pip.

* **Basic**
  * [ConnectToCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Basic/ConnectToCamera.py)  
    Connects to a Mech-Eye Industrial 3D Camera.
  * [ConnectAndCaptureImage](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Basic/ConnectAndCaptureImage.py)  
    Connects to a Mech-Eye Industrial 3D Camera and capture 2D and 3D data.
  * [CaptureColorMap](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Basic/CaptureColorMap.py) `(OpenCV)`  
    Capture color map data with OpenCV data structure from a camera.
  * [CaptureDepthMap](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Basic/CaptureDepthMap.py) `(OpenCV)`  
    Capture depth map data with OpenCV data structure from a camera.
  * [CapturePointCloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Basic/CapturePointCloud.py) `(Open3D)`  
    Capture point clouds with PCL data structure from a camera.
  * [CaptureHDRPointCloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Basic/CaptureHDRPointCloud.py) `(Open3D)`  
    Capture point clouds in HDR mode with PCL data structure from a camera.
  * [CapturePointCloudROI](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Basic/CapturePointCloudROI.py) `(Open3D)`  
    Capture point clouds with ROI enabled with PCL data structure from a camera.
* **Advanced**
  * [CaptureCloudFromDepth](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Advanced/CaptureCloudFromDepth.py) `(Open3D)`  
    Construct point clouds from depth map and color map captured from a camera.
  * [CaptureSequentiallyMultiCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Advanced/CaptureSequentiallyMultiCamera.py)
    Capture sequentially from multiple cameras.
  * [CaptureSimultaneouslyMultiCamera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Advanced/CaptureSimultaneouslyMultiCamera.py)
    Capture simultaneously from multiple cameras.
  * [CaptureTimedAndPeriodically](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Advanced/CaptureTimedAndPeriodically.py)
    Capture periodically for a specific time form a camera.
* **Util**
  * [GetCameraIntri](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Util/GetCameraIntri.py)  
    Get and print a camera's intrinsic parameters.
  * [PrintDeviceInfo](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Util/PrintDeviceInfo.py)  
    Get and print a camera's information.
  * [SetDepthRange](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Util/SetDepthRange.py)  
    Set the depth range of a camera.
  * [SetParameters](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Util/SetParameters.py)  
    Set and get the parameters from a camera.
  * [SetUserSets](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Util/SetUserSets.py)  
    Get current user set name and available user sets, save settings to a specific user set. The User Set feature allows the user to customize and store the individual settings.
* **Laser**
  * [SetLaserFramePartitionCount](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Laser/SetLaserFramePartitionCount.py)  
    Set the laser scan partition number for a laser camera.
  * [SetLaserFrameRange](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Laser/SetLaserFrameRange.py)  
    Set the laser scan field of view for a laser camera.
  * [SetLaserFringeCodingMode](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Laser/SetLaserFringeCodingMode.py)  
    Set the fringe coding mode for a laser camera.
  * [SetLaserPowerLevel](https://github.com/MechMindRobotics/mecheye_python_samples/tree/main/source/Laser/SetLaserPowerLevel.py)  
    Set the power level for a laser camera.
