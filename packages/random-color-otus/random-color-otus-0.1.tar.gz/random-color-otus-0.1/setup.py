import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='random-color-otus',
    version='0.1',
    packages=['colors'],
    include_package_data=True,
    license='GNU General Public License v3.0',
    description='Get random color',
    url='https://github.com/DanteOnline/django-dantejcoder',
    author='Leo',
    author_email='iamdanteonline@gmail.com',
    keywords=['random', 'color'],
)
