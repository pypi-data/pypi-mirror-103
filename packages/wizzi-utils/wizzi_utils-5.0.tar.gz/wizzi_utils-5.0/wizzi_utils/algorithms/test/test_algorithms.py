from wizzi_utils.algorithms import algorithms as alg
from wizzi_utils.misc import misc_tools as mt


def find_centers_test():
    # import matplotlib.pyplot as plt
    # A = np.zeros((4, 2))  # A square with origin 0
    # A[0] = [-1, -1]
    # A[1] = [-1, 1]
    # A[2] = [1, -1]
    # A[3] = [1, 1]
    # print(mt.to_str(A, title='A'))
    # centers = find_centers(A, k=1)
    # print(mt.to_str(centers, title='centers'))
    # X, y = mt.de_augment_numpy(A)
    # X_c, y_c = mt.de_augment_numpy(centers)
    # plt.scatter(X, y, color='g', marker='.', label='A')
    # plt.scatter(X_c, y_c, color='r', marker='.', label='k==1')
    # plt.legend(loc='upper right', ncol=1, fancybox=True, framealpha=0.5, edgecolor='black')
    # plt.show()
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    find_centers_test()
    print('{}'.format('-' * 5))
    return
