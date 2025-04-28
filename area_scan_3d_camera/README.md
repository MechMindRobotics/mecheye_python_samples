# Python Samples for Mech-Eye Industrial 3D Camera

This documentation provides descriptions of Mech-Eye API Python samples for Mech-Eye Industrial 3D Camera and instructions for running the samples on Windows and Ubuntu.

If you have any questions or have anything to share, feel free to post on the [Mech-Mind Online Community](https://community.mech-mind.com/). The community also contains a [specific category for development with Mech-Eye SDK](https://community.mech-mind.com/c/mech-eye-sdk-development/19).

## Sample List

Samples are divided into the following categories: **basic**, **advanced**, and **util**.

* **basic** samples: Connect to the camera and acquire data.
* **advanced** samples: Acquire data in more complicated manners and set model-specific parameters.
* **util** samples: Obtain camera information and set common parameters.

The samples marked with `(OpenCV)` require [OpenCV](https://pypi.org/project/opencv-python/) to be installed.

* **basic**
  * [connect_to_camera](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/basic/connect_to_camera.py)  
    Connect to a camera.
  * [connect_and_capture_images](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/basic/connect_and_capture_images.py)  
    Connect to a camera and obtain the 2D image, depth map, and point cloud data.
  * [capture_2d_image](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/basic/capture_2d_image.py) `(OpenCV)`  
    Obtain and save the 2D image.
  * [capture_depth_map](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/basic/capture_depth_map.py) `(OpenCV)`  
    Obtain and save the depth map.
  * [capture_point_cloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/basic/capture_point_cloud.py)  
    Obtain and save the untextured and textured point clouds.
  * [capture_point_cloud_hdr](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/basic/capture_point_cloud_hdr.py)  
    Set multiple exposure times, and then obtain and save the untextured and textured point clouds.
  * [capture_point_cloud_with_normals](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/basic/capture_point_cloud_with_normals.py)  
    Calculate normals and save the untextured and textured point clouds with normals.
* **advanced**
  * [convert_depth_map_to_point_cloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/convert_depth_map_to_point_cloud.py)  
    Generate a point cloud from the depth map and save the point cloud.
  * [multiple_cameras_capture_sequentially](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/multiple_cameras_capture_sequentially.py) `(OpenCV)`  
    Obtain and save 2D images, depth maps, and point clouds sequentially from multiple cameras.
  * [multiple_cameras_capture_simultaneously](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/multiple_cameras_capture_simultaneously.py) `(OpenCV)`  
    Obtain and save 2D images, depth maps, and point clouds simultaneously from multiple cameras.
  * [capture_periodically](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/capture_periodically.py) `(OpenCV)`  
    Obtain and save 2D images, depth maps, and point clouds periodically for the specified duration from a camera.
  * [mapping_2d_image_to_depth_map](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/mapping_2d_image_to_depth_map.py)  
    Generate untextured and textured point clouds from a masked 2D image and a depth map.
  * [render_depth_map](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/render_depth_map.py) `(OpenCV)`  
    Obtain and save the depth map rendered with the jet color scheme.
  * [transform_point_cloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/Advanced/transform_point_cloud.py)  
    Obtain and save the point clouds in the custom reference frame.
  * [set_parameters_of_laser_cameras](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/set_parameters_of_laser_cameras.py)  
    Set the parameters specific to laser cameras.
  * [set_parameters_of_uhp_cameras](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/set_parameters_of_uhp_cameras.py)  
    Set the parameters specific to the UHP series.
  * [register_camera_event](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/register_camera_event.py)  
    Define and register the callback function for monitoring camera events.
  * [capture_stereo_2d_images](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/capture_stereo_2d_images.py) `(OpenCV)`  
    Obtain and save the 2D images from both 2D cameras.
    > Note: This sample is only applicable to the following models: Deep, Laser L Enhanced, PRO XS, PRO XS-GL, LSR L, LSR L-GL, LSR S, LSR S-GL, DEEP, and DEEP-GL.
* **util**
  * [get_camera_intrinsics](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/util/get_camera_intrinsics.py)  
    Obtain and print the camera intrinsic parameters.
  * [print_camera_info](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/util/print_camera_info.py)  
    Obtain and print the camera information, such as model, serial number, firmware version, and temperatures.
  * [set_scanning_parameters](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/util/set_scanning_parameters.py)  
    Set the parameters in the **3D Parameters**, **2D Parameters**, and **ROI** categories.
  * [set_depth_range](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/util/set_depth_range.py)  
    Set the **Depth Range** parameter.
  * [set_point_cloud_processing_parameters](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/util/set_point_cloud_processing_parameters.py)  
    Set the **Point Cloud Processing** parameters.
  * [manage_user_sets](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/util/manage_user_sets.py)  
    Manage parameter groups, such as obtaining the names of all parameter groups, adding a parameter group, switching the parameter group, and saving parameter settings to the parameter group.
  * [save_and_load_user_set](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/util/save_and_load_user_set.py)  
    Import and replace all parameter groups from a JSON file, and save all parameter groups to a JSON file.
* **calibration**
  * [hand_eye_calibration](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/calibration/hand_eye_calibration.py)`(OpenCV)`  
    Perform hand-eye calibration.

## Run the Samples

### Windows

#### Prerequisites

1. Make sure that the variant of Python installed is 64-bit, and the version is between 3.7 and 3.11.
2. Please download and install the required software listed below.

* [Mech-Eye SDK (latest version)](https://downloads.mech-mind.com/?tab=tab-sdk)
* Python Mech-Eye API (latest version):

  ```python
  pip install MechEyeAPI
  ```

Optional software: If you need to build the samples dependent on third-party software (refer to the Sample List above), please install the corresponding software.

* OpenCV (latest version):

  ```python
  pip install opencv-python
  ```

#### Instructions

1. Navigate to the folder where a sample is located.

   ```sh
   cd xxx/area_scan_3d_camera
   ```

2. Run the sample: replace ``sample_name`` with the name of the sample.

   ```python
   python sample_name.py
   ```

3. Enter the index of the camera to which you want to connect, and press the Enter key. The obtained files are saved to the folder where the sample is located.

### Ubuntu

Ubuntu 18 or above is required.

#### Prerequisites

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

* Upgrade g++ to ensure that its version is 12 or above.

  a. Install a later version g++ (using g++ 13 as an example):

     ```bash
     sudo add-apt-repository ppa:ubuntu-toolchain-r/test
     sudo apt-get update
     sudo apt install g++-13
     ```

  b. Use the `ls` command to check the installed versions of g++:

     ```bash
     ls usr/bin/g++*
     ```

  c. Add all installed versions of g++ as alternatives (using g++ 9 and g++ 13 as examples):

     ```bash
     sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 10
     sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 20
     ```

  d. Select the g++ version. Enter the number corresponding to the later version ++ to select this version.

     ```bash
     sudo update-alternatives --config g++
     ```

  e. Check if the later version g++ is successfully selected:

     ```bash
     g++ --version
     ```

* Install Python Mech-Eye API:

  ```bash
  sudo pip3 install MechEyeApi
  ```

* (Optional) Install OpenCV if you need to build the samples dependent on OpenCV (refer to the Sample List above):

  ```bash
  sudo apt-get install libopencv-dev
  sudo apt-get install python3-opencv
  ```

#### Instructions

1. Navigate to the folder where a sample is located.

   ```bash
   cd xxx/area_scan_3d_camera
   ```

2. Run the sample: replace ``sample_name`` with the name of the sample.

   ```python
   sudo python3 sample_name.py
   ```

3. Enter the index of the camera to which you want to connect, and press the Enter key. The obtained files are saved to the folder where the sample is located.
