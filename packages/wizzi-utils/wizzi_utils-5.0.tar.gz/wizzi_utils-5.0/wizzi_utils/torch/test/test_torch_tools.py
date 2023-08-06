from wizzi_utils.torch import torch_tools as tt
from wizzi_utils.misc import misc_tools as mt


def cuda_on_test():
    print('{}: {}'.format(mt.get_function_name(depth=1), tt.cuda_on()))
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    cuda_on_test()
    print('{}'.format('-' * 5))
    return
