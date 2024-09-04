from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *
from time import sleep
import numpy as np
from multiprocessing import Lock

mutex = Lock()
# Calculate the initial coordinates of each point, apply the rigid body transformations to the
# initial coordinates, and then write the transformed coordinates to the PLY file.
def transform_and_save_data_to_ply(file_name: str, profile_batch: ProfileBatch, x_unit: float, y_unit: float, use_encoder_values: bool, encoder_vals: np.array, is_organized: bool = True, coordinateTransformation: FrameTransformation = []):
    data_width = profile_batch.width()
    with open(file_name, 'w') as file:
        depth = profile_batch.get_depth_map().data()
        vertex_count = depth.size if is_organized else depth[~np.isnan(
            depth)].size
        y, x = np.indices(depth.shape, dtype=np.uint16)

        file.write(f"""ply
format ascii 1.0
comment File generated
comment x y z data unit in mm
element vertex {vertex_count}
property float x
property float y
property float z
end_header
"""
                   )
                   
        rotation_matrix = np.array(coordinateTransformation.rotation)
        translation_vector = np.array(coordinateTransformation.translation)
        
        def depth_to_point(x, y, depth):
            if not np.isnan(depth):
                # Calculate the initial coordinates of each point from the original profile data.
                pos = np.array([x * x_unit * pitch, y * y_unit * pitch, depth])
                # Apply the rigid body transformations to the initial coordinates to obtain the
                # coordinates in the custom reference frame.
                transformed_pos = np.dot(rotation_matrix, pos) + translation_vector
                file.write("{} {} {}\n".format(
                       transformed_pos[0],  transformed_pos[1], transformed_pos[2]))
            elif is_organized:
                file.write("nan nan nan\n")

        np.vectorize(depth_to_point)(x, np.repeat(encoder_vals, data_width).reshape(
            depth.shape) if use_encoder_values else y, depth)


# Convert the profile data to an untextured point cloud in the custom reference frame and save it
# to a PLY file.
def convert_batch_to_point_cloud_with_transformation(profile_batch: ProfileBatch, user_set: UserSet, coordinateTransformation:FrameTransformation):
    if profile_batch.is_empty():
        return

    error, x_unit = user_set.get_float_value(
        XAxisResolution.name)
    if not error.is_ok():
        show_error(error)
        return

    error, y_unit = user_set.get_float_value(YResolution.name)
    if not error.is_ok():
        show_error(error)
        return
    # # Uncomment the following line for custom Y Unit
    # y_unit = get_trigger_interval_distance()

    error, line_scan_trigger_source = user_set.get_enum_value(
        LineScanTriggerSource.name)
    if not error.is_ok():
        show_error(error)
        return
    use_encoder_values = line_scan_trigger_source == LineScanTriggerSource.Value_Encoder

    error, trigger_interval = user_set.get_int_value(
        EncoderTriggerInterval.name)
    if not error.is_ok():
        show_error(error)
        return

    encoder_vals = profile_batch.get_encoder_array().data().squeeze().astype(np.int64)
    encoder_vals = (
        encoder_vals - encoder_vals[0]).astype(np.int16) / trigger_interval

    print("Save the transformed point cloud.")
    transform_and_save_data_to_ply("PointCloud.ply", profile_batch, x_unit,
                         y_unit, use_encoder_values, encoder_vals, True, coordinateTransformation)

class TransformPointCloud(object):
    def __init__(self):
        self.profiler = Profiler()

    def set_parameters(self):
        self.user_set = self.profiler.current_user_set()

        # Set the "Data Acquisition Trigger Source" parameter to "Software"
        show_error(self.user_set.set_enum_value(
            DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_Software))

        # Set the "Line Scan Trigger Source" parameter to "Fixed rate"
        show_error(self.user_set.set_enum_value(
            LineScanTriggerSource.name, LineScanTriggerSource.Value_FixedRate))
        # Set the " Software Trigger Rate" to 1000 Hz
        show_error(self.user_set.set_float_value(
            SoftwareTriggerRate.name, 1000))

       # Set the "Scan Line Count" parameter (the number of lines to be scanned) to 1600
        show_error(self.user_set.set_int_value(ScanLineCount.name, 1600))

        error, self.data_width = self.user_set.get_int_value(
            DataPointsPerProfile.name)
        show_error(error)

        error, self.capture_line_count = self.user_set.get_int_value(
            ScanLineCount.name)
        show_error(error)

        error, data_acquisition_trigger_source = self.user_set.get_enum_value(
            DataAcquisitionTriggerSource.name)
        show_error(error)
        self.is_software_trigger = data_acquisition_trigger_source == DataAcquisitionTriggerSource.Value_Software

    def acquire_profile_data(self) -> bool:
        """
        Call start_acquisition() to enter the laser profiler into the acquisition ready status, and
        then call trigger_software() to start the data acquisition (triggered by software).
        """
        print("Start data acquisition.")
        status = self.profiler.start_acquisition()
        if not status.is_ok():
            show_error(status)
            return False

        if self.is_software_trigger:
            status = self.profiler.trigger_software()
            if (not status.is_ok()):
                show_error(status)
                return False

        self.profile_batch.clear()
        self.profile_batch.reserve(self.capture_line_count)

        while self.profile_batch.height() < self.capture_line_count:
            # Retrieve the profile data
            batch = ProfileBatch(self.data_width)
            status = self.profiler.retrieve_batch_data(batch)
            if status.is_ok():
                self.profile_batch.append(batch)
                sleep(0.2)
            else:
                show_error(status)
                return False

        print("Stop data acquisition.")
        status = self.profiler.stop_acquisition()
        if not status.is_ok():
            show_error(status)
        return status.is_ok()

    def main(self):
        if not find_and_connect(self.profiler):
            return -1

        if not confirm_capture():
            return -1

        self.set_parameters()

        self.profile_batch = ProfileBatch(self.data_width)

        # Acquire profile data without using callback
        if not self.acquire_profile_data():
            return -1

        if self.profile_batch.check_flag(ProfileBatch.BatchFlag_Incomplete):
            print("Part of the batch's data is lost, the number of valid profiles is:",
                  self.profile_batch.valid_height())
        # Obtain the rigid body transformation from the camera reference frame to the custom reference
        # frame
        # The custom reference frame can be adjusted using the "Custom Reference Frame" tool in
        # Mech-Eye Viewer. The rigid body transformations are automatically calculated after the
        # settings in this tool have been applied
        coordinateTransformation = get_transformation_params(self.profiler)
        if(coordinateTransformation.__is__valid__() == False):
            print("Transformation parameters are not set. Please configure the transformation parameters using the custom coordinate system tool in the client.")
        # Transform the reference frame, generate the untextured point cloud, and save the point cloud
        convert_batch_to_point_cloud_with_transformation(self.profile_batch,self.user_set,coordinateTransformation)

        # # Uncomment the following line to save a virtual device file using the ProfileBatch acquired.
        # self.profiler.save_virtual_device_file(self.profile_batch, "test.mraw")

        self.profiler.disconnect()
        print("Disconnected form the Mech-Eye Profiler successfully")
        return 0

if __name__ == '__main__':
    a = TransformPointCloud()
    a.main()
