from jinja2 import Environment, PackageLoader, select_autoescape

# MODULE INTRODUCTION
"""This module contains dislay functions to render the different data layers
using Jinja2 templates and IPython rendering methods for Jupyter Notebook."""

# GLOBAL VARIABLE DECLARATIONS
ENV = Environment(
    loader=PackageLoader('ga-capstone', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
