# With this sample, you can obtain and print the laser profiler's information, such as model, serial number, firmware version, and temperatures.

from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import find_and_connect, print_profiler_status, print_profiler_info


class PrintProfilerStatus(object):
    def __init__(self):
        self.profiler = Profiler()
        self.profiler_info = ProfilerInfo()
        self.profiler_status = ProfilerStatus()

    def print_profiler_info(self):
        show_error(self.profiler.get_profiler_info(self.profiler_info))
        print_profiler_info(self.profiler_info)

    def print_profiler_status(self):
        show_error(self.profiler.get_profiler_status(self.profiler_status))
        print_profiler_status(self.profiler_status)

    def main(self):
        if find_and_connect(self.profiler):
            self.print_profiler_info()
            self.print_profiler_status()
            self.profiler.disconnect()
            print("Disconnected from the profiler successfully.")


if __name__ == '__main__':
    a = PrintProfilerStatus()
    a.main()
