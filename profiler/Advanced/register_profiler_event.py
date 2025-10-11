# With this sample, you can define and register the callback function for monitoring the profiler connection status.
import time
from datetime import datetime

from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *


# Define the callback class for handling the events
class CustomCallback(EventCallbackBase):
    def __init__(self):
        super().__init__()

    def process_event(self, event_data: EventData, extra_payload: Payload):
        print("A profiler event has occurred.")
        print("\tEvent ID: {0}".format(event_data.event_id))
        print("\tEvent Name: {0}".format(event_data.event_name))
        print("\tTimestamp: {0}".format(
            datetime.fromtimestamp(event_data.timestamp / 1000)))
        for member in extra_payload:
            if member.type == PayloadMember.Type__UInt32:
                print("\t{0} : {1}".format(
                    member.name, member.value.uint_32value))
            elif member.type == PayloadMember.Type__Int32:
                print("\t{0} : {1}".format(
                    member.name, member.value.int_32value))
            elif member.type == PayloadMember.Type__Int64:
                print("\t{0} : {1}".format(
                    member.name, member.value.int_64value))
            elif member.type == PayloadMember.Type__Float:
                print("\t{0} : {1}".format(
                    member.name, member.value.float_value))
            elif member.type == PayloadMember.Type__Double:
                print("\t{0} : {1}".format(
                    member.name, member.value.double_value))
            elif member.type == PayloadMember.Type__Bool:
                print("\t{0} : {1}".format(
                    member.name, member.value.bool_value))
            elif member.type == PayloadMember.Type__String:
                print("\t{0} : {1}".format(
                    member.name, member.value.string_value))


class RegisterProfilerEvent(object):
    def __init__(self):
        self.profiler = Profiler()

    def register_events(self):
        supported_events = EventInfos()
        show_error(ProfilerEvent.get_supported_events(
            self.profiler, supported_events))
        profiler_event = ProfilerEvent()
        self.callback = CustomCallback()
        print("\nEvents supported by this profiler")
        for event_info in supported_events:
            print()
            print(event_info.event_name, event_info.event_id)
            print("Register the callback function for the event ",
                  event_info.event_name)
            show_error(profiler_event.register_profiler_event_callback(
                self.profiler, event_info.event_id, self.callback))
        print()

    def get_parameters(self):
        self.user_set = self.profiler.current_user_set()

        # Get the number of data points in each profile
        error, self.data_width = self.user_set.get_int_value(
            DataPointsPerProfile.name)
        show_error(error)

        # Ge the current value of the "Scan Line Count" parameter
        error, self.capture_line_count = self.user_set.get_int_value(
            ScanLineCount.name)
        show_error(error)

        error, data_acquisition_trigger_source = self.user_set.get_enum_value(
            DataAcquisitionTriggerSource.name)
        show_error(error)
        self.is_software_trigger = data_acquisition_trigger_source == DataAcquisitionTriggerSource.Value_Software

    def acquire_profile_data(self) -> bool:
        """
        Call start_acquisition() to set the laser profiler to the acquisition-ready status, and
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
                time.sleep(0.2)
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
            return

        # Set the heartbeat interval to 2 seconds
        show_error(self.profiler.set_heartbeat_interval(2000))

        self.register_events()

        # The program pauses for 20 seconds to allow the user to test if the profiler disconnection
        # event works properly. If the network cable is unplugged, the disconnection will be detected
        # and the callback function will be triggered.
        print("Wait for 20 seconds for disconnect event.")
        time.sleep(20)

        if not confirm_capture():
            return 0

        self.get_parameters()
        self.profile_batch = ProfileBatch(self.data_width)

        # Acquire profile data without using callback
        if not self.acquire_profile_data():
            return -1

        self.profiler.disconnect()
        print("Disconnected from the profiler successfully.")


if __name__ == '__main__':
    a = RegisterProfilerEvent()
    a.main()
