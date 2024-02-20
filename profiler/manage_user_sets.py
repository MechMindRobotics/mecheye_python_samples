from mecheye.shared import *
from mecheye.profiler import *
from mecheye.profiler_utils import *


class ManageUserSets(object):
    def __init__(self):
        self.profiler = Profiler()

    def main(self):
        if not find_and_connect(self.profiler):
            return

        user_set_manager = self.profiler.user_set_manager()
        error, user_sets = user_set_manager.get_all_user_set_names()
        show_error(error)

        print("All user sets: ")
        for user_set in user_sets:
            print(user_set)

        current_user_set = self.profiler.current_user_set()
        error, name = current_user_set.get_name()
        print("Current user set: ", name)

        show_error(user_set_manager.select_user_set(user_sets[0]))
        print("Set \\", user_sets[0], "\\ as the current user set.")

        show_error(current_user_set.save_all_parameters_to_device())
        print("Save all parameters to current user set.")

        self.profiler.disconnect()
        print("Disconnected form the Mech-Eye Profiler successfully")

if __name__ == '__main__':
    a = ManageUserSets()
    a.main()