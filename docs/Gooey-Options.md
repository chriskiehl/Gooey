# Gooey Options 

Using `GooeyParser` we can extend the API of Argparse to support lots of cool additional functionality. 

The main addition to the top-level Argparse API is that we pick up an extra keyword argument called `gooey_options`. This accepts a dictionary of configuration parameters that lets you specify things like custom validators, style overrides, and a bunch of behavioral extensions for the various widget classes.   

`GooeyParser` is a drop-in replacement for `Argparse`. You can import it from the root Gooey namespace like this: 

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

* Global Style Options 
* Custom Widget Options
    * Textarea
    * BlockCheckbox  
    * RadioGroups
* Argument Group Options  


## Global Widget Styles    

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
| visible | bool | hides the entire widget when false. Note: the widget is still present in the UI and will still send along any default values that have been provided in code. This option is here for when you want to hide certain advanced / dangerous inputs from your users |
| full_width | bool | This is a layout hint for this widget. When `True` the widget will fill the entire available space within a given row. Otherwise, it will be sized based on the column rules provided elsewhere. | 



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

### BlockCheckbox

```python
parser.add_argument('-my-arg', widget='BlockCheckbox', gooey_options={
    # allows customizing the checkbox's label
    'checkbox_label': str  
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
  

 




