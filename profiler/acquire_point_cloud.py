from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *
import numpy as np
from time import sleep

pitch = 1e-3


class AcquirePointCloud(object):
    def __init__(self):
        self.profiler = Profiler()

    def capture(self):
        print("Start Scanning")
        status = self.profiler.start_acquisition()
        if not status.is_ok():
            return

        status = self.profiler.trigger_software()
        if not status.is_ok():
            return

        self.total_batch = ProfileBatch(self.data_points)
        self.total_batch.reserve(self.capture_line_count)
        while self.total_batch.height() < self.capture_line_count:
            batch = ProfileBatch(self.data_points)
            status = self.profiler.retrieve_batch_data(batch)

            if status.is_ok():
                self.total_batch.append(batch)
                sleep(0.2)
            else:
                show_error(status)
                return status
        self.profiler.stop_acquisition()
        encoder_vals = self.total_batch.get_encoder_array().data().squeeze().astype(np.int64)
        self.encoder_vals = encoder_vals - encoder_vals[0]
        return ErrorStatus()

    def save_depth_data_to_csv(self, file_name, is_organized=True, use_encoder_values=True):
        depth = self.total_batch.get_depth_map().data()
        y, x = np.indices(depth.shape)

        def depth_to_point_with_encoder(x, x_unit, encoder_val, y_unit, depth):
            if not np.isnan(depth):
                return np.array([x * x_unit * pitch, encoder_val * y_unit * pitch, depth])
            else:
                return np.array([np.nan, np.nan, np.nan])

        def depth_to_point_without_encoder(x, x_unit, y, y_unit, depth):
            if not np.isnan(depth):
                return np.array([x * x_unit * pitch, y * y_unit * pitch, depth])
            else:
                return np.array([np.nan, np.nan, np.nan])

        if use_encoder_values:
            vfunc = np.vectorize(
                depth_to_point_with_encoder, otypes=[np.ndarray])
            to_write = np.array(vfunc(x, np.full_like(depth, self.x_unit), np.repeat(self.encoder_vals, self.data_points).reshape(depth.shape), np.full_like(
                depth, self.y_unit), depth).tolist()).reshape((depth.size, 3))
        else:
            vfunc = np.vectorize(
                depth_to_point_without_encoder, otypes=[np.ndarray])
            to_write = np.array(vfunc(x, np.full_like(depth, self.x_unit), y, np.full_like(
                depth, self.y_unit), depth).tolist()).reshape((depth.size, 3))

        with open(file_name, 'w') as file:
            file.write("X,Y,Z\n")
            if not is_organized:
                to_write = np.array(
                    [point for point in to_write if not np.isnan(point[0])])
            np.savetxt(file, to_write, delimiter=',')

    def get_line_count(self):
        while True:
            print("Please enter capture line count (min: 16, max: 60000): ")
            capture_line_count = input()
            if capture_line_count.isdigit() and 16 <= int(capture_line_count) <= 60000:
                self.capture_line_count = int(capture_line_count)
                break
            print("Input invalid!")

    def get_trigger_interval_distance(self):
        while True:
            print(
                "Please enter encoder trigger interval distance (unit: um, min: 1, max: 65535): ")
            trigger_interval_distance = input()
            if trigger_interval_distance.isdigit() and 1 <= int(trigger_interval_distance) <= 65535:
                self.y_unit = int(trigger_interval_distance)
                break
            print("Input invalid!")

    def set_and_get_parameters(self):
        current_user_set = self.profiler.current_user_set()

        # Set tht data acquisition trigger source to be software
        show_error(current_user_set.set_enum_value(
            DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_Software))
        # Set the data acquisition trigger source to be external
        # show_error(current_user_set.set_enum_value(DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_External))

        # Set the trigger source to Encoder
        show_error(current_user_set.set_enum_value(
            LineScanTriggerSource.name, LineScanTriggerSource.Value_Encoder))
        # Set the trigger source to FixedRate
        # show_error(current_user_set.set_enum_value(
        # LineScanTriggerSource.name, LineScanTriggerSource.Value_FixedRate))

        # Set the maximum number of lines to be scanned to capture_line_count
        show_error(current_user_set.set_int_value(
            ScanLineCount.name, self.capture_line_count))

        # Get the line width in the X direction
        error, self.data_points = current_user_set.get_int_value(
            DataPointsPerProfile.name)
        show_error(error)

        error, self.x_unit = current_user_set.get_float_value(
            XAxisResolution.name)
        show_error(error)

        error, self.y_unit = current_user_set.get_float_value(YResolution.name)
        show_error(error)

    def main(self):
        if find_and_connect(self.profiler):
            if not confirm_capture():
                self.profiler.disconnect()
                return
            self.get_line_count()
            self.set_and_get_parameters()
            # Uncomment the following line for custom Y Unit
            # self.get_trigger_interval_distance()
            if not self.capture().is_ok():
                self.profiler.disconnect()
                return
            self.save_depth_data_to_csv(
                "point_cloud.csv", is_organized=True, use_encoder_values=True)
            # Comment the line above and uncomment the line below if you set "Line Scan Trigger Source" to "FixedRate"
            # self.save_depth_data_to_csv("point_cloud.csv", is_organized=True, use_encoder_values=False)
            self.profiler.disconnect()
            print("Disconnected form the Mech-Eye Profiler successfully")


if __name__ == '__main__':
    a = AcquirePointCloud()
    a.main()
