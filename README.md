Gooey (Beta)
=====  
Turn (almost) any Python Console Program into a GUI application with one line  

<p align="center">
    <img src="https://cloud.githubusercontent.com/assets/1408720/7904381/f54f97f6-07c5-11e5-9bcb-c3c102920769.png" />
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
- [Internationalization](#internationalization)
- [Configuration](#configuration)
- [Run Modes](#run-modes)
    - [Full/Advanced](#advanced)
    - [Basic](#basic)
    - [No Config](#no-config)
- [Examples](#examples)
- [Screenshots](#screenshots)
- [Change Log](#change-log)
- [TODO](#todo)
- [Contributing](#wanna-help)
- [Image Credits](#image-credits)




 


----------   


###Artist Wanted!

Want to contribute to Gooey? We need icons/logos!

Drop me an <a href="mailto:audionautic@gmail.com">email</a> if you want to help out!

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

Gooey is attached to your code via a simple decorator on whichever method has your `argparse` declarations (usually `main`).

    from gooey import Gooey

    @Gooey      <--- all it takes! :)
    def main():
      parser = ArgumentParser(...)
      # rest of code

Different styling and functionality can be configured by passing arguments into the decorator.

    # options
    @Gooey(advanced=Boolean,          # toggle whether to show advanced config or not 
           language=language_string,  # Translations configurable via json
           show_config=True,          # skip config screens all together
           program_name='name',       # Defaults to script name
           program_description,       # Defaults to ArgParse Description
           default_size=(610, 530),   # starting size of the GUI
           required_cols=1,           # number of columns in the "Required" section
           optional_cols=2,           # number of columbs in the "Optional" section
           dump_build_config=False)   # Dump the JSON Gooey uses to configure itself
    )
    def main():
      parser = ArgumentParser(...)
      # rest of code
            
See: [How does it Work](#how-does-it-work) section for details on each option.

Gooey will do its best to choose sensible widget defaults to display in the GUI. However, if more fine tuning is desired, you can use the drop-in replacement `GooeyParser` in place of `ArgumentParser`. This lets you control which widget displays in the GUI. See: [GooeyParser](#gooeyparser)

    from gooey import Gooey, GooeyParser

    @Gooey
    def main():
      parser = GooeyParser(description="My Cool GUI Program!") 
      parser.add_argument('Filename', widget="FileChooser")
      parser.add_argument('Date', widget="DateChooser")
      ...

    
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
-----------------

Gooey is attached to your code via a simple decorator on whichever method has your `argparse` declarations.

    @Gooey
    def my_run_func():
      parser = ArgumentParser(...)
      # rest of code

At run-time, it parses your Python script for all references to `ArgumentParser`. (The older `optparse` is currently not supported.) These references are then extracted, assigned a `component type` based on the `'action'` they provide, and finally used to assemble the GUI.  

####Mappings: 

Gooey does its best to choose sensible defaults based on the options it finds. Currently, `ArgumentParser._actions` are mapped to the following `WX` components. 

| Parser Action    | Widget    | Example |
|:----------------------|-----------|------|
| store  |  TextCtrl |  <img src="https://cloud.githubusercontent.com/assets/1408720/7904380/f54e9f5e-07c5-11e5-86e5-82f011c538cf.png"/>|
| store_const   |     CheckBox |  <img src="https://cloud.githubusercontent.com/assets/1408720/7904367/f538c850-07c5-11e5-8cbe-864badfa54a9.png"/>|
|   store_true|        CheckBox | <img src="https://cloud.githubusercontent.com/assets/1408720/7904367/f538c850-07c5-11e5-8cbe-864badfa54a9.png"/>|
|  store_False  |      CheckBox|  <img src="https://cloud.githubusercontent.com/assets/1408720/7904367/f538c850-07c5-11e5-8cbe-864badfa54a9.png"/>   |
|       append |       TextCtrl |  <img src="https://cloud.githubusercontent.com/assets/1408720/7904380/f54e9f5e-07c5-11e5-86e5-82f011c538cf.png"/>  | 
|        count|              DropDown &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | <img src="https://cloud.githubusercontent.com/assets/1408720/7904371/f53ccbe4-07c5-11e5-80e5-510e2aa22922.png"/> | 
| Mutually Exclusive Group | RadioGroup | <img src="https://cloud.githubusercontent.com/assets/1408720/7904383/f553feb8-07c5-11e5-9d5b-eaa4772075a9.png"/>
|choice &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|        DropDown | <img src="https://cloud.githubusercontent.com/assets/1408720/7904379/f54e4da6-07c5-11e5-9e66-d8e6d7f18ac6.png"/> |

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
    <img src="https://cloud.githubusercontent.com/assets/1408720/7904368/f5393e20-07c5-11e5-88e9-c153fc3ecfaa.PNG">
</p>

However, by dropping in `GooeyParser` and supplying a `widget` name, you can display a much more user friendly `FileChooser`


    from gooey import GooeyParser
    ....
    
    def main(): 
        parser = GooeyParser(description="My Cool Gooey App!")
        parser.add_argument('filename', help="name of the file to process", widget='FileChooser') 
        
<p align="center"><img src="https://cloud.githubusercontent.com/assets/1408720/7904370/f53ae23e-07c5-11e5-8757-c8aa6f3013b5.PNG"></p>

**Custom Widgets:**

| Widget         |           Example            | 
|----------------|------------------------------| 
|  Directory/FileChooser   | <p align="center"><img src="https://cloud.githubusercontent.com/assets/1408720/7904377/f5483b28-07c5-11e5-9d01-1935635fc22d.gif" width="400"></p> | 
|  DateChooser   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| <p align="center"><img src="https://cloud.githubusercontent.com/assets/1408720/7904376/f544756a-07c5-11e5-86d6-862ac146ad35.gif" width="400"></p> |  
 
  
Internationalization
-------------------- 

<img src="https://cloud.githubusercontent.com/assets/1408720/7904365/f52e9f1a-07c5-11e5-8f31-36a8fc14ac02.jpg" align="right" />

Gooey is international ready and easily ported to your host language. Languages are controlled via an argument to the `Gooey` decorator. 

    @Gooey(language='russian')
    def main(): 
        ... 

All program text is stored externally in `json` files. So adding new langauge support is as easy as pasting a few key/value pairs in the `gooey/languages/` directory. 

Thanks to some awesome [contributers](https://github.com/chriskiehl/Gooey/graphs/contributors), Gooey currently comes pre-stocked with the following language sets: 

- English
- Dutch
- French
- Portuguese 

Want to add another one? Submit a [pull request!](https://github.com/chriskiehl/Gooey/compare)




-------------------------------------------    



Configuration 
-------------

Just about everything in Gooey can be customized by passing arguments to the decorator. 

| Parameter | Summary | 
|-----------|---------|
| advanced | Toggles whether to show the 'full' configuration screen, or a simplified version | 
| show_config | Skips the configuration all together and runs the program immediately |
| language | Tells Gooey which language set to load from the `gooey/languages` directory.|
|program_name | The name displayed in the title bar of the GUI window. If not supplied, the title defaults to the script name pulled from `sys.argv[0]`. |
| program_description | Sets the text displayed in the top panel of the `Settings` screen. Defaults to the description pulled from `ArgumentParser`. |
| default_size | Initial size of the window | 
| required_cols | Controls how many columns are in the Required Arguments section |
| optional_cols | Controls how many columns are in the Optional Arguments section |
| dump_build_config | Saves a `json` copy of its build configuration on disk for reuse/editing | 



Run Modes
---------

Gooey has a handful of presentation modes so you can tailor its layout to your content type and user's level or experience. 




###Advanced 




The default view is the "full" or "advanced" configuration screen. It has two different layouts depending on the type of command line interface it's wrapping. For most applications, the flat layout will be the one to go with, as its layout matches best to the familiar CLI schema of a primary command followed by many options (e.g. Curl, FFMPEG). 

On the other side is the Column Layout. This one is best suited for CLIs that have multiple paths or are made up of multiple little tools each with their own arguments and options (think: git). It displays the primary paths along the left column, and their corresponding arguments in the right. This is a great way to package a lot of varied functionality into a single app. 

<p align="center">
<img src="https://cloud.githubusercontent.com/assets/1408720/7927433/f06a36cc-08ad-11e5-843e-9322df96d4d6.png">
</p>

Both views present each action in the `Argument Parser` as a unique GUI component. It makes it ideal for presenting the program to users which are unfamiliar with command line options and/or Console Programs in general. Help messages are displayed along side each component to make it as clear as possible which each widget does.

**Setting the layout style:**

Currently, the layouts can't be explicitely specified via a parameter (on the TODO!). The layouts are built depending on whether or not there are `subparsers` used in your code base. So, if you want to trigger the `Column Layout`, you'll need to add a `subparser` to your `argparse` code. 

It can be toggled via the `advanced` parameter in the `Gooey` decorator. 


    @gooey(advanced=True)
    def main():
        # rest of code   
        


--------------------------------------------  



###Basic  

The basic view is best for times when the user is familiar with Console Applications, but you still want to present something a little more polished than a simple terminal. The basic display is accessed by setting the `advanced` parameter in the `gooey` decorator to `False`. 

    @gooey(advanced=False)
    def main():
        # rest of code  

<p align="center">
    <img src="https://cloud.githubusercontent.com/assets/1408720/7904369/f53a4306-07c5-11e5-8e63-b510d6db9953.png">
</p>


----------------------------------------------  

###No Config

No Config pretty much does what you'd expect: it doesn't show a configuration screen. It hops right to the `display` section and begins execution of the host program. This is the one for improving the appearance of little one-off scripts. 

<p align="center">
    <img src="https://cloud.githubusercontent.com/assets/1408720/7904382/f54fe6f2-07c5-11e5-92e4-f72a2ae12862.png">
</p>

---------------------------------------  


Examples
--------

Gooey comes with a bunch of example programs. Examples are located in the `examples` directory inside of the root `gooey` package. However, the easiest way to play with them is to import them into a python project and execute their `main` function. 

    from gooey.examples import widget_demo 
    widget_demo.main() 
    
or    
    
    from gooey.examples import subparser_demo
    subparser_demo.main() 
    
>Note: The examples *must* be run from a Python file! Due to Gooey's file requirements, it won't work from the comman line.     


Screenshots
------------  

| Flat Layout | Column Layout |Success Screen | Error Screen | Warning Dialog |
|-------------|---------------|---------------|--------------|----------------|
| <img src="https://cloud.githubusercontent.com/assets/1408720/7950190/4414e54e-0965-11e5-964b-f717a7adaac6.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950189/4411b824-0965-11e5-905a-3a2b5df0efb3.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950192/44165442-0965-11e5-8edf-b8305353285f.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950188/4410dcce-0965-11e5-8243-c1d832c05887.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950191/4415432c-0965-11e5-9190-17f55460faf3.jpg"> | 



----------------------------------------------  


###Change Log
----------

- Subparser Support! 
- Moved all internal messaging to pubsub
- expanded i18n converage
- allowed returning to the main configuration screen 
- Fixed success checkmark showing on failure 
- Refactoring to beauty 
- Removed parsing code, replaced it with @SylvainDe patch
- Fixed issue #87
- Fixed issue #85
- Argparse no longer required to me in `main` (issue 84)
- Drag and Drop support (`Issue #28`)
- Added drag and drop support
- Added new widget packs: DateChooser, FileChooser, DirChooser
- fixed several parsing related issues. 
- Gooey now has a sane setup.py (thanks to hero user LudoVio) 
- Gooey now builds from json for easy configurability 
    - Side Note: This was done with big strides towards making Gooey language agnostic. Coming Soon! 
- Fixed GUI layout so that resizing works better




Wanna help?
-----------  

Code, translation, graphics? Pull requests are welcome.





  [1]: http://i.imgur.com/7fKUvw9.png
