#With this sample, you can periodically trigger data acquisition with signals input from an external
#device at a fixed scan rate to warm up the Mech-Eye Profiler, while the acquired data is used only
#for stabilization and not saved.

from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *
import cv2
import argparse
import signal
import sys
import threading
import time
import random
import numpy as np
from time import sleep
from threading import Lock
from datetime import datetime
from dataclasses import dataclass
mutex = Lock()
is_capturing = False
@dataclass
class IntRange:
    name: str
    min: int
    max: int
    default: int
    unit: str

WARMUP_TIME = IntRange("warmup-time", 30, 90, 30, "minutes")
SAMPLE_INTERVAL = IntRange("sample-interval", 3, 30, 5, "seconds")

class WarmupAcquisitionCallback(AcquisitionCallbackBase):
    def __init__(self, width):
        super().__init__()
        self.profile_batch = ProfileBatch(width)
        self.sample_count = 0
        self.sample_interval = 0
        self.warmup_minutes = 0
        self.profiler = None
    def run(self, batch):
        global is_capturing
        if not batch.get_error_status().is_ok():
            print("[Error] Data acquisition error.")
            show_error(batch.get_error_status())
            with mutex:
                is_capturing = False
            return

        self.profile_batch.append(batch)
        self.sample_count += 1
        total_seconds = self.warmup_minutes * 60
        elapsed_seconds = self.sample_count * self.sample_interval
        progress_ratio = min(elapsed_seconds / total_seconds, 1.0)
        progress_percent = progress_ratio * 100
        status = ProfilerStatus()
        camera_status_ret = self.profiler.get_profiler_status(status)
        show_error(camera_status_ret)
        print("\n" + "-" * 30)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Warmup sample #{self.sample_count} completed. [Progress] {progress_percent:.1f}%")
        print_profiler_status(status)
        print("-" * 30 + "\n")
        with mutex:
            is_capturing = False


