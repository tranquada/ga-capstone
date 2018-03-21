import string        # Python string utilities
import re            # Python regular expression utilities

# MODULE INTRODUCTION
"""This module contains functions and objects relevant to L1 (line-level)
script parsing operations. """

# MODULE VARIABLE DECLARATIONS
B_OPEN = re.compile(r'<b>')              # RegEx signature for opening bold tag
B_CLOSE = re.compile(r'</b>')            # RegEx signature for closing bold tag
TAG = re.compile(r'</?\w+>')             # RegEx signature for html tags
PUNC = re.compile(r'[\!-/<-@\[-`\{-~]')  # RegEx signature for punctuation
NUM = re.compile(r'[0-9]')               # RegEx signature for numbers
CHAR = re.compile(r'\w')                 # RegEx signature for characters
UPPERS = string.ascii_uppercase          # String of all uppercase letters
LOWERS = string.ascii_lowercase          # String of all lowercase letters


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
            'num': None,
        }

        # FUNCTION DICTIONARY INITIALIZATION
        self.function = {  # Dictionary to capture line function classification
            'action': None,
            'blank': None,
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
        self.metrics['space'].update(
            {'lead': 0}
        )

        # STATUS FLAG INITIALIZATION
        self.state = None  # Flag will cycle between None/parse/json/db

    def parse(self, idx, line):
        """Parses line information from a raw line string with an index."""

        # 1. BASIC LINE INFORMATION
        # ---------------------------------------------------------------------
        # Set data.raw to line data input
        self.data['raw'] = line

        # Set metrics.id and metrics.length based on input
        self.metrics['id'] = idx + .1
        self.metrics['length'] = len(line)

        # Set L1 links information
        self.links['L1'] = self.metrics['id']

        # 2. EMPTY LINE TEST
        # ---------------------------------------------------------------------
        if len(line) == 0:
            # Set function.empty to True
            self.function['empty'] = True
            return

        # 3. BOLD CHECK ROUTINE
        # ---------------------------------------------------------------------
        self.parse_bold()

        # 4. CHARACTER PARSING ROUTINE
        # ---------------------------------------------------------------------
        log = self.parse_chars()

        # 5. GENERATING REPRESENTATIONAL DATA
        # ---------------------------------------------------------------------
        self.data['fmt'] = self.generate_fmt()
        self.data['rgx'] = self.generate_rgx()

        print(log)

    def parse_bold(self):
        """Extracts information on bolded characters and tags in line."""

        # Initialize working variables
        bold = self.metrics['bold']
        data = self.data['raw']

        # Check for opening tags
        if B_OPEN.match(data) is not None:
            bold['open'] = True
            bold['bolded'] = (B_OPEN.match(data).end(), len(data))
            bold['has'] = True

        if B_CLOSE.match(data) is not None:
            bold['close'] = True
            if bold['bolded'] is None:
                bold['bolded'] = (0, B_CLOSE.match(data).start())
                if bold['bolded'][1] - bold['bolded'][0] > 0:
                    bold['has'] = True
            else:
                bold['bolded'][1] = B_CLOSE.match(data).start()

        # Set remaining metrics
        bold['num'] = bold['bolded'][1] - bold['bolded'][0]
        bold['pct'] = bold['num']/len(data)
        bold['p80'] = bold['num']/80.

    def parse_chars(self):
        """Extracts information on characters using helper functions."""

        # Initiate working variables
        char_map = ''    # Stores mapping of abstract character types
        char_spc = []    # Stores a list of tuples for spacings / (start, end)
        char_pnc = {}    # Stores a dict of punctuaton / punc:(count,[locs])
        char_num = []    # Stores a list of tuples for numbers / (start, num)
        char_err = []    # Stores a list of tuples for errors / (pos, char)
        cnt_spc = 0      # Space counter
        cnt_char = 0     # Character counter
        cnt_pnc = 0      # Punctuation counter
        cnt_num = 0      # Number counter
        cnt_lower = 0    # Lowercase character counter
        cnt_upper = 0    # Uppercase character counter
        cnt_err = 0      # Error counter
        previous = None  # Tracks previous character processed
        html = False     # Flag to signal if inside html tag
        bold = False     # Flag to signal if character is bold

        # Initiate loop
        for pos, c in enumerate(self.data['raw']):
            bold = self.is_bold(pos)
            if c.isspace():
                char_map += '_'
                if previous != ' ':
                    char_spc.append((pos, pos))
                else:
                    char_spc[-1][1] += 1
                cnt_spc += 1
            elif PUNC.match(c) is not None:
                if c in char_pnc.keys():
                    char_pnc[c][0] += 1
                    char_pnc[c][1].append(pos)
                else:
                    char_pnc[c] = (1, [pos])
                if self.is_tag(c):
                    char_map += 'H'
                    if c == '<':
                        html = True
                    if c == '>':
                        html = False
                else:
                    char_map += 'P'
                cnt_pnc += 1
                cnt_char += 1
            elif NUM.match(c) is not None:
                if bold:
                    char_map += 'N'
                else:
                    char_map += 'n'
                if NUM.match(previous) is None:
                    char_num.append((str(c), pos))
                else:
                    char_num[-1][0] += str(c)
                cnt_num += 1
                cnt_char += 1
            elif CHAR.match(c) is not None:
                cnt_char += 1
                if html:
                    char_map += c
                else:
                    if c.isupper():
                        if bold:
                            char_map += 'U'
                        else:
                            char_map += 'u'
                        cnt_upper += 1
                    else:
                        if bold:
                            char_map += 'L'
                        else:
                            char_map += 'l'
                        cnt_lower += 1
            else:
                if bold:
                    char_map += 'E'
                else:
                    char_map += 'e'
                char_err.append((c, pos))
                cnt_err += 1
                cnt_char += 1
            previous = c

        # Update metrics
        self.update_metric('char', cnt_char)
        self.update_metric('lower', cnt_lower)
        self.update_metric('num', cnt_num)
        self.update_metric('punc', cnt_pnc)
        self.update_metric('space', cnt_spc)
        self.update_metric('upper', cnt_upper)

        # Update data
        self.data['map'] = char_map
        self.data['num'] = char_num
        self.data['pnc'] = char_pnc
        self.data['spc'] = char_spc
        self.data['fmt'] = self.parse_fmt()
        self.data['rgx'] = self.parse_rgx()

        # Return error info for log
        return char_err

    def parse_fmt(self):
        return ''

    def parse_rgx(self):
        return ''

    def is_bold(self, pos):
        """Checks the bolding status during character parsing."""

        if self.metrics['bold']['bolded'] is None:
            return False
        else:
            bold_range = [num for num in range(
                self.metrics['bold']['bolded'][0],
                self.metrics['bold']['bolded'][1]
            )]
            if pos in bold_range:
                return True
            else:
                return False

    def is_tag(c):
        if c == '<':
            return True
        elif c == '>':
            return True
        else:
            return False
