from wizzi_utils.misc import misc_tools as mt


def to_str_test():
    print(mt.to_str(var=32223123123123123, title='my_int'))
    # print(to_str(var=3.2, title='my_float'))
    # print(to_str(var=3.2123123, title='my_float', float_precision=4))
    # print(to_str(var=1234567890.223123123123123123, title='my_long_float', float_precision=3))
    # print(to_str(var='a', title='my_str'))
    # print(to_str(var=[], title='my_empty_list'))
    # print(to_str(var=[112312312, 3, 4], title='1d list of ints', recursive=True))
    # print(to_str(var=[1, 3123123], title='1d list of ints no data', data_chars=-1, recursive=True))  # no data
    # print(to_str(var=[1.0000012323, 3123123.22454875123123], title='1d list of ints no data', float_precision=7,
    #              recursive=True))
    # print(to_str(var=np.array([1.0000012323, 3123123.22454875123123], dtype=float), title='1d list of ints no data',
    #              float_precision=7, recursive=True))
    # print(to_str(var=[11235] * 1000, title='1d long list', recursive=True))
    # print(to_str(var=(1239, 3, 9), title='1d tuple', recursive=True))
    # print(to_str(var=[[1231.2123123, 15.9], [3.0, 7.55]], title='2d list', recursive=True))
    # print(to_str(var=[(1231.2123123, 15.9), (3.0, 7.55)], title='2d list of tuples', recursive=True))
    # b = np.array([[1231.123122, 15.9], [3.0, 7.55]])
    # print(to_str(var=b, title='2d np array', recursive=True))
    # cv_img = np.zeros(shape=[480, 640, 3], dtype=np.uint8)
    # print(to_str(var=cv_img, title='cv_img', recursive=True))
    # print(to_str(var={'a': [1213, 2]}, title='dict of lists', recursive=True))
    # print(to_str(var={'a': [{'k': [1, 2]}, {'c': [7, 2]}]}, title='nested dict', recursive=True))
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name(depth=1)))
    to_str_test()
    print('{}'.format('-' * 20))
    return
