import os


def create_output_folder(folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    except OSError:
        raise OSError("Could not create folder %s" % folder_name)


def copy_to_folder(f, folder):
    try:
        os.system("cp " + f + " " + folder)
    except OSError:
        raise OSError("Could not copy %s to folder %s" % f % folder)


def change_to_folder(folder):
    os.chdir(os.getcwd() + '/' + folder)
