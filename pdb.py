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

    # returns a list of the specified keys, which can be given as a list or a string
    def get(self, keys):
        if isinstance(keys, str):
            keys = keys.split()

        if not isinstance(keys, list):
            raise ValueError("Keys have to be given as strings (e.g. \"number type\") or list (e.g. \"[\'number\'"
                             ", \'type\']\")")
        out = []
        for item in self.atoms:
            for key in keys:
                if key in item.keys():
                    out.append(item[key])
                else:
                    raise ValueError(
                        "Key %s not found. Available keys: 'number', 'type', 'residue_type', 'residue_number'"
                        ", 'x', 'y', 'z'" % key)
        return out

    # returns list of atom types
    def get_atom_types(self):
        types = self.get("type")
        types = list(set(types))
        return types

    # returns list of residue numbers as integers
    def get_residue_numbers(self):
        residue_numbers = self.get("residue_number")
        residue_numbers = list(set(residue_numbers))
        residue_numbers = [int(x) for x in residue_numbers]
        residue_numbers = sorted(residue_numbers)
        return residue_numbers
