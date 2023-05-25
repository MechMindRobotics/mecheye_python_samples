# With this sample program, you can perform functions related to parameter groups, such as getting the
# names of available parameter groups, switching parameter group, and saving the current parameter
# values to a specific parameter group. The parameter group feature allows user to save and quickly
# apply a set of parameter values.

import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from MechEye import Device
from source import Common


class SetUserSets(object):
    def __init__(self):
        self.device = Device()

    def set_user_sets(self):
        print("All user sets: ", end='')
        user_sets = self.device.get_all_user_sets()
        for user_set in user_sets:
            print(user_set, end=' ')

        current_user_set = self.device.get_current_user_set()
        print("\nCurrent user set: " + str(current_user_set))

        Common.show_error(self.device.set_current_user_set(user_sets[0]))
        print("Set {} as the current user set.".format(user_sets[0]))

        self.device.save_all_settings_to_user_set()
        print("Save all parameters to current user set.")

        self.device.disconnect()
        print("Disconnected from the Mech-Eye device successfully.")

    def main(self):
        Common.find_camera_list(self)
        if Common.choose_camera_and_connect(self):
            self.set_user_sets()


if __name__ == '__main__':
    a = SetUserSets()
    a.main()
