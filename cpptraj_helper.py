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
def generate_pdb(prmtop, trajin, wat, hydro):
    cpptraj = create_pdb_cpptraj(prmtop, trajin, wat, hydro)
    run_cpptraj(prmtop, trajin, cpptraj[0])
    pdb_name = cpptraj[1]
    return pdb_name


# creates a cpptraj file to generate a pdb from the given inputs. Returns name of cpptraj file and name of pdb file.
# Water, Chlor and hydrogen stripped
def create_pdb_cpptraj(prmtop, trajin, wat, hydro):
    prmtop = prmtop.split('.')[0]
    prmtop = prmtop.split('/')[-1]
    trajin = trajin.split('.')[0]
    trajin = trajin.split('/')[-1]
    cpptraj_file = prmtop + "_cpptraj"
    pdb = prmtop + "_" + trajin + ".pdb"

    with open(cpptraj_file, 'w') as f:
        if wat:
            f.write('strip :WAT\n')
        if hydro:
            f.write('strip @H*\nstrip @?H*\nstrip @Cl-\n')
        f.write('trajout ' + pdb)
        f.write('\ngo')
    return [cpptraj_file, pdb]
