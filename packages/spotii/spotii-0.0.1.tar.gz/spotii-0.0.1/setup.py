from setuptools import setup, find_packages
__packages__ = ["spotii"]

setup(
    name = "spotii",
    version = "0.0.1",
    description = "a demo",
    author = 'gxf',
    author_email = 'feng.gao@laipac.com',
    url = 'https://github.com/gxfca/gitTest',
#    packages = find_packages('spotii'),
    packages = find_packages(
    where = 'spotii',
#    include = ['define*',],
#    exclude = ['additional',]
    ),
#    packages = __packages__,
    package_dir ={"":"spotii"},
#     entry_points={
#     'console_scripts': [
#         'spotii=spotii.__main__:spot_main',
#     ],
#     },
    )
