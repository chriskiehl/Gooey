import os 
from distutils.core import setup

with open('README.md') as readme:
  long_description = readme.read()

local_path = os.path.join(os.path.dirname(__file__), 'gooey') 

imagepath = os.path.join(local_path, 'images')
langpath  = os.path.join(local_path, 'languages')

images = [os.path.join(imagepath, image) for image in os.listdir(imagepath)]

languages = [os.path.join(langpath, lang)
            for lang in os.listdir(langpath)
            if '.py' not in lang]

print(images)
print(languages)

setup(
    name='Gooey',
    version='0.1.0',
    author='Chris Kiehl',
    author_email='ckiehl@gmail.com',
    data_files=[
      ('', images), 
      ('', languages)
    ],
    packages=[
      'gooey',
      'gooey.gui',
      'gooey.images',
      'gooey.languages',
      'gooey.mockapplications',
    ],

    url='http://pypi.python.org/pypi/Gooey/',
    license='LICENSE.txt',
    description='Turn (almost) any command line program into a full GUI application with one line',
    long_description=long_description
)
