import os
import subprocess
import timeit
from collections import Counter

# executes the cpptraj with the given parameters, outputs of will be written as files specified in the cpptraj file
def run_cpptraj(prmtop, trajin, cpptraj_file):
    cpptraj = 'cpptraj -p ' + prmtop + ' -y ' + trajin + ' -i ' + cpptraj_file + ' > ' + cpptraj_file.replace('.',
                                                                                                              '_') + ".log"
    print cpptraj
    start = timeit.default_timer()
    os.system(cpptraj)
    stop = timeit.default_timer()
    elapsed = round(stop - start)
    minutes = str(int(elapsed / 60))
    seconds = str(int(elapsed % 60))
    print minutes + " minutes " + seconds + " seconds"


# creates a cpptraj file to generate a pdb from the given inputs. Returns name of cpptraj file and name of pdb file.
def create_pdb_cpptraj(prmtop, trajin, strip_water, strip_hydrogen):
    prmtop = prmtop.split('.')[0]
    prmtop = prmtop.split('/')[-1]
    trajin = trajin.split('/')[-1]
    trajin = trajin.replace(' ', '_')
    trajin = trajin.replace('.', '_')
    trajin = trajin.replace('\"', '')
    cpptraj_file = prmtop + "_" + trajin + "_pdb.cpptraj"
    pdb = prmtop + "_" + trajin + ".pdb"
    pdb = pdb.replace("\"", "")

    with open(cpptraj_file, 'w') as f:
        if strip_water:
            f.write('strip :WAT\n')
        if strip_hydrogen:
            f.write('strip @H*\nstrip @?H*\nstrip @Cl-\n')
        f.write('trajout ' + pdb)
        f.write('\ngo')
    return [cpptraj_file, pdb]


# generates pdb file in the working directory from parameters. Returns the name of the pdb file.
def generate_pdb(prmtop, trajin, start_frame, end_frame, strip_water, strip_hydrogen):
    trajin = "\"" + trajin + " " + start_frame + " " + end_frame + "\""
    cpptraj = create_pdb_cpptraj(prmtop, trajin, strip_water, strip_hydrogen)
    run_cpptraj(prmtop, trajin, cpptraj[0])
    pdb_file_name = cpptraj[1]
    return pdb_file_name


# get atoms in contact with atoms of the specified residue
def get_residue_contacting_atoms(prmtop, trajin, start_frame, end_frame, residue, strip_water, strip_hydrogen):
    model_contacts = create_contact_cpptraj(prmtop, trajin, start_frame, end_frame, [residue], ['1-500000'],
                                            strip_water,
                                            strip_hydrogen)
    run_cpptraj(prmtop, trajin, model_contacts[0])
    contact_atoms_init = get_atom_contacts(model_contacts[1], residue)
    atoms = extract_atoms(contact_atoms_init)
    return atoms


# creates a cpptraj infile that contains commands to get native contacts between the list given by res1 and res2 (
# e.g. nativecontacts :47@C :1-5000 writecontacts F2196A_contacts.dat distance 3.9). The name of the file is the
# given topology followed by the trajectory and "_contacts.cpptraj" (e.g. prmtop = F2196A trajin = prod_20.nc ->
# F2196A_prod_20_nc_contacts.cpptraj).
def create_contact_cpptraj(prmtop, trajin, start_frame, end_frame, mask1, mask2, wat, hydro):
    t = trajin.split()
    cpptraj_file = prmtop.split(".")[0] + "_" + t[0].replace(".", "_").strip(
        "\"") + "_" + start_frame + "_" + end_frame + "_contacts.cpptraj"

    out_file = cpptraj_file.replace('cpptraj', 'dat')

    with open(cpptraj_file, 'w') as f:
        if wat:
            f.write('strip :WAT\n')
        if hydro:
            f.write('strip @H*\nstrip @?H*\nstrip @Cl-\n')

        for item1 in mask1:
            # TODO: needs proper handling of a list of masks
            for item2 in mask2:
                f.write('nativecontacts :' + item1 + ' :' + item2 + ' writecontacts ' +
                        out_file + ' distance 3.9\n')
        f.write('go')

    return [cpptraj_file, out_file]


# transform cpptraj writecontacts data from file into list
def get_atom_contacts(data_file, residue):
    contact_atoms = []
    with open(data_file, 'r') as f:
        for line in f:
            if line[0] is not '#':
                # get lines which do not contain the mutation residue as contact itself (only consider extra mutation
                #  residue contacts)
                if "_:" + residue + "@" not in line:
                    # extract residue number from line
                    line = line.split(' ')
                    line = filter(None, line)
                    # line = line[1].split("_")[1]
                    # line = line.split('@')[0]
                    # line = line.replace(':', '')
                    atom = line[1]
                    contacts = line[2]
                    contact_atoms.append([atom, contacts])

    return contact_atoms


