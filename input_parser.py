import argparse

class InputParser():
    def __init__(self, argv):
        self.argv = argv
        if not isinstance(argv,list):
            raise TypeError("Input has to be of type list. Given: %s" % type(argv))

        if len(argv) < 2:
            raise TypeError("At least two arguments needed. Given: %d" % len(argv))

        if len(argv) > 5:
            raise TypeError("A maximum of 5 arguments is allowed. Given: %d" % len(argv))
