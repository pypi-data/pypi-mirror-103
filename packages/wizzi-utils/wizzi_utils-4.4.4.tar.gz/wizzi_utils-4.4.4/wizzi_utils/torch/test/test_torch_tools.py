from wizzi_utils.torch import torch_tools as tt
from wizzi_utils import misc_tools as mt


def cuda_on_test():
    print('{}: {}'.format(mt.get_function_name_and_line(depth=1), tt.cuda_on()))
    return


def test_all():
    cuda_on_test()
    return
