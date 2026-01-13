# actions.py
import argparse
import sys

class RunCommand(argparse.Action):
    def __init__(self, option_strings, dest, function=None, **kwargs):
        self.function = function
        super().__init__(option_strings, dest, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        self.function()
        sys.exit(0)
