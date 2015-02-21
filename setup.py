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
    long_description='''
<h1>Gooey (Beta)</h1>

<h3>Turn (almost) any Python Console Program into a GUI application with one line</h3>

<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/primary.png"/>
</p>


<h2>Quick Start</h2>

<p>Gooey is attached to your code via a simple decorator on your `main` method.</p>

<pre>
    from gooey import Gooey

    @Gooey      <--- all it takes! :)
    def main():
      # rest of code

</pre>

With the decorator attached, run your program and the GUI will now appear!

<b>Note: PyPi's formatting is ancient, so checkout the full documentation, instructions, and source on <a href="https://github.com/chriskiehl/Gooey">github!</a></b>

<br /><br /><br /><br />'''
)
