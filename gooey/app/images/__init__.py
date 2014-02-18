'''
Code generation for the image_store module

Loops throught the image package and 

At some point early on, I thought this would be waaaaaaaay easier than just 
updating the paths by hand. Being that I ended up with just a handful of images, 
I was wrong.. 
'''


import os 

PATH = os.path.dirname(__file__)
	
def render_class(assignments):
	template = '''
"""
GENERATED CODE: DO NOT EDIT

Simple mapping of image names to their location on disc. 
Convenience module for keeping the filepaths in one place.

"""

{variables}
'''
	return template.format(variables=assignments)


def load_imagepaths():
	file_extension = lambda x: os.path.splitext(x)[-1]
	
	return [os.path.join(PATH, f) for f in os.listdir(PATH)
			if file_extension(f) in ('.jpeg','.png', '.ico', '.gif')]


	
def write_module(contents):
	module_path = os.path.join(PATH, 'image_store.py')
	with open(module_path, 'wb') as f: 
		f.write(contents)	

	
def build_assignments(paths):
	get_name = lambda x: os.path.splitext(os.path.split(x)[-1])[0]
	
	assignments = ('%s = r"%s"' % (get_name(p), p)
									for p in paths)
	return '\n'.join(assignments)
		
paths = load_imagepaths()
assignments = build_assignments(paths)
write_module(render_class(assignments))
	
	
	
	
	
	
	
