from setuptools import setup, find_packages
# __packages__ = find_packages(
#     where = 'spotii',
# #    include = ['define*',],
# #    exclude = ['additional',]
#     )
# __packages__.append('spotii')
__packages__=['spotii','spotii.guifolder','spotii.communication','spotii.on_off','spotii.test_handler']
print(__packages__)
setup(
    name = "spotii",
    version = "0.0.4",
    description = "a demo",
    author = 'gxf',
    author_email = 'feng.gao@laipac.com',
    url = 'https://github.com/gxfca/gitTest',
    packages = __packages__,
#    package_dir ={"":"spotii"},
    entry_points={
    'console_scripts': [
        'spotii=spotii.__main__:spot_main',
    ],
    },
    )
