try:
    from wizzi_utils.torch.torch_tools import *

    # print('a init torch worked')
except ModuleNotFoundError as e:
    # print('a Missing some modules')
    # print('\tError: {}'.format(e))
    pass

from wizzi_utils.torch import test
