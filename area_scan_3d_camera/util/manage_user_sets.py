# With this sample, you can manage user sets, such as obtaining the names of all user sets, adding a user set, switching the user set, and saving parameter settings to the user set.

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import find_and_connect


class ManageUserSets(object):
    def __init__(self):
        self.camera = Camera()

    def manage_user_set(self):
        user_set_manager = self.camera.user_set_manager()

        # Obtain the names of all user sets.
        user_set_manager.delete_user_set("NewUserSet")
        print("All user sets: ", end='')
        error, user_sets = user_set_manager.get_all_user_set_names()
        show_error(error)
        for user_set in user_sets:
            print(user_set, end=' ')

        # Obtain the name of the currently selected user set.
        error, name = user_set_manager.current_user_set().get_name()
        show_error(error)
        print("\nCurrent user set: " + str(name))

        # Add a user set.
        new_set = "NewUserSet"
        show_error(user_set_manager.add_user_set(new_set))
        print("Add a new user set : \"{}\".".format(new_set))

        # Select a user set by its name.
        show_error(user_set_manager.select_user_set(new_set))
        print("select \"{}\" as the current user set.".format(new_set))

        show_error(user_set_manager.current_user_set(
        ).save_all_parameters_to_device())
        print("Save all parameters to current user set.")

    def main(self):
        if find_and_connect(self.camera):
            self.manage_user_set()
            self.camera.disconnect()
            print("Disconnected from the camera successfully.")


if __name__ == '__main__':
    a = ManageUserSets()
    a.main()
