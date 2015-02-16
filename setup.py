"""Script for setuptools."""

from setuptools import setup, find_packages


with open('README.md') as readme:
    long_description = readme.read()

version = __import__('gooey').__version__

setup(
    name='Gooey',
    version=version,
    url='http://pypi.python.org/pypi/Gooey/',
    author='Chris Kiehl',
    author_email='audionautic@gmail.com',
    description=('Turn (almost) any command line program into a full GUI '
                 'application with one line'),
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    dependency_links = ["http://www.wxpython.org/download.php"],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Desktop Environment',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Widget Sets',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    long_description=long_description
)
