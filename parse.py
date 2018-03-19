import pandas as pd                    # Data handling
import numpy as np                     # Math utilities
import string                          # String utilities
import json                            # JSON handling
import re                              # Regular expressions
from bs4 import BeautifulSoup as soup  # BeautifulSoup object


class Line(object):
    """Object used to hold line-level data for parsing and manipulation."""

    # Declare class variables used for parsing operations
    bold_open = re.compile(r'<b>')    # RegEx signature for opening bold tag
    bold_close = re.compile(r'</b>')  # RegEx signature for closing bold tag
    uppers = string.ascii_uppercase   # String of all uppercase letters
    lowers = atring.ascii_lowercase   # String of all lowercase letters

    def __init__(self, data=None, display=None, map=None, tokens={}, metrics={}, targets=None):
        # Initialize Line-level data structures
        self.data = data        # Store input string as 'raw'
        self.display = display  # Create placeholder for 'display' data
        self.map = map          # Create placeholder for 'map' data

        # Initialize Line-level measurement data structures
        self.tokens = tokens    # Create token dictionary
        self.metrics = metrics  # Create metric dictionary

        # Initialize categorical target data strcture
        self.targets = targets  # Create placeholder for target categories

    def fit(self):
        self.parse_bold()
        return True

    def parse_bold(self):
        test_open = re.findall(self.bold_open, self.data)
        test_close = re.findall(self.bold_close, self.data)
        self.bolded = (0, len(self.data))

        if len(test_open) == 0:
            self.bolded = (self.bolded[1], self.bolded[1])
        elif len(test_open) == 1:
            self.bolded = self.bolded = (test_open.end(), self.bolded[1])
        else:
            print("ERR: {} bold open tags found in line.".format(len(test_open)))

        if len(test_close) == 0:
            self.bolded = self.bolded = (self.bolded[0], self.bolded[0])
        elif len(test_open) == 1:
            self.bolded = (self.bolded[0], test_close.start())
        else:
            print("ERR: {} bold close tags found in line.".format(len(test_close)))
