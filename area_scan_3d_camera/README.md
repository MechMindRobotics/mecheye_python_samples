# Python Samples

This repository contains Python samples for Mech-Eye SDK.

If you have any questions or have anything to share, feel free to post on the [Mech-Mind Online Community](https://community.mech-mind.com/). The community also contains a [specific category for development with Mech-Eye SDK](https://community.mech-mind.com/c/mech-eye-sdk-development/19).

## Sample List

Samples are divided into the following categories: **basic**, **advanced**, and **util**.

* **basic** samples: Connect to the camera and acquire data.
* **advanced** samples: Acquire data in more complicated manners and set model-specific parameters.
* **util** samples: Obtain camera information and set common parameters.

The samples marked with `(OpenCV)` require OpenCV to be installed.

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
  * [set_parameters_of_laser_cameras](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/set_parameters_of_laser_cameras.py)  
    Set the parameters specific to laser cameras.
  * [set_parameters_of_uhp_cameras](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/set_parameters_of_uhp_cameras.py)  
    Set the parameters specific to the UHP series.
  * [register_camera_event](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/advanced/register_camera_event.py)  
    Define and register the callback function for monitoring the camera connection status.
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
  * [manage_user_set](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/util/manage_user_set.py)  
    Manage user sets, such as obtaining the names of all user sets, adding a user set, switching the user set, and saving parameter settings to the user set.
  * [save_and_load_user_set](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/area_scan_3d_camera/util/save_and_load_user_set.py)  
    Import and replace all user sets from a JSON file, and save all user sets to a JSON file.

## Run the Samples

This section introduces how to clone and then run the samples.

Make sure that the version of Python installed is between 3.6.5 and 3.10.

### Windows

1. Clone this repository to local.
2. Install the latest version of [Mech-Eye SDK](https://downloads.mech-mind.com/?tab=tab-sdk).
3. Install Python Mech-Eye API:

   ```python
   pip install MechEyeAPI
   ```

4. (Optional) Install OpenCV if you need to build the samples dependent on OpenCV (refer to the Sample List above):

   ```python
   pip install opencv-python
   ```

5. Navigate to the folder where a sample is located. Replace `category` with the category name of the sample.

   ```sh
   cd xxx/mecheye_python_samples/area_scan_3d_camera/category
   ```

6. Run the sample: replace `sample_name`` with the name of the sample.

   ```python
   python sample_name.py
   ```

7. Enter the index of the camera to which you want to connect, and press the Enter key. The obtained files are saved to the folder where the sample is located.

### Ubuntu

1. Clone this repository to local:

   ```bash
   cd ~
   git clone https://github.com/MechMindRobotics/mecheye_python_samples.git
   ```

2. Install [Mech-Eye SDK (latest version)](https://downloads.mech-mind.com/?tab=tab-sdk).

   >Note: If you have installed Mech-Eye SDK before, please   uninstall it first with the following command:
   >
   >```bash
   >sudo dpkg -P MechEyeApi
   >```

   * If the system architecture is AMD64, execute the following   command:

     ```bash
     sudo dpkg -i 'MechEyeApi_x.x.x_amd64.deb'
     ```

   * If the system architecture is ARM64, execute the following   command:

     ```bash
     sudo dpkg -i 'MechEyeApi_x.x.x_arm64.deb'
     ```

3. Upgrade g++ to ensure that its version is 12 or above.

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

   d. Select the g++ version. Enter the number corresponding to the later version g++ to select this version.

      ```bash
      sudo update-alternatives --config g++
      ```

   e. Check if the later version g++ is successfully selected:

      ```bash
      g++ --version
      ```

4. Install Python Mech-Eye API:

   ```bash
   sudo pip3 install MechEyeApi
   ```

5. (Optional) Install OpenCV if you need to build the samples dependent on OpenCV (refer to the Sample List above):

   ```bash
   sudo apt-get install libopencv-dev
   sudo apt-get install python3-opencv
   ```

6. Navigate to the folder where a sample is located. Replace `category` with the category name of the sample.

   ```bash
   cd ~/mecheye_python_samples/area_scan_3d_camera/category
   ```

7. Run the sample: replace `sample_name`` with the name of the sample.

   ```python
   sudo python3 sample_name.py
   ```

8. Enter the index of the camera to which you want to connect, and press the Enter key. The obtained files are saved to the folder where the sample is located.