from distutils.core import setup

"""
see https://docs.python.org/3/distutils/setupscript.html
"""

setup(
    name='wizzi_utils',
    packages=[  # main package and sub packages
        'wizzi_utils',  # package name
        'wizzi_utils/misc',  # main sub package
        'wizzi_utils/misc/test',
        'wizzi_utils/algorithms',
        'wizzi_utils/algorithms/test',
        'wizzi_utils/coreset',
        'wizzi_utils/coreset/test',
        'wizzi_utils/json',
        'wizzi_utils/json/test',
        'wizzi_utils/open_cv',
        'wizzi_utils/open_cv/test',
        'wizzi_utils/pyplot',
        'wizzi_utils/pyplot/test',
        'wizzi_utils/socket',
        'wizzi_utils/socket/test',
        'wizzi_utils/torch',
        'wizzi_utils/torch/test',
    ],
    version='5.0',
    license='MIT',  # https://help.github.com/articles/licensing-a-repository
    description='some handy tools',
    long_description='some handy tools bla',
    author='Gilad Eini',
    author_email='giladEini@gmail.com',
    url='https://github.com/2easy4wizzi/2021wizzi_utils',  # link to github
    # TODO update on new release
    download_url='https://github.com/2easy4wizzi/2021wizzi_utils/archive/refs/tags/v_5.0.tar.gz',
    keywords=[  # Keywords that define your package best
        'debug tools',
        'cuda',
        'torch',
        'cv2',
        'tensorflow'
    ],
    install_requires=[  # TODO add pip installed libraries
        'datetime',
        'typing',
        'numpy',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6'
    ],
)
