import os
from setuptools import setup, find_packages
# __packages__ = find_packages(
#     where = 'spotii_project',
# #    include = ['define*',],
# #    exclude = ['additional',]
#     )
#__packages__ = ['spotii'] + __packages__
__packages__=['spotii','spotii.guifolder','spotii.communication','spotii.on_off','spotii.test_handler']
#__packages__=['spotii']
print(__packages__)


# _ROOT = os.path.abspath(os.path.dirname(__file__))
# def get_data(path):
#     return os.path.join(_ROOT, 'data', path)

#print get_data('resource1/foo.txt')
setup(
    name = "spotii",
    version = "0.0.6",
    description = "a demo",
    author = 'gxf',
    author_email = 'feng.gao@laipac.com',
    url = 'https://github.com/gxfca/gitTest',
    packages = __packages__,
#    package_dir ={'spoitii':'spotii'},
    package_data={
        'spotii':['guifolder/png/slot/*',
                  'guifolder/png/slot/detecting/*',
                  'guifolder/png/slot/invalid/*',
                  'guifolder/png/slot/negative/*',
                  'guifolder/png/slot/positive/*',
                  'guifolder/png/slot/warning/*',
                  'guifolder/png/titile/*',
                  'img/*',
                  ],
                  },
    entry_points={
    'console_scripts': [
        'spotii=spotii.__main__:spot_main',
    ],
    },
    )
