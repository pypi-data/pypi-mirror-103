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
        the modules installed.

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

from wizzi_utils.misc_tools import *  # misc tools

# from .misc_tools import *  # misc tools
# __all__ = ['misc_tools']
# import .torch_tools as tt

from wizzi_utils import temp_sub_package as temp_pac

try:
    from wizzi_utils import torch_tools as tt  # torch tools
except ModuleNotFoundError:
    pass

try:
    from wizzi_utils import pyplot_tools as pyplt  # pyplot tools
except ModuleNotFoundError:
    pass

try:
    from wizzi_utils import algorithms as algs  # known algorithms
except ModuleNotFoundError:
    pass

try:
    from wizzi_utils import open_cv_tools as cvt  # cv2 tools
except ModuleNotFoundError:
    pass

try:
    from wizzi_utils import coreset_tools as cot  # coreset tools
except ModuleNotFoundError:
    pass

try:
    from wizzi_utils import json_tools as jt  # coreset tools
except ModuleNotFoundError:
    pass

try:
    from wizzi_utils import socket_tools as st  # coreset tools
except ModuleNotFoundError:
    pass
