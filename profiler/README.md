# Python Samples

This documentation provides descriptions of Mech-Eye API Python samples for Mech-Eye Industrial 3D Camera and instructions for running the samples on Windows and Ubuntu.

If you have any questions or have anything to share, feel free to post on the [Mech-Mind Online Community](https://community.mech-mind.com/). The community also contains a [specific category for development with Mech-Eye SDK](https://community.mech-mind.com/c/mech-eye-sdk-development/19).

## Sample List

Currently, the following samples are provided.

The samples marked with `(OpenCV)` require [OpenCV](https://opencv.org/releases/) to be installed.  

* [acquire_profile_data](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/acquire_profile_data.py) `(OpenCV)`  
  Acquire the profile data, generate the intensity image and depth map, and save the images.
* [acquire_profile_data_using_callback](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/acquire_profile_data_using_callback.py)  `(OpenCV)`  
  Acquire the profile data using a callback function, generate the intensity image and depth map, and save the images.
* [acquire_point_cloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/acquire_point_cloud.py)  
  Acquire the profile data, generate the point cloud, and save the point cloud in the CSV and PLY formats.
* [manage_user_sets](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/manage_user_sets.py)  
  Manage parameter groups, such as obtaining the names of all parameter groups, adding a parameter group, switching the parameter group, and saving parameter settings to the parameter group.
* [register_profiler_event](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/register_profiler_event.py)  
Define and register the callback function for monitoring the laser profiler connection status.
* [use_virtual_device](https://github.com/MechMindRobotics/mecheye_csharp_samples/tree/master/profiler/use_virtual_device.py) `(OpenCV)`  
Acquire the profile data stored in a virtual device, generate the intensity image and depth map, and save the images.

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
   cd xxx/profiler
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

  >Note: If you have installed Mech-Eye SDK before, please   uninstall it firstwith the following command:
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

  c. Add all installed versions of g++ as alternatives (using g++ 9 and g++ 13 asexamples):

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
   cd xxx/profiler
   ```

2. Run the sample: replace ``sample_name`` with the name of the sample.

   ```python
   sudo python3 sample_name.py
   ```

3. Enter the index of the camera to which you want to connect, and press the Enter key. The obtained files are saved to the folder where the sample is located.