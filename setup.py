import os 
from distutils.core import setup

with open('README.md') as readme:
  long_description = readme.read()

local_path = os.path.join(os.path.dirname(__file__), 'gooey') 

images = [image for image in os.listdir(os.path.join(local_path, 'images'))]

languages = [lang 
            for lang in os.listdir(os.path.join(local_path, 'languages'))
            if '.py' not in lang]

setup(
    name='Gooey',
    version='0.1.0',
    author='Chris Kiehl',
    author_email='ckiehl@gmail.com',
    packages=[
      'gooey',
      'gooey.gui',
      'gooey.images',
      'gooey.languages',
      'gooey.mockapplications',
    ],

    data_files=[
      ('gooey/images', images), 
      ('gooey/languages', languages)
    ],
    url='http://pypi.python.org/pypi/Gooey/',
    license='LICENSE.txt',
    description='Turn (almost) any command line program into a full GUI application with one line',
    long_description=long_description
)
