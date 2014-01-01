'''
generates the internals of the image_store module

Nice perk of this approach is that it turns path errors into 
things that lint can catch, rather than something that gets stumbled 
upon randomly at runtime. 
'''


import os 

PATH = __path__[0]
print PATH 
	
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
			if file_extension(f) in ('.jpeg','.png', '.ico')]


	
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
	
	
	
	
	
	
	
