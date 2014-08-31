import os 
from setuptools import setup, find_packages


with open('README.md') as readme:
  long_description = readme.read()

local_path = os.path.join(os.path.dirname(__file__), 'gooey') 

imagepath = os.path.join(local_path, 'images')
langpath  = os.path.join(local_path, 'languages')

images = [os.path.join(imagepath, image) for image in os.listdir(imagepath)]

languages = [os.path.join(langpath, lang)
            for lang in os.listdir(langpath)
            if '.py' not in lang]

setup(
    name='Gooey',
    version='0.1.0',
    author='Chris Kiehl',
    author_email='audionautic@gmail.com',
    package_data={
      '': ['*.txt', '*.png', '*.jpg', '*.json', '*.ico', '*.gif']
    },
    packages=find_packages(),
    url='http://pypi.python.org/pypi/Gooey/',
    dependency_links = [
        "http://www.wxpython.org/download.php"
    ],
    license='LICENSE.txt',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools :: GUI :: CLI',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
    description='Turn (almost) any command line program into a full GUI application with one line',
    long_description=long_description
)
