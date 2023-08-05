import os
from setuptools import setup, find_packages


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='random-color-otus',
    version='0.2',
    packages=find_packages(),
    include_package_data=False,
    license='GNU General Public License v3.0',
    description='random colors',
    url='https://github.com/DanteOnline/charon',
    author='DanteOnline',
    author_email='iamdanteonline@gmail.com',
    keywords = ['iw', 'dev', 'trxpower', 'monitor', 'managed', 'interface', 'wi-fi'],
    entry_points={
        'console_scripts': [
            'use_random_color = colors.main:main',
        ]
    },
)