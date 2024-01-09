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
                encoder_vals = self.total_batch.get_encoder_array().data().squeeze()
                self.encoder_vals = encoder_vals - encoder_vals[0]
                sleep(0.2)
            else:
                show_error(status)
                return status
        return ErrorStatus()

    def save_data(self, file_name, is_organized=True):
        depth = self.total_batch.get_depth_map().data().flatten()
        to_write = np.array([])
        for i in range(self.capture_line_count * self.data_points):
            if not np.isnan(depth[i]):
                to_write = np.append(to_write, [i % self.data_points * self.x_unit * pitch,
                                                self.encoder_vals[int(i / self.data_points)] * self.y_unit * pitch, depth[i]])
            elif is_organized:
                to_write = np.append(to_write, [np.nan, np.nan, np.nan])
        to_write = to_write.reshape((-1, 3))
        with open(file_name, 'w') as file:
            file.write("X,Y,Z\n")
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

    def set_parameters(self):
        current_user_set = self.profiler.current_user_set()

        # Set tht data acquisition trigger source to be software
        show_error(current_user_set.set_enum_value(
            DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_Software))
        # Set the data acquisition trigger source to be external
        # show_error(current_user_set.set_enum_value(DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_External))

        # Set the trigger source to Encoder
        show_error(current_user_set.set_enum_value(
            LineScanTriggerSource.name, LineScanTriggerSource.Value_Encoder))

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

    def main(self):
        if find_and_connect(self.profiler):
            self.get_line_count()
            self.get_trigger_interval_distance()
            if not confirm_capture():
                self.profiler.disconnect()
                return
            self.set_parameters()
            if not self.capture().is_ok():
                self.profiler.disconnect()
                return
            self.save_data("point_cloud.csv")
            self.profiler.disconnect()
            print("Disconnected form the Mech-Eye Profiler successfully")


if __name__ == '__main__':
    a = AcquirePointCloud()
    a.main()
