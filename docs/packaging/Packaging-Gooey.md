# Packaging Gooey as a Stand Alone Application

<p align="center">
    <img src="https://github.com/chriskiehl/GooeyImages/raw/images/docs/packaging/packaged-application.png" />
</p>


>:warning: Packaging Gooey is an ongoing science. Gooey currently runs on all the major platforms, can be installed in a bajillion different ways, and has several active versions in wide usage. In short, edge cases abound. If you run into any problems, hit up [this issue](https://github.com/chriskiehl/Gooey/issues/259).

You can package all of your programs files into a single easy to distribute executable using PyInstaller.  

Packing Gooey into a standalone executable is super straight forward thanks to [PyInstaller](http://www.pyinstaller.org/). It is the only dependency you'll need and can be installed via the following. 

```
pip install pyinstaller
```

**Setting up the build:**

PyInstaller uses [spec files](http://pythonhosted.org/PyInstaller/#using-spec-files) to determine how to bundle the project. These are a bit like `setup.py` files, but contain rules for how PyInstaller should bundle your whole application as a stand alone executable.    

This file is usually placed in the root of your project. e.g.  

```
MyProject/
   - src/
   - build.spec  # <-- goes here!
   - LICENCE.txt
   - README.md
```

**Download Spec Files**

* Windows users can grab a pre-built spec file [here](https://raw.githubusercontent.com/chriskiehl/Gooey/master/docs/packaging/build-win.spec).
* For OSX users, you'll want [this one](https://raw.githubusercontent.com/chriskiehl/Gooey/master/docs/packaging/build-osx.spec).

The exact contents of the spec files will vary based on your OS, but at a high level, they'll share the same core pieces: `Analysis`, `EXE`, and, if you're on OSX, `BUNDLE` 


```
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # replace me with the main entry point 
    pathex=['/path/to/main.py'],  # replace me with the appropriate path
    ...
    )

pyz = PYZ(a.pure)

options = [('u', None, 'OPTION'), ('v', None, 'OPTION'), ('w', None, 'OPTION')]

exe = EXE(pyz,
       ...
       name='MyCoolApplication'  # replace me with exe name
       console=False)
       
## OSX only below!       
app = BUNDLE(exe,
             name='APPNAME.app',  # osx users replace me!
             bundle_identifier=None,
             info_plist=info_plist
            )
```

The `Analysis` section is where you'll tell PyInstaller about your program. Using the build.spec from above, you'll need to make two edits to this section. 

1. replace `APPNAME` in the `Analysis()` section with the name of _your_ application
2. replace the `pathex` value in the `Analysis()` section with the path to your application's root


> note: If you use additional data resources (e.g. images, data, etc..) you'll also need to explicitly add them to the EXE section. See [packaging custom images] for more info. 

Next is `EXE`. In this section you'll replace the `name` argument with what you'd like the final `.exe` to be named.

>Note: if you're providing your own icon file, EXE is where you'll provide it. If you're on Windows, you must provide an .ico file (not PNG).

If you're on OSX, you'll have an additional `BUNDLE` section. You'll need to make one final edit here as well to control the name of the `.app` bundle that PyInstaller produces. Additionally, if you're customizing the bundle's icon, this is where you would supply the override (versus Windows, which places it in the EXE section). 

Once you've updated the `.spec` to reflect your program's details. All that's left to do is build the executable! 

### Running the .spec file 

From the command line, run 

```
pyinstaller -F --windowed build.spec
```

* `-F` tells PyInstaller to create a single bundled output file
* `--windowed` disables the terminal which would otherwise launch when you opened your app. 

And that's it. Inside of the `dist/` directory, you'll find a beautiful stand-alone executable that you can distribute to your users. 


## Troubleshooting

**PROBLEM: My bundled Application won't work!** 

First things first: _See if you can package your application **without** Gooey!_

Read and understand all of the PyInstaller docs. If you're referencing binaries or external data files, you may have to do a little extra work in your `.spec` to get PyInstaller to understand all of your dependencies. 

Rebuild your bundle with `debug=True` set in the `.spec` file. This will give lots of useful output when your application bootstraps which can make pinning down the problem much easier. 

Rebuild your bundle without the `-F` flag (e.g. just `pyinstaller build.spec`). This will build a directory with all of your dependencies. This can make it easier to poke around and see what PyInstaller's view of your project actually is.  

**PROBLEM: I'm seeing the wrong icon on my executable** 

First things first: Is Windows gas lighting you? 

Windows caches icons semi-aggressively. This can lead to it showing an icon in the file explorer that doesn't actually reflect reality. 

![image](https://github.com/chriskiehl/GooeyImages/raw/images/docs/packaging/cached-icon.png)

Right-click on the executable and select "properties." This will show you the icon that's actually associated with file. As long as everything looks good there, you're golden. Windows will catch up... _eventually_.  


**PROBLEM: Exception: This program needs access to the screen. Please run with a Framework build of python, and only when you are logged in on the main display of your Mac.**

This happens on OSX when you neglect the `--windowed` flag during your build step. 

wrong:
```
pyinstaller build.spec  ## oops! forgot the required flags    
```

Correct:
```
pyinstaller --windowed build.spec 
```
 
Checkout the [Pyinstaller Manual](https://github.com/pyinstaller/pyinstaller/wiki/FAQ) for more details. 

