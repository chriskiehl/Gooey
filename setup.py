from distutils.core import setup

setup(
		name='Gooey',
		version='0.1.0',
		author='Chris Kiehl',
		author_email='ckiehl@gmail.com',
		packages=[
					'gooey', 
					'gooey.languages', 
					'gooey.app', 
					'gooey.app.dialogs', 
					'gooey.app.images', 
					'gooey.mockapplications',
					'gooey.themes'],
		url='http://pypi.python.org/pypi/TowelStuff/',
		license='LICENSE.txt',
		description='Useful towel-related stuff.',
		long_description=open('README.txt').read()
)