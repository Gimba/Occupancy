import argparse
import os
import sys

from input_parser import Inputs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-r', '--residue', help='investigated residue')
    parser.add_argument('-i', '--input', nargs='?',
                        help='list of inputs (e.g. model1.prmtop model1.incprd, mutation.prmtop, prod_1.nc 1 20, ...')
    parser.add_argument('-a', '--avrgs', help='calculate averages', action='store_true')
    parser.add_argument('-w', '--wat', help='strip water', action='store_true')
    parser.add_argument('-hy', '--hydro', help='strip hydrogen', action='store_true')
    args = parser.parse_args()

    ip = Inputs(sys.argv)


def create_output_folder(folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    except OSError:
        raise OSError("Could not create folder %s" % folder_name)
