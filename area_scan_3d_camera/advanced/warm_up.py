#With this sample, you can obtain and save 2D images and point clouds
#periodically for the specified duration from a camera.


import time
import cv2
import time
import threading
import signal
import sys
import random
import argparse
from dataclasses import dataclass
from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *

@dataclass
class IntRange:
    name: str
    min: int
    max: int
    default: int
    unit: str

WARMUP_TIME = IntRange("warmup-time", 15, 90, 30, "minutes")
SAMPLE_INTERVAL = IntRange("sample-interval", 3, 30, 5, "seconds")

WarmupTimeOfLsrsAndUhp = 60
SampleIntervalOfUhp = 3   


class WarmUp:
    def __init__(self, args):
        self.warmup_time_minutes = args.warmup_time
        self.sample_interval_seconds = args.sample_interval
        self.user_set_warmup_time = getattr(args, "warmup_time_user_set", False)
        self.sample_interval_user_set = getattr(args, "sample_interval_user_set", False)
        self.camera = Camera()
        self.stop_flag = threading.Event()
        self.is_capturing = threading.Lock()
        self.original_user_set = ""
        self.warmup_user_set = ""

    def signal_handler(self, sig, frame):
        print("\n[Interrupt] Ctrl+C received. Cleaning up...")
        self.stop_flag.set()

    def connect_camera(self):
        if find_and_connect(self.camera):
            print("Camera connected.")
            return True
        else:
            return False

    def disconnect_camera(self):
        self.camera.disconnect()
        print("Camera disconnected.")

    def get_current_user_set(self):
        error, raw_name = self.camera.current_user_set().get_name()
        try:
            name = raw_name.encode("latin1").decode("utf-8")
        except Exception:
            name = raw_name
        return name

    def create_warmup_group_name(self,group_names, base_name="warmup"):
        if base_name not in group_names:
            return base_name

        while True:
            random_num = random.randint(0, 9999)
            new_name = f"{base_name}_{random_num:04d}"
            if new_name not in group_names:
                return new_name


    def switch_to_warmup_user_set(self):
        status, self.original_user_set = self.camera.current_user_set().get_name()
        if not status.is_ok():
            show_error(status)
            return False
        print(f"[Info] Original user set: {self.original_user_set}")
        
        status = self.camera.user_set_manager().select_user_set("calib")
        if not status.is_ok():
            show_error(status)
            return False
        print(f'Current user set is now "calib".')

        status, user_sets =  self.camera.user_set_manager().get_all_user_set_names()
        if not status.is_ok():
            show_error(status)
            return False
        self.warmup_use_set = self.create_warmup_group_name(user_sets)

        status = self.camera.user_set_manager().add_user_set(self.warmup_use_set)
        if not status.is_ok():
            show_error(status)
            return False

        status = self.camera.user_set_manager().select_user_set(self.warmup_use_set)
        if not status.is_ok():
            show_error(status)
            return False

        print(f"[Info] Switched to user set {self.warmup_use_set}")
        return True
    
    def restore_user_set(self):
        if self.original_user_set:
            print(f'[Restore] Switching back to: "{self.original_user_set}"')
            show_error(
                self.camera.user_set_manager().select_user_set(self.original_user_set),
                f'Select user set "{self.original_user_set}"'
            )
            show_error(
                self.camera.user_set_manager().delete_user_set(self.warmup_use_set),
                f'Delete user set "{self.original_user_set}"'
            )

    def capture_sample(self, sample_count):
        frame_all_2d_3d = Frame2DAnd3D()
        with self.is_capturing:
            status = self.camera.capture_2d_and_3d(frame_all_2d_3d)
            show_error(status)
            if not status.is_ok():
                return False

            status = CameraStatus()
            camera_status_ret = self.camera.get_camera_status(status)
            show_error(camera_status_ret)

            total_seconds = self.warmup_time_minutes * 60
            elapsed_seconds = sample_count * self.sample_interval_seconds
            progress_ratio = min(elapsed_seconds / total_seconds, 1.0)
            progress_percent = progress_ratio * 100

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print("\n" + "-" * 30)
            print(f"[{timestamp}] Warmup sample #{sample_count} completed. [Progress] {progress_percent:.1f}%")
            print_camera_status(status)
            print("-" * 30 + "\n")
        return True

    def warmup_thread_func(self):
        sample_count = 0
        next_capture_time = time.time()

        while not self.stop_flag.is_set():
            now = time.time()
            if now >= next_capture_time:
                if not self.is_capturing.locked():
                    sample_count += 1
                    threading.Thread(target=self.capture_sample, args=(sample_count,), daemon=True).start()
                else:
                    print("[INFO] Previous capture still in progress, skipping this interval.")
                next_capture_time += self.sample_interval_seconds
            time.sleep(0.05)


    def start_warmup(self):
        try:
            print(f"[Config] warmup_time = {self.warmup_time_minutes} min, sample_interval = {self.sample_interval_seconds} sec")
            warmup_thread = threading.Thread(target=self.warmup_thread_func, daemon=True)
            warmup_thread.start()

            deadline = time.time() + self.warmup_time_minutes * 60
            while time.time() < deadline and not self.stop_flag.is_set():
                time.sleep(0.2)

            self.stop_flag.set()
            warmup_thread.join()
            print("[Init] Warmup completed.")

        except Exception as e:
            print(f"[ERROR] Warmup error: {e}")

    def main(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        if not self.connect_camera():
            print("[ERROR] Failed to connect to camera.")
            return
        try:
            if not self.switch_to_warmup_user_set():
                return -1


            info = CameraInfo()
            status = self.camera.get_camera_info(info)
            if(status.is_ok()):
                if info.model == "Mech-Eye LSR S" or "Mech-Eye UHP" in info.model:
                    WARMUP_TIME.default = WarmupTimeOfLsrsAndUhp
                    print(f"[Info] Detected {info.model}, warmup time adjusted to {WARMUP_TIME.default} minutes.") 
                
                if not self.user_set_warmup_time:
                    self.warmup_time_minutes = WARMUP_TIME.default
                    print(f"[Info] Sample interval set to {self.warmup_time_minutes} seconds.")

                if "Mech-Eye UHP" in info.model:
                    SAMPLE_INTERVAL.default = SampleIntervalOfUhp
                    print(f"[Info] Detected {info.model}, interval time adjusted to {SAMPLE_INTERVAL.default} minutes.") 

                if not self.sample_interval_user_set:
                    self.sample_interval_seconds = SAMPLE_INTERVAL.default
                    print(f"[Info] Sample interval set to { self.sample_interval_seconds} seconds.")

            self.start_warmup()
        finally:
            self.restore_user_set()
            self.disconnect_camera()

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
    parser = argparse.ArgumentParser(
        description="Camera Warmup Tool: Periodically captures images to warm up the camera."
    )

    class StoreWithFlag(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, values)
            setattr(namespace, self.dest + "_user_set", True)

    parser.add_argument(
        "-w", "--warmup-time",
        type=restricted_int(WARMUP_TIME),
        default=WARMUP_TIME.default,
        metavar=WARMUP_TIME.unit,
        help=f"Warmup time in {WARMUP_TIME.unit} ({WARMUP_TIME.min}–{WARMUP_TIME.max}), default: {WARMUP_TIME.default} (UHP and LSRS camera default: 60m)",
        action=StoreWithFlag
    )

    parser.add_argument(
        "-i", "--sample-interval",
        type=restricted_int(SAMPLE_INTERVAL),
        default=SAMPLE_INTERVAL.default,
        metavar=SAMPLE_INTERVAL.unit,
        help=(
            f"Sample interval in {SAMPLE_INTERVAL.unit} ({SAMPLE_INTERVAL.min}–{SAMPLE_INTERVAL.max}), "
            f"default: {SAMPLE_INTERVAL.default}. "
            f"(UHP camera default: 3s)"
        ),
        action=StoreWithFlag
    )
    parser.set_defaults(warmup_time_user_set=False)
    parser.set_defaults(sample_interval_user_set=False)
    args = parser.parse_args()
    return args





if __name__ == "__main__":
    args = parse_args()
    warmup = WarmUp(args)
    warmup.main()
