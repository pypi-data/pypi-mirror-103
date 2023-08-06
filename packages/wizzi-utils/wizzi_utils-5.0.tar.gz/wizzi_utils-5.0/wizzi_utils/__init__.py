"""
package wizzi utils:
    pip install wizzi_utils
    of
    pip install wizzi_utils --upgrade

to import all functions:
    import wizzi_utils as wu
    # the above will give you all functions and tests
    # everything in misc_tools must work
    # everything else, e.g. torch_tools, will work only if you have all
        the modules need for torch_tools installed.

examples:
    # direct access to a module - must work
    print(wu.misc_tools.to_str(var=1, title='my_int'))

    # access to a function in the main module misc_tools - must work
    print(wu.to_str(var=2, title='my_int'))

    # access to a function in the torch module - will work if you have torch
        and the rest of the modules needed installed
    print(wu.tt.to_str(var=3, title='my_int'))

    # access to a function in the matplotlib module - same as torch above
    print(wu.pyplt.get_RGB_color(color_str='r'))
"""

__version__ = '5.0'
# __all__ = ['misc_tools']  # TODO future

# default package - available without extra namespace
from wizzi_utils.misc import *

# extra packages - available with extra namespace - requires extra modules
from wizzi_utils import algorithms as algs
from wizzi_utils import coreset as cot
from wizzi_utils import json as jt
from wizzi_utils import open_cv as cvt
from wizzi_utils import pyplot as pyplt
from wizzi_utils import socket as st
from wizzi_utils import torch as tt

