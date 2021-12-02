# Gooey Options 

Using `GooeyParser` we can extend the API of `argparse` to support lots of cool additional functionality. 

The main addition to the top-level `argparse` API is that we pick up extra keywords: `widget` and `gooey_options`. `widget` is used to specified which UI element to provide for the argument, i.e., a listbox or a file browser. `gooey_options` accepts a dictionary of configuration parameters that lets you specify things like custom validators, style overrides, and a bunch of behavioral extensions for the various widget classes.   

`GooeyParser` is a drop-in replacement for `argparse`. You can import it from the root Gooey namespace like this: 

```python
from gooey import GooeyParser
```

and replace `ArgumentParser` with `GooeyParser`

```python
# parser = ArgumentParser()   # old busted
parser = GooeyParser()        # new hotness
```

and with that, you're ready to rock. 


## Overview

* Global Style/Layout Options 
* Global Config Options 
* Custom Widget Options
    * Textarea
    * BlockCheckbox  
    * Listbox
    * RadioGroups
* Argument Group Options  


## Global Style / Layout Options     

All widgets in Gooey (with the exception of RadioGroups) are made up of three basic components. 

1. Label 
2. Help Text 
3. Input Control

![image](https://user-images.githubusercontent.com/1408720/56450719-cfca9c80-62dc-11e9-93ec-6ad56810e79a.png)

The following options apply to all Widget types in Gooey. 

```python
parser.add_argument('-my-arg', gooey_options={
    'label_color': '#ffffff',
    'label_bg_color': '#ffffff', 
    'help_color': '#ffffff',
    'help_bg_color': '#ffffff',
    'error_color': '#ffffff',
    'error_bg_color': '#ffffff',
    'show_label': bool,
    'show_help': bool, 
    'visible': bool,
    'full_width': bool
})
``` 

| Keyword | Type | Description | 
|---------|------|-------------|
| label_color | hex string | The foreground color of the label text (e.g. `#ff0000`) |
| label_bg_color | hex string | The background color of the label text. |
| help_color | hex string | The foreground color of the help text. |
| help_bg_color | hex string | The background color of the help text. |
| error_color | hex string | The foreground color of the error text (when visible). |
| error_bg_color | hex string | The background color of the error text (when visible). |
| show_label | bool | Toggles whether or not to display the label text |
| show_help | bool | Toggles whether or not to display the help text |
| visible | bool | Hides the entire widget when `False`. Note: the widget is still present in the UI and will still send along any default values that have been provided in code. This option is here for when you want to hide certain advanced / dangerous inputs from your GUI users. |
| full_width | bool | This is a layout hint for this widget. When `True` the widget will fill the entire available space within a given row. Otherwise, it will be sized based on the column rules provided elsewhere. | 


## Global Config Options 

> new in 1.0.8

All widgets in Gooey accept an `initial_value` option to seed the UI. 

```python
parser.add_argument('-my-arg', widget='Textarea', gooey_options={
    'initial_value': 'Hello world!'  
})
```

## Individual Widget Options

A few widgets have additional options for controlling their layout and behavior. 

### Textarea

```python
parser.add_argument('-my-arg', widget='Textarea', gooey_options={
    # height of the text area in pixels
    'height': int,    
    # prevents the user from editing when true
    'readonly': bool  
})
``` 

### IntegerField

```python
parser.add_argument('-my-arg', widget='IntegerField', gooey_options={
    'min': int, 
    'max': int, 
    'increment': int  
})
``` 


### DecimalField

```python
parser.add_argument('-my-arg', widget='IntegerField', gooey_options={
    'min': float, 
    'max': float, 
    'increment': float,
    'precision': int  # 0 - 20
})
``` 

### Slider

The Slider is just a reskinned IntegerField, so it has the same options
 
```python
parser.add_argument('-my-arg', widget='Slider', gooey_options={
    'min': int, 
    'max': int, 
    'increment': int  
})
``` 


### BlockCheckbox

```python
parser.add_argument('-my-arg', widget='BlockCheckbox', gooey_options={
    # allows customizing the checkbox's label
    'checkbox_label': str  
})
```
 
### Listbox

```python
parser.add_argument('-my-arg', widget='Listbox', gooey_options={
    # height of the listbox in pixels
    'height': int
})
```

### Radio Group  

```python
parser.add_mutually_exclusive_group(gooey_options={
    # Pre-select a specific option within a mutually exclusive group. 
    # default behavior is to have all options unselected by default.  
    'initial_selection': int
})
```


## Argument Groups

Argument Groups take a number of `gooey_options` to help control layout. 

```python
parser.add_argument_group('MyGroup', desription='my cool group', gooey_options={
    'show_border': bool,
    'show_underline': bool,
    'label_color': '#FF9900',
    'columns': int,
    'margin_top': int
})
``` 
  
| Keyword | Type | Description | 
|---------|------|-------------|
| show_border | bool | When `True` a labeled border will surround all widgets added to this group. |
| show_underline | bool | Controls whether or not to display the underline when using the default border style |
| label_color | hex string | The foreground color for the group name |
| columns | int | Controls the number of widgets on each row | 
| margin_top | int | specifies the top margin in pixels for this group |

![image](https://user-images.githubusercontent.com/1408720/57576112-9c77bb00-740d-11e9-9dac-4e798699a35c.png)



## File and Folder choosers

File and Folder Choosers Groups take a number of `gooey_options` to help control default values. 

```python
parser.add_argument("FileChooser", widget="FileChooser",
                            gooey_options={
                                'wildcard':
                                    "Comma separated file (*.csv)|*.csv|"
                                    "All files (*.*)|*.*",
                                'default_dir': "c:/batch",
                                'default_file': "def_file.csv",
                                'message': "pick me"
                            }
                            )
parser.add_argument("DirectoryChooser", widget="DirChooser",
                            gooey_options={
                                'wildcard':
                                    "Comma separated file (*.csv)|*.csv|"
                                    "All files (*.*)|*.*",
                                'message': "pick folder",
                                'default_path': "c:/batch/stuff"
                            }
                            )
parser.add_argument("FileSaver", widget="FileSaver",
                            gooey_options={
                                'wildcard':
                                    "JPG (*.jpg)|*.jpg|"
                                    "All files (*.*)|*.*",
                                'message': "pick folder",
                                'default_dir': "c:/projects",
                                'default_file': "def_file.csv"
                            }
                            )
parser.add_argument("MultiFileSaver", widget="MultiFileChooser",
                            gooey_options={
                                'wildcard':
                                    "Comma separated file (*.csv)|*.csv|"
                                    "All files (*.*)|*.*",
                                'message': "pick folder",
                                'default_dir': "c:/temp",
                                'default_file': "def_file.csv"
                            }
                            )
``` 
  
| Keyword | Type | Description | 
|---------|------|-------------|
| wildcard | string | Sets the wildcard, which can contain multiple file types, for example: "BMP files (.bmp)&#124;.bmp&#124;GIF files (.gif)&#124;.gif" |
| message | string | 	Sets the message that will be displayed on the dialog. |
| default_dir | string | The default directory |
| default_file | string | The default filename | 
| default_path | string | The default path |


  
