# Python Samples for Mech-Eye 3D Laser Profiler

This documentation provides descriptions of Mech-Eye API Python samples for Mech-Eye 3D Laser Profiler and instructions for running the samples on Windows and Ubuntu.

If you have any questions or have anything to share, feel free to post on the [Mech-Mind Online Community](https://community.mech-mind.com/). The community also contains a [specific category for development with Mech-Eye SDK](https://community.mech-mind.com/c/mech-eye-sdk-development/19).

## Sample List

Samples are divided into the following categories: **Basic**, **Advanced**, and **Util**.

* **Basic** samples: Connect to the profiler and acquire data.
* **Advanced** samples: Acquire data in more complicated manners and set model-specific parameters.
* **Util** samples: Obtain profiler information and set common parameters.


The samples marked with `(OpenCV)` require [OpenCV](https://pypi.org/project/opencv-python/) to be installed.  

* **Basic**
  * [trigger_with_software_and_fixed_rate](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Basic/trigger_with_software_and_fixed_rate.py) `(OpenCV)`  
    Trigger data acquisition with signals input from software, trigger line scans at a fixed rate, and then retrieve and save the acquired data.
  * [trigger_with_external_device_and_fixed_rate](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Basic/trigger_with_external_device_and_fixed_rate.py) `(OpenCV)`  
    Trigger data acquisition with signals input from the external device, trigger line scans at a fixed rate, and then retrieve and save the acquired data.
  * [trigger_with_software_and_encoder](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Basic/trigger_with_software_and_encoder.py) `(OpenCV)`  
    Trigger data acquisition with signals input from software, trigger line scans with signals input from the encoder, and then retrieve and save the acquired data.
  * [trigger_with_external_device_and_encoder](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Basic/trigger_with_external_device_and_encoder.py) `(OpenCV)`  
    Trigger data acquisition with signals input from the external device, trigger line scans with signals input from the encoder, and then retrieve and save the acquired data.
  * [trigger_non_stop_acquisition](https://github.com/MechMindRobotics/mecheye_csharp_samples/tree/master/profiler/Basic/trigger_non_stop_acquisition.py) `(OpenCV)`  
    Trigger non-stop acquisition, and then retrieve and save the acquired data.
* **Advanced**
  * [trigger_multiple_profilers_simultaneously](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Advanced/trigger_multiple_profilers_simultaneously.py) `(OpenCV)`  
    Trigger multiple laser profilers to acquire data asynchronously and retrieve the acquired data.
  * [blind_spot_filtering](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Advanced/blind_spot_filtering.py) `(OpenCV)`  
    Detect and remove the false data caused by blind spots and obtain the filtered profile data.
  * [noise_removal](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Advanced/noise_removal.py) `(OpenCV)`  
    Remove the noise in the depth data and obtain the filtered profile data.
  * [profile_alignment](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Advanced/profile_alignment.py) `(OpenCV)`  
    Correct the X-axis and Z-axis vibrations in the profiles (aligning the profiles) and obtain the corrected profile data.
  * [transform_point_cloud](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Advanced/transform_point_cloud.py)  
    Obtain and save the point clouds in the custom reference frame.
  * [register_profiler_event](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Advanced/register_profiler_event.py)  
    Define and register the callback function for monitoring laser profiler events.
  * [use_virtual_device](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Advanced/use_virtual_device.py) `(OpenCV)`  
    Acquire the profile data stored in a virtual device, generate the intensity image and depth map, and save the images.
* **Util**
  * [render_depth_map](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Util/render_depth_map.py) `(OpenCV)`  
    Obtain and save the depth map rendered with the jet color scheme.
  * [manage_user_sets](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Util/manage_user_sets.py)  
    Manage parameter groups, such as obtaining the names of all parameter groups, adding a parameter group, switching the parameter group, and saving parameter settings to the parameter group.
  * [print_profiler_status](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Util/print_profiler_status.py)  
    Obtain and print the laser profiler's information, such as model, serial number, firmware version, and temperatures.
  * [handle_nan_and_negative_in_depth](https://github.com/MechMindRobotics/mecheye_python_samples/tree/master/profiler/Util/handle_nan_and_negative_in_depth.py) `(OpenCV)`  
    Trigger data acquisition and handle NaN and negative values in depth data.

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

3. Enter the index of the laser profiler to which you want to connect, and press the Enter key. The obtained files are saved to the folder where the sample is located.

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
   cd xxx/profiler
   ```

2. Run the sample: replace ``sample_name`` with the name of the sample.

   ```python
   sudo python3 sample_name.py
   ```

3. Enter the index of the laser profiler to which you want to connect, and press the Enter key. The obtained files are saved to the folder where the sample is located.
