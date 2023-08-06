try:
    from wizzi_utils.temp_sub_package import temp_module
    print('init temp_sub_package worked')
except ModuleNotFoundError as e:
    print('Missing some modules')
    print('Error: {}'.format(e))


def temp_func_test():
    print(temp_module.temp_func())
    return


def test_all():
    temp_func_test()
    return
