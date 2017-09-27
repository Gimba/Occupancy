import os


def create_output_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def copy_to_folder(f, folder):
    os.system("cp " + f + " " + folder)


def change_to_folder(folder):
    os.chdir(os.getcwd() + '/' + folder)
