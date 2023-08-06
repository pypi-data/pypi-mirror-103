try:
    from wizzi_utils.temp_sub_package.temp_module import *
    print('init temp_sub_package worked')
except ModuleNotFoundError as e:
    print('Missing some modules')
    print('Error: {}'.format(e))

