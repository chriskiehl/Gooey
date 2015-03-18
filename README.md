Gooey (Beta)
=====  
Turn (almost) any Python Console Program into a GUI application with one line  

<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/primary.png"/>
</p> 


Table of Contents
-----------------  

- [Gooey](#gooey)
- [Table of contents](#table-of-contents)
- [Latest Update](#latest-update)
- [Quick Start](#quick-start)
    - [Installation Instructions](#installation-instructions)
    - [Usage](#usage)
- [What It Is](#what-is-it)
- [Why Is It](#why)
- [Who is this for](#who-is-this-for)
- [How does it work](#how-does-it-work)
- [Configuration](#configuration)
    - [Full/Advanced](#advanced)
    - [Basic](#basic)
    - [No Config](#no-config)
    - [AutoGooey](#autogooey)
- [Final Screen](#final-screen)
- [Change Log](#change-log)
- [TODO](#todo)
- [Contributing](#wanna-help)
- [Image Credits](#image-credits)




 


----------   


###Latest Update: 

Drag and Drop support (`Issue #28`)

<p align="center">
 <img src="https://github.com/chriskiehl/Gooey/blob/master/resources/dragdrop.gif" width="500">
</p>

Tada!   

  

----------------  




##Quick Start


###Installation instructions


The easiest way to install Gooey is via `pip` 

    pip install Gooey 


Alternatively, you can install Gooey by cloning the project to your local directory

    git clone https://github.com/chriskiehl/Gooey.git

run `setup.py` 

    python setup.py install

###Usage  

Gooey is attached to your code via a simple decorator on your `main` method. 

    from gooey import Gooey

    @Gooey      <--- all it takes! :)
    def main():
      # rest of code

Different styling and functionality can be configured by passing arguments into the decorator.

    # options
    @Gooey(advanced=Boolean,          # toggle whether to show advanced config or not 
           language=language_string,  # Translations configurable via json
           show_config=Boolean,            # skip config screens all together
           program_name='name',       # Defaults to script name 
           program_description        # Defaults to ArgParse Description
      )
    def main():
      # rest of app
            
See: [How does it Work](#how-does-it-work) section for details on each option.

Gooey will do its best to choose sensible widget defaults to display in the GUI. However, if more fine tuning is desired, you can use the drop-in replacement `GooeyParser` in place of `ArgumentParser`. This lets you control which widget displays in the GUI. See: [GooeyParser](#gooeyparser)

    from gooey import Gooey

    @Gooey      <--- all it takes! :)
    def main():
      parser = GooeyParser(description="My Cool GUI Program!") 
      parser.add_argument('Filename', widget="FileChooser")

    
What is it? 
-----------  

Gooey converts your Console Applications into end-user-friendly GUI applications. It lets you focus on building robust, configurable programs in a familiar way, all without having to worry about how it will be presented to and interacted with by your average user. 

Why?
---  

Because as much as we love the command prompt, the rest of the world looks at it like an ugly relic from the early '80s. On top of that, more often than not programs need to do more than just one thing, and that means giving options, which previously meant either building a GUI, or trying to explain how to supply arguments to a Console Application. Gooey was made to (hopefully) solve those problems. It makes programs easy to use, and pretty to look at! 

Who is this for?
----------------  

If you're building utilities for yourself, other programmers, or something which produces a result that you want to capture and pipe over to another console application (e.g. *nix philosophy utils), Gooey probably isn't the tool for you. However, if you're building 'run and done,' around-the-office-style scripts, things that shovel bits from point A to point B, or simply something that's targeted at a non-programmer, Gooey is the perfect tool for the job. It lets you build as complex of an application as your heart desires all while getting the GUI side for free. 

How does it work? 
------------------  

Gooey is attached to your code via a simple decorator on your `main` method. 

    @Gooey      <--- all it takes! :)
    def main():
      # rest of code

At run-time, it parses your Python script for all references to `ArgumentParser`. (The older `optparse` is currently not supported.) These references are then extracted, assigned a `component type` based on the `'action'` they provide, and finally used to assemble the GUI.  

####Mappings: 

Gooey does its best to choose sensible defaults based on the options it finds. Currently, `ArgumentParser._actions` are mapped to the following `WX` components. 

| Parser Action    | Widget    | Example |
|:----------------------|-----------|------|
| store  |  TextCtrl |  <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/general_tb.png"/>|
| store_const   |     CheckBox |  <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/check_box.png"/>|
|   store_true|        CheckBox | <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/check_box.png"/>|
|  store_False  |      CheckBox|  <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/check_box.png"/>   |
|       append |       TextCtrl |  <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/general_tb.png"/>  | 
|        count|              DropDown &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/count_dropdown.png"/> | 
| Mutually Exclusive Group | RadioGroup | <img src="https://github.com/chriskiehl/Gooey/blob/master/resources/radio_group.png"/>
|choice &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|        DropDown | <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/options_dropdown.png"/> |

###GooeyParser

If the above defaults aren't cutting it, you can control the exact widget type by using the drop-in `ArgumentParser` replacement `GooeyParser`. This gives you the additional keyword argument `widget`, to which you can supply the name of the component you want to display. Best part? You don't have to change any of your `argparse` code to use it. Drop it in, and you're good to go. 

**Example:**

    from argparse import ArgumentParser
    ....

    def main(): 
        parser = ArgumentParser(description="My Cool Gooey App!")
        parser.add_argument('filename', help="name of the file to process") 

Given then above, Gooey would select a normal `TextField` as the widget type like this: 
<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/textfield_demo.PNG">
</p>

However, by dropping in `GooeyParser` and supplying a `widget` name, you display a much more user friendly `FileChooser`.

Note: notice that you still need to decorate your function with @Gooey.

    from gooey import Gooey, GooeyParser
    ....

    @Gooey
    def main(): 
        parser = GooeyParser(description="My Cool Gooey App!")
        parser.add_argument('filename', help="name of the file to process", widget='FileChooser') 
        
<p align="center"><img src="https://github.com/chriskiehl/Gooey/blob/master/resources/chooser_demo.PNG"></p>

**Custom Widgets:**

| Widget         |           Example            | 
|----------------|------------------------------| 
|  FileChooser<br />FileSaver<br />DirChooser<br />MultiFileChooser   | <p align="center"><img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/filechooser.gif" width="400"></p> | 
|  DateChooser   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| <p align="center"><img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/datechooser.gif" width="400"></p> |  
|  TextField   |  | 
|  Dropdown   |  | 
|  Counter   |  | 
|  RadioGroup   |  | 
|  CheckBox   |  | 
 
  


   

-------------------------------------------    





Configuration 
------------   

Gooey can show three kinds of GUI.

- Full/Advanced
- Basic
- No config

Each has the following options: 


| Parameter | Summary | 
|-----------|---------|
| language | Gooey is (kind of) international ready (sans Unicode issues (TODO)). All program text is stored in an external `json` file. Translating to your host language only requires filling in the key/value pairs.|
|program_name | The name displayed in the title bar of the GUI window. If the value is `None`, the title is pulled from `sys.argv[0]`. |
| program_description | Sets the text displayed in the top panel of the `Settings` screen. If `None` the description is pulled from the  `ArgumentParser`. |  





###Advanced 


The default view is the "full" or "advanced" configuration screen. It can be toggled via the `advanced` parameter in the `Gooey` decorator. 



    @gooey(advanced=True)
    def main():
        # rest of code   
        

        
This view presents each action in the `Argument Parser` as a unique GUI component. This view is ideal for presenting the program to users which are unfamiliar with command line options and/or Console Programs in general. Help messages are displayed along side each component to make it as clear as possible which each widget does.
<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/advanced_config.png">
</p>

--------------------------------------------  



###Basic  

The basic view is best for times when the user is familiar with Console Applications, but you still want to present something a little more polished than a simple terminal. The basic display is accessed by setting the `advanced` parameter in the `gooey` decorator to `False`. 

    @gooey(advanced=False)
    def main():
        # rest of code  

<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/basic_config.png">
</p>


----------------------------------------------  

###No Config

No Config pretty much does what you'd expect: it doesn't show a configuration screen. It hops right to the `display` section and begins execution of the host program. This is the one for improving the appearance of little one-off scripts. 

<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/no_config.png">
</p>

---------------------------------------  


###AutoGooey

When using the @Gooey decorator, your script will always display a GUI. If you want to offer both interfaces (command-line and GUI), you can use this code snippet:

    # Try to import Gooey for GUI display, but manage exception so that we replace the Gooey decorator by a dummy function that will just return the main function as-is, thus keeping the compatibility with command-line usage
    try:
        import lib.gooey as gooey
    except:
        # Define a dummy replacement function for Gooey to stay compatible with command-line usage
        class gooey(object):
            def Gooey(func):
                return func
        # If --gui was specified, then there's a problem
        if len(sys.argv) > 1 and sys.argv[1] == '--gui': raise ImportError('--gui specified but lib/gooey could not be found, cannot load the GUI (however you can still use in commandline).')

    def check_gui_arg():
        '''Check that the --gui argument was passed, and if true, we remove the --gui option and replace by --gui_launched so that Gooey does not loop infinitely'''
        if len(sys.argv) > 1 and sys.argv[1] == '--gui':
            #del sys.argv[1]
            sys.argv[1] = '--gui_launched' # CRITICAL: need to remove/replace the --gui argument, else it will stay in memory and when Gooey will call the script again, it will be stuck in an infinite loop calling back and forth between this script and Gooey. Thus, we need to remove this argument, but we also need to be aware that Gooey was called so that we can call gooey.GooeyParser() instead of argparse.ArgumentParser() (for better fields management like checkboxes for boolean arguments). To solve both issues, we replace the argument --gui by another internal argument --gui_launched.
            return True
        else:
            return False

    def AutoGooey(fn):
        '''Automatically show a Gooey GUI if --gui is passed as the first argument, else it will just run the function as normal'''
        if check_gui_arg():
            return gooey.Gooey(fn)
        else:
            return fn

    @AutoGooey
    def main(argv=None):
        # ... your program here ...

And then when parsing command-line arguments, you can detect if your script is running inside Gooey or from command-line:

    @AutoGooey
    def main(argv=None):
        #-- Constructing the parser
        if len(sys.argv) > 1 and sys.argv[1] == '--gui_launched':
            main_parser = gooey.GooeyParser()
        else:
            main_parser = argparse.ArgumentParser()
        #-- Constructing arguments
        main_parser.add_argument('-i', '--input', metavar='/path/to/root/folder', type=str, required=True,
                            help='Path to the root folder from where the scanning will occur.')

You can then just call your script using --gui as the first argument (eg, `python yourscript.py --gui`) to show the Gooey GUI, or just omit this argument and use your script from command-line as usual.


---------------------------------------  


Final Screen
------------  
<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/final_screen.png">
</p>

----------------------------------------------  


###Change Log
----------
- Added drag and drop support
- Added new widget packs: DateChooser, FileChooser, DirChooser
- fixed several parsing related issues. 
- Gooey now has a sane setup.py (thanks to hero user LudoVio) 
- Gooey now builds from json for easy configurability 
    - Side Note: This was done with big strides towards making Gooey language agnostic. Coming Soon! 
- Fixed GUI layout so that resizing works better


###Planned Features: 
- Language agnostic! 
- Stop/cancel button on run screen 
    
    

TODO
----  

* Add to pypi
* Update graphics
* Get OS X version working. 



Wanna help?
-----------  

* **Artist Wanted!** The graphics and icons in Gooey are a mismash of stuff I was able to scrape up for free off the internet. I'd love to replace them with something more stylistically unified. 
* Programmer? Pull requests are super welcome. The projects' style is *fantastically* inconsistent, though. So be warned :) I tried to follow the WxWidgets style of Leading Capital methods and CamelCased variables, but.. Python habits die hard. So, there are underscores littered all over the place. 





  [1]: http://i.imgur.com/7fKUvw9.png
