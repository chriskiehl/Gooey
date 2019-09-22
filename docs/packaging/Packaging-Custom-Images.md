# Using Custom Images while Packaging  

> Note: if you're new to packaging Gooey, checkout the main [Packaging Guide](https://github.com/chriskiehl/Gooey/blob/doc-improvements/docs/packaging/Packaging-Gooey.md) first!  

Gooey comes with a set of six default icons. These can be overridden with your own custom images/icons by telling Gooey to search additional directories when initializing. This is done via the `image_dir` argument to the `Gooey` decorator. 

```python
@Gooey(program_name='Custom icon demo', image_dir='/path/to/images')
def main():
    # rest of program
```

While this works for regular executions, a little additional work is required to make sure that your images will actually be available when running as a stand alone executable. 
    
To make your custom images available after packaging, you have to do two things. 

**Step 1:** wrap the path to your image directory in the `local_resource_path()` function provided by Gooey. When PyInstaller runs your application, it decompresses all the contents to a random temp directory. This function will handle the logic of resolving that directory and fetching your resources from it. 

```python
from gooey import Gooey, local_resource_path

@Gooey(image_dir=local_resource_path('relative/path/to/images'))
def main():
   ...
```

**Step 2:** Update `build.spec` to include the image directory during bundling. This is done by giving the path to your Images as a Tree object to Pyinstaller's `EXE` section. 

```
# -*- mode: python ; coding: utf-8 -*-

import os
...
# LOOK AT ME! I AM A TREE OBJECT 
image_overrides = Tree('path/to/images', prefix='path/to/images')

...

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          options,
          image_overrides,  # <-- NEW 
          name='APPNAME',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon=os.path.join(gooey_root, 'images', 'program_icon.ico'))
``` 

And then build via PyInstaller as usual. 

```
pyinstaller -F --windowed build.spec
``` 

PyInstaller will now include your images in its bundle.   




