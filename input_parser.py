import argparse

class InputParser():
    def __init__(self, argv):
        self.argv = argv
        if not isinstance(argv,list):
            raise TypeError("Input has to be of type list. Given: %s" % type(argv))