class ProfilerWarmup:
    def __init__(self, warmup_minutes=WARMUP_TIME.default, sample_interval=SAMPLE_INTERVAL.default):
        self.profiler = Profiler()
        self.warmup_minutes = warmup_minutes
        self.sample_interval = sample_interval
        self.stop_flag = threading.Event()
        self.original_user_set = ""
        self.warmup_use_set = ""
        self.current_batch = None
        self.callback = None

    def handle_interrupt(self, signum, frame):
        print("\n[Interrupt] Ctrl+C received, stopping warmup...")
        self.stop_flag.set()

    def create_warmup_group_name(self,group_names, base_name="warmup"):
        if base_name not in group_names:
            return base_name

        while True:
            random_num = random.randint(0, 9999)
            new_name = f"{base_name}_{random_num:04d}"
            if new_name not in group_names:
                return new_name

    def switch_to_warmup_user_set(self):
        status, name = self.profiler.current_user_set().get_name()
        if not status.is_ok():
            show_error(status)
            return False
        self.original_user_set = name
        print(f"[Info] Original user set: {name}")

        status, user_sets =  self.profiler.user_set_manager().get_all_user_set_names()
        if not status.is_ok():
            show_error(status)
            return False
        self.warmup_use_set = self.create_warmup_group_name(user_sets)

        status = self.profiler.user_set_manager().add_user_set(self.warmup_use_set)
        if not status.is_ok():
            show_error(status)
            return False

        status = self.profiler.user_set_manager().select_user_set(self.warmup_use_set)
        if not status.is_ok():
            show_error(status)
            return False

        print(f"[Info] Switched to user set {self.warmup_use_set}")
        return True

    def set_warmup_params(self):
        user_set = self.profiler.current_user_set()
        status = user_set.set_enum_value(LineScanTriggerSource.name, LineScanTriggerSource.Value_FixedRate)  # FixedRate
        if not status.is_ok():
            show_error(status)
            return False

        status = user_set.set_enum_value(DataAcquisitionTriggerSource.name, DataAcquisitionTriggerSource.Value_Software)  # Software
        if not status.is_ok():
            show_error(status)
            return False

        status = user_set.set_enum_value(DataAcquisitionMethod.name, DataAcquisitionMethod.Value_Frame_Based)  # Frame_Based
        if not status.is_ok():
            show_error(status)
            return False

        return True

    def interactive_set_scan_params(self):
        print("[Info] Entering interactive scan parameter input...")

        user_set = self.profiler.current_user_set()
        _, current_line_count = user_set.get_int_value(ScanLineCount.name)
        _, current_frequency = user_set.get_float_value(SoftwareTriggerRate.name)
        max_line_count = 20000
        min_line_count = 1
        _, max_trigger_rate = user_set.get_float_value(MaxScanRate.name)
        min_trigger_rate = 2.0

        scan_line_count = self._get_int_input_within_range_or_default(
            prompt=(
                f"Please input scan line count (integer, current: {current_line_count}, "
                f"range: {min_line_count}-{max_line_count}): "
            ),
            default=current_line_count,
            min_val=min_line_count,
            max_val=max_line_count,
            error_msg="Invalid input. Please enter an integer within valid range."
        )
        scan_frequency = self._get_float_input_within_range_or_default(
            prompt=(
                f"Please input scan frequency (Hz, float, current: {current_frequency}, "
                f"range: {min_trigger_rate}-{max_trigger_rate}): "
            ),
            default=current_frequency,
            min_val=min_trigger_rate,
            max_val=max_trigger_rate,
            error_msg="Invalid input. Please enter a float within valid range."
        )
        print(f"[Info] Received parameters: scanLineCount = {scan_line_count}, scanFrequency = {scan_frequency} Hz")
        status = user_set.set_int_value(ScanLineCount.name, scan_line_count)
        if not status.is_ok():
            show_error(status)
            return False
        status = user_set.set_float_value(SoftwareTriggerRate.name, scan_frequency)
        if not status.is_ok():
            show_error(status)
            return False
        return True


    def _get_int_input_within_range_or_default(self, prompt, default, min_val, max_val, error_msg):
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input == "":
                    return default
                value = int(user_input)
                if min_val <= value <= max_val:
                    return value
                print(error_msg)
            except ValueError:
                print(error_msg)

    def _get_float_input_within_range_or_default(self, prompt, default, min_val, max_val, error_msg):
        while True:
            try:
                user_input = input(prompt).strip()
                if user_input == "":
                    return default
                value = float(user_input)
                if min_val <= value <= max_val:
                    return value
                print(error_msg)
            except ValueError:
                print(error_msg)

    def prepare_callback(self):
        status, data_width = self.profiler.current_user_set().get_int_value(DataPointsPerProfile.name)
        if not status.is_ok():
            show_error(status)
            return False

        self.current_batch = ProfileBatch(data_width)
        self.callback = WarmupAcquisitionCallback(data_width)
        self.callback.profiler = self.profiler 
        self.callback.sample_interval = self.sample_interval
        self.callback.warmup_minutes = self.warmup_minutes
        status = self.profiler.register_acquisition_callback(self.callback)
        if not status.is_ok():
            show_error(status)
            return False

        return True

    def warmup_thread_func(self):
        global is_capturing
        start_time = time.monotonic()
        end_time = start_time + self.warmup_minutes * 60

        status = self.profiler.start_acquisition()
        if not status.is_ok():
            show_error(status)
            self.stop_flag.set()
            return

        while not self.stop_flag.is_set() and time.monotonic() < end_time:
            with mutex:
                if is_capturing:
                    print("[Warning] Previous capture not finished, skipping this cycle.")
                    continue
                is_capturing = True

            def capture():
                    status = self.profiler.trigger_software()
                    if not status.is_ok():
                        show_error(status)
            threading.Thread(target=capture).start()

            waited = 0
            interval = 0.1
            while waited < self.sample_interval and not self.stop_flag.is_set():
                time.sleep(interval)
                waited += interval

        status = self.profiler.stop_acquisition()
        if not status.is_ok():
            show_error(status)

        print("[Info] Warmup loop ended.")

    def start_warmup(self):
        try:
            print(f"[Config] warmup_time = {self.warmup_minutes} min, sample_interval = {self.sample_interval} sec")
            warmup_thread = threading.Thread(target=self.warmup_thread_func, daemon=True)
            warmup_thread.start()

            deadline = time.time() + self.warmup_minutes * 60
            while time.time() < deadline and not self.stop_flag.is_set():
                time.sleep(0.2)

            self.stop_flag.set()
            warmup_thread.join()
            print("[Info] Warmup completed.")
            return True

        except Exception as e:
            print(f"[Error] Warmup error: {e}")
            return False

    def cleanup(self):
        try:
            if self.original_user_set:
                try:
                    self.profiler.user_set_manager().select_user_set(self.original_user_set)
                    print(f"[Info] Restored user set to '{self.original_user_set}'")
                except Exception as e:
                    print(f"[Error] Failed to restore user set: {e}")

                try:
                    self.profiler.user_set_manager().delete_user_set(self.warmup_use_set)
                    print(f"[Info] Deleted '{self.warmup_use_set}' user set")
                except Exception as e:
                    print(f"[Error] Failed to delete '{self.warmup_use_set}' user set: {e}")

        except Exception as e:
            print(f"[Error] Exception during cleanup: {e}")

        self.profiler.disconnect()
        print("[Info] Profiler disconnected.")

    def main(self):
        signal.signal(signal.SIGINT, self.handle_interrupt)

        if not find_and_connect(self.profiler):
            print("[Error] Failed to connect to profiler.")
            return -1

        try:
            if not self.switch_to_warmup_user_set():
                return -1

            if not self.set_warmup_params():
                return -1

            if not self.interactive_set_scan_params():
                return -1

            if not self.prepare_callback():
                return -1

            if not self.start_warmup():
                return -1

            print("[Info] Warmup finished.")
            return 0
        finally:
            self.cleanup()



def restricted_int(range_def: IntRange):
    def checker(val):
        try:
            val = int(val)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{range_def.name} must be an integer.")
        if val < range_def.min or val > range_def.max:
            raise argparse.ArgumentTypeError(
                f"{range_def.name} must be between {range_def.min} and {range_def.max}"
            )
        return val
    return checker

def parse_args():
    parser = argparse.ArgumentParser(description="LNX Profiler Warmup Tool")

    parser.add_argument(
        "-w", "--warmup-time",
        type=restricted_int(WARMUP_TIME),
        default=WARMUP_TIME.default,
        metavar=WARMUP_TIME.unit,
        help=f"Warmup time in {WARMUP_TIME.unit} ({WARMUP_TIME.min}–{WARMUP_TIME.max}), default: {WARMUP_TIME.default}"
    )

    parser.add_argument(
        "-i", "--sample-interval",
        type=restricted_int(SAMPLE_INTERVAL),
        default=SAMPLE_INTERVAL.default,
        metavar=SAMPLE_INTERVAL.unit,
        help=f"Sample interval in {SAMPLE_INTERVAL.unit} ({SAMPLE_INTERVAL.min}–{SAMPLE_INTERVAL.max}), default: {SAMPLE_INTERVAL.default}"
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    warmup_tool = ProfilerWarmup(warmup_minutes=args.warmup_time, sample_interval=args.sample_interval)
    sys.exit(warmup_tool.main())
