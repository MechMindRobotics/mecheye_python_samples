# With this sample, you can manage user sets, such as obtaining the names of all user sets, adding a user set, switching the user set, and saving parameter settings to the user set.

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

        success_message = "Set \\" + \
            user_sets[0] + "\\ as the current user set."
        show_error(user_set_manager.select_user_set(
            user_sets[0]), success_message)

        success_message = "Save all parameters to current user set."
        show_error(current_user_set.save_all_parameters_to_device(),
                   success_message)

        self.profiler.disconnect()
        print("Disconnected from the Mech-Eye Profiler successfully")


if __name__ == '__main__':
    a = ManageUserSets()
    a.main()
