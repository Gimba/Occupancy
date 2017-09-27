import os
import timeit


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


# generates pdb file in the working directory from parameters. Returns the name of the pdb file.
def generate_pdb(prmtop, trajin, strip_water, strip_hydrogen):
    cpptraj = create_pdb_cpptraj(prmtop, trajin, strip_water, strip_hydrogen)
    run_cpptraj(prmtop, trajin, cpptraj[0])
    pdb_name = cpptraj[1]
    return pdb_name


# creates a cpptraj file to generate a pdb from the given inputs. Returns name of cpptraj file and name of pdb file.
def create_pdb_cpptraj(prmtop, trajin, strip_water, strip_hydrogen):
    prmtop = prmtop.split('.')[0]
    prmtop = prmtop.split('/')[-1]
    trajin = trajin.split('.')[0]
    trajin = trajin.split('/')[-1]
    cpptraj_file = prmtop + ".cpptraj"
    pdb = prmtop + "_" + trajin + ".pdb"

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
def get_residue_contacting_atoms(prmtop, trajin, residue, strip_water, strip_hydrogen):
    model_contacts = create_contact_cpptraj(trajin, [residue], ['1-500000'], strip_water, strip_hydrogen)
    run_cpptraj(prmtop, trajin, model_contacts[0])
    contact_atoms_init = get_atom_contacts(model_contacts[1], residue)
    atoms = extract_atoms(contact_atoms_init)
    return atoms


# creates a cpptraj infile that contains commands to get native contacts between the list given by res1 and res2 (
# e.g. nativecontacts :47@C :1-5000 writecontacts F2196A_contacts.dat distance 3.9). The name fo the file is the
# given trajin without file extension followed by "_contacts.cpptraj" (e.g. trajin = F2196A.nc ->
# F2196A_contacts.cpptraj). Water, Chlor and hydrogen stripped
def create_contact_cpptraj(trajin, mask1, mask2, wat, hydro):
    t = trajin.split()
    frames = ""
    if len(t) > 1:
        frames = "_" + t[1] + "_" + t[2]
        frames = frames.strip("\"")
    cpptraj_file = t[0].split('.')[0].strip("\"") + "_" + t[0].split('.')[1] + frames + "_contacts.cpptraj"
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


# transform cpptraj writecontacts data file into list
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


# retrieve atoms from a cpptraj outfile
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
