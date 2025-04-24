from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *
import cv2
from time import sleep
from multiprocessing import Lock

mutex = Lock()


class CustomAcquisitionCallback(AcquisitionCallbackBase):
    def __init__(self, width):
        AcquisitionCallbackBase.__init__(self)
        self.total_batch = ProfileBatch(width)

    def run(self, batch):
        mutex.acquire()
        if (not batch.get_error_status().is_ok()):
            print("Error occurred during data acquisition.")
            show_error(batch.get_error_status())
        self.total_batch.append(batch)
        mutex.release()


class UseVirtualDevice(object):
    def __init__(self):
        #  Please ensure that the file name is encoded in UTF-8 format.
        self.profiler = VirtualProfiler("test.mraw")

    def get_parameters(self):
        current_user_set = self.profiler.current_user_set()

        # Get the number of data points in each profile
        error, self.data_width = current_user_set.get_int_value(
            DataPointsPerProfile.name)
        show_error(error)

        # Get the current value of the "Scan Line Count" parameter
        error, self.capture_line_count = current_user_set.get_int_value(
            ScanLineCount.name)
        show_error(error)

    def capture_without_callback(self):
        # Define a ProfileBatch object to store the profile data
        self.total_batch = ProfileBatch(self.data_width)

        # Acquire data without using callback
        status = self.profiler.start_acquisition()
        if not status.is_ok():
            show_error(status)
            return False

        self.total_batch.reserve(self.capture_line_count)
        while self.total_batch.height() < self.capture_line_count:
            batch = ProfileBatch(self.data_width)
            # Retrieve the profile data
            status = self.profiler.retrieve_batch_data(batch)
            if status.is_ok():
                self.total_batch.append(batch)
                sleep(0.1)
            else:
                show_error(status)
                break
        status = self.profiler.stop_acquisition()
        if not status.is_ok():
            show_error(status)
            return False
        return True

    def capture_with_callback(self):
        self.callback = CustomAcquisitionCallback(
            self.data_width)

        # Acquire data with the callback function
        status = self.profiler.register_acquisition_callback(
            self.callback)
        if not status.is_ok():
            show_error(status)
            return False

        # Call startAcquisition() to enter the virtual device into the acquisition ready status
        status = self.profiler.start_acquisition()
        if not status.is_ok():
            show_error(status)
            return False

        while True:
            mutex.acquire()
            if self.callback.total_batch.is_empty():
                mutex.release()
                sleep(0.1)
            else:
                mutex.release()
                break

        status = self.profiler.stop_acquisition()
        if not status.is_ok():
            show_error(status)
            return False
        return True

    def save_images(self, depth_file_name, intensity_file_name):
        cv2.imwrite(depth_file_name,
                    self.total_batch.get_depth_map().data())
        cv2.imwrite(intensity_file_name,
                    self.total_batch.get_intensity_image().data())

    def save_callback_images(self, depth_file_name, intensity_file_name):
        cv2.imwrite(depth_file_name,
                    self.callback.total_batch.get_depth_map().data())
        cv2.imwrite(intensity_file_name,
                    self.callback.total_batch.get_intensity_image().data())

    def main(self):
        self.get_parameters()
        if not self.capture_without_callback():
            return -1
        print("Save the depth map and the intensity image.")
        self.save_images("DepthMap.tiff", "IntensityImage.png")
        # if not self.capture_with_callback():
        #     return -1
        # print("Save the depth map and the intensity image.")
        # self.save_callback_images("DepthMapUsingCallback.tiff",
        #                           "IntensityImageUsingCallback.png")


if __name__ == '__main__':
    try:
        a = UseVirtualDevice()
        a.main()
    except IOError as error:
        print(error)
