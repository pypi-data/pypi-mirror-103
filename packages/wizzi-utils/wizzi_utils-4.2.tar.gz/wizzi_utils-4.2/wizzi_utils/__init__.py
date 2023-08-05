"""
to import package:
    import wizzi_utils as wu
example:
    print(wu.misc_tools.to_str(var=1, title='my_int'))  # must work
    print(wu.to_str(var=2, title='my_int'))  # must work
    print(wu.tt.to_str(var=3, title='my_int')) # works if you have torch
    print(wu.pyplt.get_RGB_color(color_str='r'))  # works if you have matplotlib
"""

from wizzi_utils.misc_tools import *  # misc tools

# from .misc_tools import *  # misc tools
# __all__ = ['misc_tools']
# import .torch_tools as tt

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
