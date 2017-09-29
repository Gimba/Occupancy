import argparse
import sys

import cpptraj_helper as cpp
import os_helper as os
from input import Input
from list_helper import *
from pdb import Pdb

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

    ##### calculate occupancies #####
    initial_contact_atoms = cpp.get_residue_contacting_atoms(ip.input[0][0], ip.input[0][1], ip.input[0][2],
                                                             ip.input[0][3], ip.mutation, ip.strip_water,
                                                             ip.strip_hydro)
    occupancies = []
    for item in ip.input:
        occupancies.append(cpp.get_occupancy_of_atoms(item[0], item[1], item[2], item[3], initial_contact_atoms,
                                                      ip.mutation, ip.strip_water))

    ##### calculate average occupancies #####
    if ip.calc_averages:

        # generate pdb to get non solvent residues
        pdb_file_name = cpp.generate_pdb(ip.input[0][0], ip.input[0][1], "1", "1", 1, 1)
        pdb = Pdb(pdb_file_name)

        # get non solvent residue numbers to create mask to exclude solvent in calculation of averages
        non_solvent_residues = pdb.get_non_solvent_residue_numbers()
        mask1 = str(non_solvent_residues[0]) + "-" + str(non_solvent_residues[-1])
        mask2 = "1-50000"

        # get types of contacting atoms
        contacting_atoms_types = pdb.get_atom_types(initial_contact_atoms)

        averages = []
        for item in ip.input:
            averages.append(cpp.get_contact_averages_of_types(item[0], item[1], item[2], item[3], contacting_atoms_types
                                                              , mask1, mask2, ip.strip_water, ip.strip_hydro))

    ##### reformat data #####
    occupancies = reformat_occupancies_list(occupancies)

    if ip.calc_averages:
        for item in averages:
            occupancies = add_averages_column(occupancies, item)

    # add headers
    output = add_headers(occupancies, ip.calc_averages)

    # format output
    output = output_2D_list(output)
    output = prepare_output(output, ip.calc_averages)

    ##### write data #####
    input_file_names = ip.get_file_names()
    write_output(output, ip.mutation + '_occupancies.dat')
    output_to_pdf(output, ip.mutation + '_occupancies.dat', ip.calc_averages, ip.strip_water, ip.strip_hydro,
                  input_file_names, ip.mutation)
