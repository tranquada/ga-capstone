from jinja2 import Environment, PackageLoader, select_autoescape
from IPython.display import HTML

# MODULE INTRODUCTION
"""This module contains dislay functions to render the different data layers
using Jinja2 templates and IPython rendering methods for Jupyter Notebook."""

# GLOBAL VARIABLE DECLARATIONS
ENV = Environment(
    loader=PackageLoader('ga-capstone', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def div(format, data):  # HTML formatting utility function
    """Wraps 'data' inside a div of class 'format' for HTML printing."""

    d = '<div class="{}">{}</div>'  # Basic div template
    return d.format(format, data)


def char(i, char, map_char, state):
    """Formats character information for html display. state can be
    [blank/bold/plain/tag]."""

    top = div(map_char, char)  # Create div for top part with characetr
    bottom = div(state, i)     # Create div for botm part with index
    filling = top + bottom     # Stick th two together to fill the charbox
    return div('charbox', filling)


def line(raw, char_map, states, pad=True):
    """Formats line information for html display. 'raw' should come from
    data.raw, and 'char_map' should come from styler(data.map). pad=True will
    add black squares to fill the row up to 80 characters."""

    filling = ''
    for i, (c, m, s) in zip(raw, char_map, states):
        filling += char(i, c, m, s)

    if pad:  # Check line length and initialize pad_length if creating a pad
        pad_length = 80 - len(raw)
        for x in range(pad_length):
            filling += char(len(raw) + x, '', 'e', 'blank')

    return div('stringbox', filling)


def show(content, style):
    """Takes a string representing HTML content and packages it for display in
    IPython/Jupyter Notebook"""

    window = div('window', content)
    return div('viewer', window)
