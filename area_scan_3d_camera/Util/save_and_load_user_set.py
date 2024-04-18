# With this sample, you can import and replace all user sets from a JSON file, and save all user sets to a JSON file.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect


class SaveAndLoadUserSet(object):
    def __init__(self):
        self.camera = Camera()
        self.user_set_manager = self.camera.user_set_manager()

    def save_and_load_user_set(self):

        # Obtain the names of all user sets.
        print("All user sets: ", end='')
        error, user_sets = self.user_set_manager.get_all_user_set_names()
        show_error(error)
        for user_set in user_sets:
            print(user_set, end=' ')

        print("Save all user sets to a JSON file.")
        show_error(self.user_set_manager.save_to_file("camera_config.json"))

        print("Import and replace all user sets from a JSON file.")
        show_error(self.user_set_manager.load_from_file("camera_config.json"))

    def main(self):
        if find_and_connect(self.camera):
            self.save_and_load_user_set()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = SaveAndLoadUserSet()
    a.main()
