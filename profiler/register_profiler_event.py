# With this sample program, you can register a profiler event, such as profiler disconnected event, and
# respond to the event via a callback function.

from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *


class CustomCallback(EventCallbackBase):
    def __init__(self):
        super().__init__()

    def run(self, event):
        print("A profiler event has occurred. Event ID is {0}.".format(event))


class RegisterProfilerEvent(object):
    def __init__(self):
        self.profiler = Profiler()

    def main(self):
        if not find_and_connect(self.profiler):
            return

        device_event = ProfilerEvent()
        callback = CustomCallback()
        print("Register profiler disconnected event,")
        show_error(device_event.register_profiler_event_callback(
            self.profiler, callback, ProfilerEvent.PROFILER_EVENT_DISCONNECTED))

        self.profiler.disconnect()
        print("Disconnected from the Mech-Eye profiler successfully.")


if __name__ == '__main__':
    a = RegisterProfilerEvent()
    a.main()
