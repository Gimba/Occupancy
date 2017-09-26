import argparse
import sys

import os_helper as os
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

    # parse inputs into input object
    ip = Inputs(sys.argv)

    # create output folder
    os.create_output_folder(ip.folder)

    # copy input trajectories and topology files to output folder
    for item in ip.input:
        os.copy_to_folder(item, ip.folder)