# retrieve atoms from a cpptraj data file
def extract_atoms(atoms):
    out = []

    for item in atoms:
        # :23@N_:22@O -> :22@O
        item = item[0].split('_')[1]
        # :22@O -> 22@O
        item = item.replace(':', '')
        if item.split('@')[0] != '23':
            out.append(item)

    # consolidate same entries
    out = list(set(out))

    return out


# get the occupancy of the given atoms
def get_occupancy_of_atoms(prmtop, trajin, start_frame, end_frame, atoms, strip_water, strip_hydrogen):
    cpptraj_file = create_contact_cpptraj(prmtop, trajin, start_frame, end_frame, atoms, ['1-500000'], strip_water,
                                          strip_hydrogen)
    trajin = trajin_start_end(trajin, start_frame, end_frame)
    run_cpptraj(prmtop, trajin, cpptraj_file[0])
    contacts_init = get_atom_contacts(cpptraj_file[1], '')

    # calculate number of frames if range is specified in trajectory
    frames = int(end_frame) - int(start_frame) + 1

    occupancy = get_atom_occupancy(contacts_init, frames)

    return occupancy


def get_atom_occupancy(occupancy_atoms, frames):
    counter = 0.0
    last_atom = ""
    out = []
    for item in occupancy_atoms:
        atom = item[0].split('_')[0]
        contacts = float(item[1])
        if last_atom == "":
            last_atom = atom
        if last_atom == atom:
            counter += contacts
        else:
            out.append([atom, round((counter / frames), 2)])
            counter = 0.0
            last_atom = atom

    return out


def get_trajectory_length(prmtop, trajin):
    cpptraj = 'cpptraj -p ' + prmtop + ' -y ' + trajin + ' -tl'
    proc = subprocess.Popen(cpptraj, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out.split()[-1]


# returns the averages for atoms types given in the topology and trajectory files. Since we are normally not
# interested in the calculation of the occupancy of solvent atoms, these could be excluded by giving appropriate
# residue masks
def get_contact_averages_of_types(prmtop, trajin, start_frame, end_frame, types, mask1, mask2, wat, hydro):
    model_contacts_mutated = create_contact_cpptraj_types(prmtop, trajin, start_frame, end_frame, types, mask1, mask2,
                                                          wat, hydro)
    trajin = trajin_start_end(trajin, start_frame, end_frame)
    run_cpptraj(prmtop, trajin, model_contacts_mutated[0])
    avrgs = get_occupancy_averages_of_types(model_contacts_mutated[1], types)
    return avrgs


# create cpptraj infile to calculate occupancies for given atom types
def create_contact_cpptraj_types(prmtop, trajin, start_frame, end_frame, types, mask1, mask2, wat, hydro):
    t = trajin.split()
    cpptraj_file = prmtop.split(".")[0] + "_" + t[0].replace(".", "_").strip(
        "\"") + "_" + start_frame + "_" + end_frame + "_averages_contacts.cpptraj"
    out_file = cpptraj_file.replace('cpptraj', 'dat')

    with open(cpptraj_file, 'w') as f:
        if wat:
            f.write('strip :WAT\n')
        if hydro:
            f.write('strip @H*\nstrip @?H*\nstrip @Cl-\n')

        for item in types:
            f.write('nativecontacts (:' + mask1 + ')&(@' + item + ') :' + mask2 + ' writecontacts ' + out_file +
                    ' distance 3.9\n')
        f.write('go')

    return [cpptraj_file, out_file]


# get the average of contacts of types from a given cpptraj data file
def get_occupancy_averages_of_types(data_file, types):
    data = read_cpptraj_data_contacts_distance(data_file)

    type_occupancy_average = []
    for item in types:
        residue_types = []
        for line in data:
            temp = line[0][0].split('@')[1]
            if item == temp:
                residue_types.append(line[0][0])
        if len(residue_types) != 0:
            type_occupancies = Counter(residue_types).values()
            average = round(sum(type_occupancies) / float(len(type_occupancies)), 2)
            type_occupancy_average.append([item, average])

    return type_occupancy_average


# reads in the specfied file and returns a list that contains elements consisting of the two contacting atoms and
# their distance to each other (e.g. [[[246@N, 23@C],2.34], [[246@H, 23@CB], 3.12],...]
def read_cpptraj_data_contacts_distance(file_name):
    out = []
    with open(file_name, 'r') as f:
        for line in f:
            if line[0] is not '#':
                line = line.split()
                atom = line[1].replace(':', '')
                atom = atom.split('_')
                dist = float(line[4])
                if atom[0] != atom[1]:
                    out.append([atom, dist])
    return out


# add start and end frames to trajectory
def trajin_start_end(trajin, start_frame, end_frame):
    trajin = "\"" + trajin + " " + start_frame + " " + end_frame + "\""
    return trajin
