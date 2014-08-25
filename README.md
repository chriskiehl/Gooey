Gooey (Beta)
=====  
Turn (almost) any Console Program into a GUI application with one line  

<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/primary.png"/>
</p> 



**Update**
----------  

First attempt at packaging went not as planned. I've since swapped from `distutils` to `setuptools` and that seems to have remedied the issue. However, if you do receive an error after running `setup.py` please let me know by submitting an issue! It was caused by the image and language files not copying to the correct location during setup, so in a pinch you can remedy this by manually copying `/images` and `/languages` from the repo into `/site-packages/gooey`. 




Table of Contents
-----------------  

- [Gooey](#gooey)
- [Table of contents](#table-of-contents)
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
- [Final Screen](#final-screen)

- [TODO](#todo)
- [Contributing](#wanna-help)
- [Image Credits](#image-credits)


Quick Start
-------------  

###Installation instructions

To install Gooey, simply clone the project to your local directory

    git clone https://github.com/chriskiehl/Gooey.git

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
	       config=Boolean,            # skip config screens all together
	       program_name='name',       # Defaults to script name 
	       program_description        # Defaults to ArgParse Description
      )
    def main():
      # rest of app
	        
See: [How does it Work](#how-does-it-work) section for details on each option.

    
What is it? 
-----------  

Gooey converts your Console Applications into end-user friendly GUI applications. It lets you focus on building robust, configurable programs in a familiar way, all without having to worry about how it will be presented to and interacted with by your average user. 

Why?
---  

Because as much as we love the command prompt, the rest of the world looks at it like some kind of ugly relic from the early '80s. On top of that, more often than not programs need to do more than just one thing, and that means giving options, which previously meant either building a GUI, or trying to explain how to supply arguments to a Console Application. Gooey was made to (hopefully) solve those problems. It makes programs easy to use, and pretty to look at! 

Who is this for?
----------------  

If you're building utilities for yourself, other programmers, or something which produces a result that you want capture and pipe over to another console application (e.g. *nix philosophy utils), Gooey probably isn't the tool for you. However, if you're building 'run and done,' around the office style scripts, things that shovel bits from point A to point B, or simply something that's targeted at a non-programmer, Gooey is the perfect tool for the job. It lets you build as complex of an application as your heart desires all while getting the GUI side for free. 

How does it work? 
------------------  

Gooey is attached to your code via a simple decorator on your `main` method. 

    @gooey      <--- all it takes! :)
    def main():
      # rest of code

At runtime, it loads the Abstract Syntax Tree for your module and parses it for all references to `ArgumentParser` (The older `optparse` is currently not supported). These references are then extracted, assigned a `component type` based on the `'action'` they provide, and finally used to assemble the GUI.  

####Mappings: 


Currently, the `ArgumentParser._actions` are mapped to the following `WX` components. 

| Parser Action    | Widget    | Example |
|:----------------------|-----------|------|
| store  |  TextCtrl |  <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/general_tb.png"/>|
| store_const   |     CheckBox |  <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/check_box.png"/>|
|   store_true|        CheckBox | <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/check_box.png"/>|
|  store_False  |      CheckBox|  <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/check_box.png"/>   |
|       append |       TextCtrl |  <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/general_tb.png"/>  | 
|        count|              DropDown &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/count_dropdown.png"/> | 
|choice &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|        DropDown | <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/options_dropdown.png"/> |
  
  
-------------------------------------------  




Configuration 
------------   

Gooey comes in three main flavors.  

- Full/Advanced 
- Basic
- No config  

And each with the following options: 


| Parameter | Summary | 
|-----------|---------|
| language | Gooey is (kind of) international ready (sans unicode issues (TODO). All program text is stored in an external `json` file. Translating to your host language only requires filling in the key/value pairs.|
|program_name | The name displayed in the title bar of the GUI window. If the value is `None`, the title is pulled from `sys.argv[0]`. |
| program_description | Sets the text displayed in the top panel of the `Settings` screen. If `None` the decription is pulled from the  `ArgumentParser`. |  





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

No Config pretty much does what you'd expect: it doesn't show a configuration screen. It hops right to the `display` section and begins execution of the host program. This is the guy for classing up the delivery of little one-off scripts. 

<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/no_config.png">
</p>

---------------------------------------  

Final Screen
------------  
<p align="center">
    <img src="https://raw.githubusercontent.com/chriskiehl/Gooey/master/resources/final_screen.png">
</p>

----------------------------------------------  



    
    

TODO
----  

* Add to pypi
* Themes 
* Add ability to customize the mapping between `Parser` actions and `wxComponents`. For instance, if your program had a file as a required argument, it'd be far more useful to the end user to supply a `wx.FileDialog` rather than a simple `TextBox`. 
* Update graphics
* Optparse support? 
* Get OS X version working. 



Wanna help?
-----------  

* Do you art? I'd love to swap out the graphics to something more stylistically unified. 
* Programmer? Pull requests are super welcome. The projects style is *fantastically* inconsistent, though. So be warned :) I tried to follow the WxWidgets style of Leading Capital methods and CamelCased variables, but.. Python habits die hard. So, there are underscores littered all over the place. 





  [1]: http://i.imgur.com/7fKUvw9.png
