import string        # Python string utilities
import re            # Python regular expression utilities


# Module variable declarations
B_OPEN = re.compile(r'<b>')      # RegEx signature for opening bold tag
B_CLOSE = re.compile(r'</b>')    # RegEx signature for closing bold tag
TAG = re.compile(r'</?\w+>')     # RegEx signature for html tags in general
UPPERS = string.ascii_uppercase  # String of all uppercase letters
LOWERS = string.ascii_lowercase  # String of all lowercase letters


class Line(object):
    """Object used to hold line-level data for parsing and manipulation."""

    def __init__(self):
        self.data = {
            'raw': None,
            'fmt': None,
            'map': None,
            'spc': None,
            'rgx': None,
            'pnc': None,
        }
        self.function = {
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
        self.links = {
            'L1': None,
            'L2': None,
            'L3': None,
            'L4': None,
        }
        self.metrics = {
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
