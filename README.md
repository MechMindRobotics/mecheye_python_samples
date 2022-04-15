# Mech-Eye_python_interface
  This is official Python interfaces for Mech-Eye cameras. 

  Please select the proper branch corresponding to the camera firmware version.
## Introduction

  This project is developped by python. We use ZeroMQ library to connect camera devices in the LANs. And json is used to pack and unpack data from network. Supported     on both Windows and Ubuntu OS.

## Features

  By using these interfaces, you can easily control your mech_eye cameras in python programs. The features are as follows:

    * Connect to your camera in your LANS.
    * Set and get camera parameters like exposure time, period and so on.
    * Get color images and depth images as numpy arrays.
    * Get point cloud data as the format defined in open3d, a python lib which can deal with point clouds.

## Installation

### Dependencies

1. Download and install [Mech-Eye SDK_1.5.1](https://www.mech-mind.com.cn/support/xjSDK.html)
2. Clone this repository to a specific folder.
3. Add MechEyeApi to the path of environment variables of the system.
4. We ran and tested interfaces on Python3.6. Make sure to install Python 3.6 or higher.
5. These python libraries are needed:

    * opencv_python
    * json
    * open3d
    * numpy
    * pcl_python

  opencv_python,json,open3d and numpy you can install with pip, by the following command:

  ```
  pip3 install opencv-python json open3d numpy
  ```
  install pcl_python you need source code of python-pcl,the All-In-One Installer of PCL1.9.1(Version must be between 1.6 and 1.9.)and windows Gtk.

### Installing official version from PyPI using PIP

  Use PIP to fetch the latest official version from PyPI:

    pip install MechEyeAPI


## Quick Start

  In terminal, change your working directory to the repo, then in  **captureResultToCV.py**, then run:

  ```powershell
  python.exe captureResultToCV.py
  ```

  Some pictures will also be captured and stored in the same directory of the repo.

## Project hierarchy

  The following shows the hierarchy of project files:

  ```
  Mech-Eye_python_interface

  ├─ captureResultToCV.py
  ├─ captureResultToPLY.py
  ├─ connectAndCaptureImage.py
  └─ getAndSetParameter.py
  ```
 

## Intro to samples

  The original project provides a **getAndSetParameter.py** to show how to use interfaces. 

  This sample mainly shows how to set camera's paramters like exposure time.

  First, we need to Get camera list and  get some brief info about camera, and then connect by index:

  ```python
  device = Device()
  device_list = device.get_device_list()

  def print_device_info(info):
      print("Camera Model Name: " + info.model())
      print("Camera ID: " + info.id())
      print("Camera IP: " + info.ip())
      print("Hardware Version: " + info.hardware_version())
      print("Firmware Version: " + info.firmware_version())
      print(" ")

  for i, info in enumerate(device_list):
      print("Mech-Eye device index : " + str(i))
      print_device_info(info)

  user_input = input("Please enter the device index you want to connect: ")

  device.connect(device_list[int(user_input)])
  ```

  We can set and get the value of a specific parameter, in this case, we choose exposure time for color image:

  ```python
  device.set2D_exposure_mode("Timed") # set exposure mode to Timed
  print(str(device.get2D_exposure_mode()))
  device.set2D_exposure_time(812) # set exposure time to 812ms
  print(device.get2D_exposure_time())
  ```

We can set and get the value of a specific parameter, in this case, we choose exposure time for color image:

```python
device.set2D_exposure_mode("Timed") # set exposure mode to Timed
print(str(device.get2D_exposure_mode()))
device.set2D_exposure_time(812) # set exposure time to 812ms
print(device.get2D_exposure_time())
```

