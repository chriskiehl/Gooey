Gooey (Beta)
=====  
Turn (almost) any Python 2 or 3 Console Program into a GUI application with one line

<p align="center">
    <img src="https://cloud.githubusercontent.com/assets/1408720/7904381/f54f97f6-07c5-11e5-9bcb-c3c102920769.png" />
</p>

# Gooey now supports Python 3!!


Table of Contents
-----------------  

- [Gooey](#gooey)
- [Table of contents](#table-of-contents)
- [Latest Update](#latest-update)
- [Quick Start](#quick-start)
    - [Installation Instructions](#installation-instructions)
    - [Usage](#usage)
    - [Examples](#examples)
- [What It Is](#what-is-it)
- [Why Is It](#why)
- [Who is this for](#who-is-this-for)
- [How does it work](#how-does-it-work)
- [Internationalization](#internationalization)
- [Global Configuration](#global-configuration)
- [Layout Customization](#layout-customization)
- [Run Modes](#run-modes)
    - [Full/Advanced](#advanced)
    - [Basic](#basic)
    - [No Config](#no-config)
- [Input Validation](#input-validation)
- [Using Dynamic Values](#using-dynamic-values)
- [Showing Progress](#showing-progress)
- [Customizing Icons](#customizing-icons)
- [Packaging](#packaging)
- [Screenshots](#screenshots)
- [Contributing](#wanna-help)
- [Image Credits](#image-credits)



----------------  


## Quick Start


### Installation instructions


The easiest way to install Gooey is via `pip`

    pip install Gooey 

Alternatively, you can install Gooey by cloning the project to your local directory

    git clone https://github.com/chriskiehl/Gooey.git

run `setup.py` 

    python setup.py install
    
**NOTE:** Python 2 users must manually install WxPython! Unfortunately, this cannot be done as part of the pip installation and should be manually downloaded from the [wxPython website](http://www.wxpython.org/download.php).



### Usage  

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
           target=executable_cmd,     # Explicitly set the subprocess executable arguments
           program_name='name',       # Defaults to script name
           program_description,       # Defaults to ArgParse Description
           default_size=(610, 530),   # starting size of the GUI
           required_cols=1,           # number of columns in the "Required" section
           optional_cols=2,           # number of columbs in the "Optional" section
           dump_build_config=False,   # Dump the JSON Gooey uses to configure itself
           load_build_config=None,    # Loads a JSON Gooey-generated configuration
           monospace_display=False)   # Uses a mono-spaced font in the output screen
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

### Examples

Gooey downloaded and installed? Great! Wanna see it in action? Head over the the [Examples Repository](https://github.com/chriskiehl/GooeyExamples) to download a few ready-to-go example scripts. They'll give you a quick tour of all Gooey's various layouts, widgets, and features. 

[Direct Download](https://github.com/chriskiehl/GooeyExamples/archive/master.zip)


    
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

#### Mappings: 

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

### GooeyParser

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
|  DirChooser/FileChooser/MultiFileChooser   | <p align="center"><img src="https://cloud.githubusercontent.com/assets/1408720/7904377/f5483b28-07c5-11e5-9d01-1935635fc22d.gif" width="400"></p> | 
|  DateChooser   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| <p align="center"><img src="https://cloud.githubusercontent.com/assets/1408720/7904376/f544756a-07c5-11e5-86d6-862ac146ad35.gif" width="400"></p> |
| PasswordField | <p align="center"><img src="https://user-images.githubusercontent.com/1408720/28953722-eae72cca-788e-11e7-8fa1-9a1ef332a053.png" width="400"></p> |
| Listbox | ![image](https://user-images.githubusercontent.com/1408720/31590191-fadd06f2-b1c0-11e7-9a49-7cbf0c6d33d1.png) |


 
  
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



Global Configuration 
--------------------

Just about everything in Gooey's overall look and feel can be customized by passing arguments to the decorator. 

| Parameter | Summary | 
|-----------|---------|
| encoding | Text encoding to use when displaying characters (default: 'utf-8') | 
| use_legacy_titles | Rewrites the default argparse group name from "Positional" to "Required". This is primarily for retaining backward compatibilty with previous versions of Gooey (which had poor support/awareness of groups and did its own naive bucketing of arguments). |
| advanced | Toggles whether to show the 'full' configuration screen, or a simplified version |
| auto_start | Skips the configuration all together and runs the program immediately |
| language | Tells Gooey which language set to load from the `gooey/languages` directory.|
| target | Tells Gooey how to re-invoke itself. By default Gooey will find python, but this allows you to specify the program (and arguments if supplied).|
|program_name | The name displayed in the title bar of the GUI window. If not supplied, the title defaults to the script name pulled from `sys.argv[0]`. |
| program_description | Sets the text displayed in the top panel of the `Settings` screen. Defaults to the description pulled from `ArgumentParser`. |
| default_size | Initial size of the window | 
| required_cols | Controls how many columns are in the Required Arguments section <br> :warning: **Deprecation notice:** See [Group Parameters](#group-configuration) for modern layout controls|
| optional_cols | Controls how many columns are in the Optional Arguments section <br> :warning: **Deprecation notice:** See [Group Parameters](#group-configuration) for modern layout controls|
| dump_build_config | Saves a `json` copy of its build configuration on disk for reuse/editing | 
| load_build_config | Loads a `json` copy of its build configuration from disk | 
| monospace_display | Uses a mono-spaced font in the output screen <br> :warning: **Deprecation notice:** See [Group Parameters](#group-configuration) for modern font configuration| 
| image_dir | Path to the directory in which Gooey should look for custom images/icons |
| language_dir | Path to the directory in which Gooey should look for custom languages files |
| disable_stop_button | Disable the `Stop` button when running |
| show_stop_warning | Displays a warning modal before allowing the user to force termination of your program |
| force_stop_is_error | Toggles whether an early termination by the shows the success or error screen |
| show_success_modal | Toggles whether or not to show a summary modal after a successful run |
| run_validators | Controls whether or not to have Gooey perform validation before calling your program |
| poll_external_updates | (Experimental!) When True, Gooey will call your code with a `gooey-seed-ui` CLI argument and use the response to fill out dynamic values in the UI (See: [Using Dynamic Values](#using-dynamic-values))|
| return_to_config | When True, Gooey will return to the configuration settings window upon successful run |
| progress_regex | A text regex used to pattern match runtime progress information. See: [Showing Progress](#showing-progress) for a detailed how-to | 
| progress_expr | A python expression applied to any matches found via the `progress_regex`. See: [Showing Progress](#showing-progress) for a detailed how-to |
| disable_progress_bar_animation | Disable the progress bar | 
| navigation | Sets the "navigation" style of Gooey's top level window. <br>Options: <table> <thead> <tr><th>TABBED</th><th>SIDEBAR</th></tr></thead> <tbody> <tr> <td><img src="https://user-images.githubusercontent.com/1408720/34464826-2a946ba2-ee47-11e7-92a4-4afeb49dc9ca.png" width="200" height="auto"></td><td><img src="https://user-images.githubusercontent.com/1408720/34464847-9918fbb0-ee47-11e7-8d5f-0d42631c2bc0.png" width="200" height="auto"></td></tr></tbody></table>|
| sidebar_title | <img src="https://user-images.githubusercontent.com/1408720/34472159-1bfedbd0-ef10-11e7-8bc3-b6d69febb8c3.png" width="250" height="auto" align="right"> Controls the heading title above the SideBar's navigation pane. Defaults to: "Actions" |
| show_sidebar | Show/Hide the sidebar in when navigation mode == `SIDEBAR` |
| body_bg_color | HEX value of the main Gooey window |
| header_bg_color | HEX value of the header background | 
| header_height | height in pixels of the header | 
| header_show_title | Show/Hide the header title | 
| header_show_subtitle | Show/Hide the header subtitle | 
| footer_bg_color | HEX value of the Footer background | 
| sidebar_bg_color | HEX value of the Sidebar's background | 
| terminal_panel_color | HEX value of the terminal's panel | 
| terminal_font_color | HEX value of the font displayed in Gooey's terminal | 
| terminal_font_family | Name of the Font Family to use in the terminal | 
| terminal_font_weight | Weight of the font (NORMAL|BOLD) | 
| terminal_font_size | Point size of the font displayed in the terminal | 
| error_color | HEX value of the text displayed when a validation error occurs |



Layout Customization
--------------------

You can achieve fairly flexible layouts with Gooey by using a few simple customizations. 

At the highest level, you have several overall layout options controllable via various arguments to the Gooey decorator.


| `show_sidebar=True` | `show_sidebar=False` | `navigation='TABBED'` |  `tabbed_groups=True` |
|---------------------|----------------------|----------------------|------------------------|
|<img src="https://user-images.githubusercontent.com/1408720/34464847-9918fbb0-ee47-11e7-8d5f-0d42631c2bc0.png" width="400"> |<img src="https://user-images.githubusercontent.com/1408720/35487799-762aa308-0434-11e8-8eb3-1e9fab2d13ae.png" width="400"> |<img src="https://user-images.githubusercontent.com/1408720/34464835-5ba9b0e4-ee47-11e7-9561-55e3647c2165.png" width="400"> |<img src="https://user-images.githubusercontent.com/1408720/34464826-2a946ba2-ee47-11e7-92a4-4afeb49dc9ca.png" width="400"> |


**Grouping Inputs**

By default, if you're using Argparse with Gooey, your inputs will be split into two buckets: `positional` and `optional`. However, these aren't always the most descriptive groups to present to your user. You can arbitrarily bucket inputs into logic groups and customize the layout of each. 

With `argparse` this is done via `add_argument_group()`

<img src="https://user-images.githubusercontent.com/1408720/35487956-a4c9915e-0436-11e8-8a11-fd21528aedf0.png" align="right" width="410">

```
parser = ArgumentParser()
search_group = parser.add_argument_group(
    "Search Options", 
    "Customize the search options"
)
```

You can add arguments to the group as normal 

```
search_group.add_argument(
    '--query', 
    help='Base search string'
) 
```

Which will display them as part of the group within the UI. 

**Customizing Group Layout**

> Note: Make sure you're using GooeyParser if you want to take advantage of the layout customizations!  

With a group created, we can now start tweaking how it looks! `GooeyParser` extends the API of `add_argument_group` to accept an additional keyword argument: `gooey_options`.  It accepts two keys: `show_border` and `columns`

```
gooey_options={
    'show_border': Bool,
    'columns': 1-100 
}
```

<img src="https://user-images.githubusercontent.com/1408720/35488154-e201ab90-0438-11e8-9479-3a27fd1c523e.png" align="right" width="400">

`show_border` is nice for visually tying together closely related items within a parent group. Setting it to `true` will draw a small border around all of the inputs and nest the title at the top. 

`columns` controls how many many items get places on each row within the 













Run Modes
---------

Gooey has a handful of presentation modes so you can tailor its layout to your content type and user's level or experience. 




### Advanced 




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



### Basic  

The basic view is best for times when the user is familiar with Console Applications, but you still want to present something a little more polished than a simple terminal. The basic display is accessed by setting the `advanced` parameter in the `gooey` decorator to `False`. 

    @gooey(advanced=False)
    def main():
        # rest of code  

<p align="center">
    <img src="https://cloud.githubusercontent.com/assets/1408720/7904369/f53a4306-07c5-11e5-8e63-b510d6db9953.png">
</p>


----------------------------------------------  

### No Config

No Config pretty much does what you'd expect: it doesn't show a configuration screen. It hops right to the `display` section and begins execution of the host program. This is the one for improving the appearance of little one-off scripts. 

<p align="center">
    <img src="https://cloud.githubusercontent.com/assets/1408720/7904382/f54fe6f2-07c5-11e5-92e4-f72a2ae12862.png">
</p>

---------------------------------------  


### Input Validation


<img src="https://user-images.githubusercontent.com/1408720/34464861-0e82c214-ee48-11e7-8f4a-a8e00721efef.png" width="400" height="auto" align="right" />


>:warning: 
>Note! This functionality is experimental. Its API may be changed or removed alltogether. Feedback/thoughts on this feature is welcome and encouraged! 

Gooey can optionally do some basic pre-flight validation on user input. Internally, it uses these validator functions to check for the presence of required arguments. However, by using [GooeyParser](#gooeyparser), you can extend these functions with your own validation rules. This allows Gooey to show much, much more user friendly feedback before it hands control off to your program. 


**Writing a validator:**

Validators are specified as part of the `gooey_options` map available to `GooeyParser`. It's a simple map structure made up of a root key named `validator` and two internal pairs: 

 * `test` The inner body of the validation test you wish to perform 
 * `message` the error message that should display given a validation failure
 
e.g.

```
gooey_options={
    'validator':{
        'test': 'len(user_input) > 3',
        'message': 'some helpful message'
    }
}
```

**The `test` function**

Your test function can be made up of any valid Python expression. It receives the variable `user_input` as an argument against which to perform its validation. Note that all values coming from Gooey are in the form of a string, so you'll have to cast as needed in order to perform your validation.   

**Full Code Example**

```
from gooey.python_bindings.gooey_decorator import Gooey
from gooey.python_bindings.gooey_parser import GooeyParser

@Gooey
def main():
    parser = GooeyParser(description='Example validator')
    parser.add_argument(
        'secret',
        metavar='Super Secret Number',
        help='A number specifically between 2 and 14',
        gooey_options={
            'validator': {
                'test': '2 <= int(user_input) <= 14',
                'message': 'Must be between 2 and 14'
            }
        })

    args = parser.parse_args()

    print("Cool! Your secret number is: ", args.secret)
```

<img src="https://user-images.githubusercontent.com/1408720/34465024-f011ac3e-ee4f-11e7-80ae-330adb4c47d6.png" width="400" height="auto" align="left" />

With the validator in place, Gooey can present the error messages next to the relevant input field if any validators fail.  



---------------------------------------
  

## Using Dynamic Values

>:warning: 
>Note! This functionality is experimental. Its API may be changed or removed alltogether. Feedback on this feature is welcome and encouraged! 

Gooey's Choice style fields (Dropdown, Listbox) can be fed a dynamic set of values at runtime by enabling the `poll_external_updates` option. This will cause Gooey to request updated values from your program everytime the user visits the Configuration page. This can be used to, for instance, show the result of a previous execution on the config screen without requiring that the user restart the program. 

**How does it work?**

<img src="https://user-images.githubusercontent.com/1408720/35487459-bd7fe938-0430-11e8-9f6d-fa8f703b9da5.gif" align="right" width="420"/>

At runtime, whenever the user hits the Configuration screen, Gooey will call your program with a single CLI argument: `gooey-seed-ui`. This is a request to your program for updated values for the UI. In response to this, on `stdout`, your program should return a JSON string mapping cli-inputs to a list of options.

For example, assuming a setup where you have a dropdown that lists user files:

```
 ...
 parser.add_argument(
        '--load',
        metavar='Load Previous Save',
        help='Load a Previous save file',
        dest='filename',
        widget='Dropdown',
        choices=list_savefiles(),
    )
```

Here the input we want to populate is `--load`. So, in response to the `gooey-seed-ui` request, you would return a JSON string with `--load` as the key, and a list of strings that you'd like to display to the user as the value. e.g.  

```
{"--load": ["Filename_1.txt", "filename_2.txt", ..., "filename_n.txt]}
```

Checkout the full example code in the [Examples Repository](https://github.com/chriskiehl/GooeyExamples/blob/master/examples/dynamic_updates.py). Or checkout a larger example in the silly little tool that spawned this feature: [SavingOverIt](https://github.com/chriskiehl/SavingOverIt). 

-------------------------------------

## Showing Progress

<img src="https://user-images.githubusercontent.com/1408720/45590349-55bbda80-b8eb-11e8-9aed-b4fe377756ac.png" align="right" width="420"/>

Giving visual progress feedback with Gooey is easy! If you're already displaying textual progress updates, you can tell Gooey to hook into that existing output in order to power its Progress Bar. 

For simple cases, output strings which resolve to a numeric representation of the completion percentage (e.g. `Progress 83%`) can be pattern matched and turned into a progress bar status with a simple regular expression (e.g. `@Gooey(progress_regex=r"^progress: (\d+)%$")`). 

For more complicated outputs, you can pass in a custom evaluation expression (`progress_expr`) to transform the things however you need. 

**Program Output:**

```
progress: 1/100
progress: 2/100
progress: 3/100
...
```

**Regex and Processing Expression**

```python
@Gooey(progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
       progress_expr="current / total * 100")
```

There are lots of options for telling Gooey about progress as your program is running. Checkout the [Gooey Examples](https://github.com/chriskiehl/GooeyExamples) repository for more detailed usage and examples! 

| progress_regex | A text regex used to pattern match runtime progress information. See: [Showing Progress](#showing-progress) for a detailed how-to |
| progress_expr | A python expression applied to any matches found via the `progress_regex`. See: [Showing Progress](#showing-progress) for a detailed how-to |

--------------------------------------


## Customizing Icons

Gooey comes with a set of six default icons. These can be overridden with your own custom images/icons by telling Gooey to search additional directories when initializing. This is done via the `image_dir` argument to the `Goeey` decorator. 

    @Gooey(program_name='Custom icon demo', image_dir='/path/to/my/image/directory')
    def main():
        # rest of program
        
Images are discovered by Gooey based on their _filenames_. So, for example, in order to supply a custom configuration icon, simply place an image with the filename `config_icon.png` in your images directory. These are the filenames which can be overridden:

* program_icon.ico
* success_icon.png
* running_icon.png
* loading_icon.gif
* config_icon.png
* error_icon.png


## Packaging

Thanks to some [awesome contributers](https://github.com/chriskiehl/Gooey/issues/58), packaging Gooey as an executable is super easy. 

The tl;dr [pyinstaller](https://github.com/pyinstaller/pyinstaller) version is to drop this [build.spec](https://github.com/chriskiehl/Gooey/files/29568/build.spec.txt) into the root directory of your application. Edit its contents so that the `application` and `name` are relevant to your project, then execute `pyinstaller build.spec` to bundle your app into a ready-to-go executable. 

Detailed step by step instructions can be found [here](http://chriskiehl.com/article/packaging-gooey-with-pyinstaller/). 


Screenshots
------------  

| Flat Layout | Column Layout |Success Screen | Error Screen | Warning Dialog |
|-------------|---------------|---------------|--------------|----------------|
| <img src="https://cloud.githubusercontent.com/assets/1408720/7950190/4414e54e-0965-11e5-964b-f717a7adaac6.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950189/4411b824-0965-11e5-905a-3a2b5df0efb3.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950192/44165442-0965-11e5-8edf-b8305353285f.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950188/4410dcce-0965-11e5-8243-c1d832c05887.jpg"> | <img src="https://cloud.githubusercontent.com/assets/1408720/7950191/4415432c-0965-11e5-9190-17f55460faf3.jpg"> | 

| Custom Groups | Tabbed Groups | Tabbed Navigation | Sidebar Navigation | Input Validation |
|-------------|---------------|---------------|--------------|----------------|
| <img src="https://user-images.githubusercontent.com/1408720/34464824-c044d57a-ee46-11e7-9c35-6e701a7c579a.png"> | <img src="https://user-images.githubusercontent.com/1408720/34464826-2a946ba2-ee47-11e7-92a4-4afeb49dc9ca.png"> | <img src="https://user-images.githubusercontent.com/1408720/34464835-5ba9b0e4-ee47-11e7-9561-55e3647c2165.png"> | <img src="https://user-images.githubusercontent.com/1408720/34464847-9918fbb0-ee47-11e7-8d5f-0d42631c2bc0.png"> | <img src="https://user-images.githubusercontent.com/1408720/34464861-0e82c214-ee48-11e7-8f4a-a8e00721efef.png"> | 





----------------------------------------------  







Wanna help?
-----------  

Code, translation, graphics? Pull requests are welcome.





  [1]: http://i.imgur.com/7fKUvw9.png
