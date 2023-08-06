try:
    from wizzi_utils.torch.test.test_torch_tools import *

    # print('d init test_torch_tools worked')
except ModuleNotFoundError as e:
    # print('d Missing some modules')
    # print('\tError: {}'.format(e))
    pass
