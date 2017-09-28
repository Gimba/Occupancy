import argparse
import sys

import cpptraj_helper as cpp
import os_helper as os
from input import Input

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
    ip = Input(sys.argv)

    # create output folder
    os.create_output_folder(ip.folder)

    # copy input trajectories and topology files to output folder
    for item in ip.input:
        os.copy_to_folder(item[0], ip.folder)
        os.copy_to_folder(item[1], ip.folder)

    # change to results folder
    os.change_to_folder(ip.folder)
    # set new file paths
    ip.set_file_paths_to_output_folder()

    # generate pdb objects from topologies
    # pdb_file_name_unmutated = cpp.generate_pdb(ip.input[0][0], ip.input[0][1], ip.input[0][2], ip.input[0][3],
    #                                            ip.strip_water, ip.strip_hydro)
    # pdb_unmutated = Pdb(pdb_file_name_unmutated)

    initial_contact_atoms = cpp.get_residue_contacting_atoms(ip.input[0][0], ip.input[0][1], ip.input[0][2],
                                                             ip.input[0][3], ip.mutation, ip.strip_water,
                                                             ip.strip_hydro)
    occupancies = []
    for item in ip.input:
        occupancies.append(cpp.get_occupancy_of_atoms(item[0], item[1], item[2], item[3], initial_contact_atoms,
                                                      ip.mutation, ip.strip_water))
