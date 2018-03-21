import string        # Python string utilities
import re            # Python regular expression utilities

# MODULE INTRODUCTION
"""This module contains functions and objects relevant to L1 (line-level)
script parsing operations. """

# MODULE VARIABLE DECLARATIONS
B_OPEN = re.compile(r'<b>')      # RegEx signature for opening bold tag
B_CLOSE = re.compile(r'</b>')    # RegEx signature for closing bold tag
TAG = re.compile(r'</?\w+>')     # RegEx signature for html tags in general
PUNC = re.compile(r'[\!-/<-@\[-`\{-~]')
CHAR = re.compile(r'\w')         # RegEx signature for characters
UPPERS = string.ascii_uppercase  # String of all uppercase letters
LOWERS = string.ascii_lowercase  # String of all lowercase letters


class Line(object):
    """Line-level data object for parsing and manipulation. The Line is
    equivalent to the L1 level of the script data structure, and is composed
    of 'data', 'function', 'links', and 'metrics' dictionaries to store
    line-level traits for analysis. 'function' is unique to the Line data
    layer, and is intended to store classification data created by the user
    for training."""

    def __init__(self):  # Initiates empty data object
        # DATA DICTIONARY INITIALIZATION
        self.data = {  # Dictionary holding line string and component data
            'raw': None,
            'fmt': None,
            'map': None,
            'spc': None,
            'rgx': None,
            'pnc': None,
        }

        # FUNCTION DICTIONARY INITIALIZATION
        self.function = {  # Dictionary to capture line function classification
            'action': None,
            'camera': None,
            'character': None,
            'dialogue': None,
            'instruction': None,
            'intro': None,
            'location': None,
            'note': None,
            'scene': None,
            'shot_index': None,
        }

        # LINK DICTIONARY INITIALIZATION
        self.links = {  # Dictionary to store links between data levels
            'L1': None,
            'L2': None,
            'L3': None,
            'L4': None,
            'self': 'L1',
        }

        # METRIC DICTIONARY INITIALIZATION
        self.metrics = {  # Dictionary to store line-level observations
            'length': None,
            'id': None,
        }
        types = ['bold', 'char', 'lower', 'num', 'punc', 'space', 'upper']
        for x in types:
            self.metrics[x] = {
                'has': False,
                'num': 0,
                'pct': 0.,
                'p80': 0.,
            }
        self.metrics['bold'].update(
            {'open': False, 'close': False, 'bolded': None, }
        )

        # STATUS FLAG INITIALIZATION
        self.state = None  # Flag will cycle between None/parse/json/db
