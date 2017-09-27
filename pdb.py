class Pdb:
    def __init__(self, file_name):
        self.file_name = file_name
        self.atoms = []
        self.read_pdb_file(self.file_name)

    def read_pdb_file(self, file_name):
        with open(self.file_name, 'r') as f:
            for line in f:
                line = line.split()
                if 'ATOM' in line[0]:
                    self.atoms.append({'number': line[1], 'type': line[2], 'residue_type': line[3], 'residue_number':
                        line[4], 'x': line[5], 'y': line[6], 'z': line[7]})
