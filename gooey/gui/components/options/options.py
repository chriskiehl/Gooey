from gooey.gui.components.filtering.prefix_filter import PrefixTokenizers



def _include_layout_docs(f):
    """
    Combines the layout_options docsstring with the
    wrapped function's doc string.
    """
    f.__doc__ = (f.__doc__ or '') + LayoutOptions.__doc__
    return f


def _include_global_option_docs(f):
    """
    Combines docstrings for options available to
    all widget types.
    """
    _doc = """:param initial_value:  Sets the initial value in the UI. 
    """
    f.__doc__ = (f.__doc__ or '') + _doc
    return f

def _include_chooser_msg_wildcard_docs(f):
    """
    Combines the basic Chooser options (wildard, message) docsstring
    with the wrapped function's doc string.
    """
    _doc = """:param wildcard: Sets the wildcard, which can contain multiple file types, for 
                     example: "BMP files (.bmp)|.bmp|GIF files (.gif)|.gif"
    :param message:  Sets the message that will be displayed on the dialog.
    """
    f.__doc__ = (f.__doc__ or '') + _doc
    return f

def _include_choose_dir_file_docs(f):
    """
        Combines the basic Chooser options (wildard, message) docsstring
        with the wrapped function's doc string.
        """
    _doc = """:param default_dir: The default directory selected when the dialog spawns 
    :param default_file: The default filename used in the dialog
    """
    f.__doc__ = (f.__doc__ or '') + _doc
    return f



def LayoutOptions(label_color=None,
                  label_bg_color=None,
                  help_color=None,
                  help_bg_color=None,
                  error_color=None,
                  error_bg_color=None,
                  show_label=True,
                  show_help=True,
                  visible=True,
                  full_width=False):
    """
    Layout Options:
    ---------------

    Color options can be passed either as a hex string ('#ff0000') or as
    a collection of RGB values (e.g. `[255, 0, 0]` or `(255, 0, 0)`)

    :param label_color:    The foreground color of the label text
    :param label_bg_color: The background color of the label text.
    :param help_color:     The foreground color of the help text.
    :param help_bg_color:  The background color of the help text.
    :param error_color:    The foreground color of the error text (when visible).
    :param error_bg_color: The background color of the error text (when visible).
    :param show_label:     Toggles whether or not to display the label text
    :param show_help:      Toggles whether or not to display the help text
    :param visible:        Hides the entire widget when False. Note: the widget
                           is still present in the UI and will still send along any
                           default values that have been provided in code. This option
                           is here for when you want to hide certain advanced / dangerous
                           inputs from your GUI users.
    :param full_width:     This is a layout hint for this widget. When True the widget
                           will fill the entire available space within a given row.
                           Otherwise, it will be sized based on the column rules
                           provided elsewhere.
    """
    return _clean(locals())



@_include_layout_docs
@_include_global_option_docs
def TextField(initial_value=None, validator=None, **layout_options):
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def PasswordField(initial_value=None, validator=None, **layout_options):
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def IntegerField(initial_value=None, validator=None, min=0, max=100, increment=1, **layout_options):
    """
    :param min: The minimum value allowed
    :param max: The maximum value allowed
    :param increment: The step size of the spinner
    """
    return _clean(locals())

@_include_layout_docs
@_include_global_option_docs
def Slider(initial_value=None, validator=None, min=0, max=100, increment=1, **layout_options):
    """
    :param min: The minimum value allowed
    :param max: The maximum value allowed
    :param increment: The step size of the slider
    """
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def DecimalField(validator=None,
                 initial_value=None,
                 min=0.0,
                 max=1.0,
                 increment=0.01,
                 precision=2,
                 **layout_options):
    """
    :param min: The minimum value allowed
    :param max: The maximum value allowed
    :param increment: The step size of the spinner
    :param precision: The precision of the decimal (0-20)
    """
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def TextArea(initial_value=None, height=None, readonly=False, validator=None, **layout_options):
    """
    :param height:   The height of the TextArea.
    :param readonly: Controls whether or not user's may modify the contents
    """
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def RichTextConsole(**layout_options):
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def ListBox(initial_value=None, height=None, **layout_options):
    """
    :param height: The height of the ListBox
    """
    return _clean(locals())

# TODO: what are this guy's layout options..?
def MutexGroup(initial_selection=None, title=None, **layout_options):
    """
    :param initial_selection: The index of the option which should be initially selected.
    :param title:             Adds the supplied title above the RadioGroup options (when present)
    """
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def Dropdown(initial_value=None, **layout_options):
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def Counter(initial_value=None, **layout_options):
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def CheckBox(initial_value=None, **layout_options):
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def BlockCheckBox(initial_value=None, checkbox_label=None, **layout_options):
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
def FilterableDropdown(placeholder=None,
                       empty_message=None,
                       max_size=80,
                       search_strategy=None,
                       initial_value=None,
                       **layout_options):
    """
    :param placeholder:     Text to display when the user has provided no input
    :param empty_message:   Text to display if the user's query doesn't match anything
    :param max_size:        maximum height of the dropdown
    :param search_strategy: see: PrefixSearchStrategy
    """
    return _clean(locals())


def PrefixSearchStrategy(
                   choice_tokenizer=PrefixTokenizers.WORDS,
                   input_tokenizer=PrefixTokenizers.REGEX('\s'),
                   ignore_case=True,
                   operator='AND',
                   index_suffix=False):
    """
    :param choice_tokenizer: See: PrefixTokenizers - sets the tokenization strategy
                             for the `choices`
    :param input_tokenizer:  See: PrefixTokenizers sets how the users's `input` get tokenized.
    :param ignore_case:      Controls whether or not to honor case while searching
    :param operator:         see: `OperatorType` - controls whether or not individual
                             search tokens
                             get `AND`ed or `OR`d together when evaluating a match.
    :param index_suffix:     When enabled, generates a suffix-tree to enable efficient
                             partial-matching against any of the tokens.
    """
    return {**_clean(locals()), 'type': 'PrefixFilter'}


@_include_layout_docs
@_include_global_option_docs
@_include_choose_dir_file_docs
@_include_chooser_msg_wildcard_docs
def FileChooser(wildcard=None,
                default_dir=None,
                default_file=None,
                message=None,
                initial_value=None,
                **layout_options):
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
@_include_chooser_msg_wildcard_docs
def DirectoryChooser(wildcard=None,
                    default_path=None,
                    message=None,
                    initial_value=None,
                    **layout_options):
    """
    :param default_path: The default path selected when the dialog spawns
    """
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
@_include_choose_dir_file_docs
@_include_chooser_msg_wildcard_docs
def FileSaver(wildcard=None,
              default_dir=None,
              default_file=None,
              message=None,
              initial_value=None,
              **layout_options):
    return _clean(locals())


@_include_layout_docs
@_include_global_option_docs
@_include_choose_dir_file_docs
@_include_chooser_msg_wildcard_docs
def MultiFileSaver(wildcard=None,
              default_dir=None,
              default_file=None,
              message=None,
              initial_value=None,
              **layout_options):
    return _clean(locals())


def ExpressionValidator(test=None, message=None):
    """
    Creates the data for a basic expression validator.

    Your test function can be made up of any valid Python expression.
    It receives the variable user_input as an argument against which to
    perform its validation. Note that all values coming from Gooey
    are in the form of a string, so you'll have to cast as needed
    in order to perform your validation.
    """
    return {**_clean(locals()), 'type': 'ExpressionValidator'}


def RegexValidator(test=None, message=None):
    """
    Creates the data for a basic RegexValidator.

    :param test:    the regex expression. This should be the expression
                    directly (i.e. `test='\d+'`). Gooey will test
                    that the user's input satisfies this expression.
    :param message: The message to display if the input doesn't match
                    the regex
    """
    return {**_clean(locals()), 'type': 'RegexValidator'}


def ArgumentGroup(show_border=False,
                  show_underline=True,
                  label_color=None,
                  columns=None,
                  margin_top=None):
    """
    :param show_border:    When True a labeled border will surround all widgets added to this group.
    :param show_underline: Controls whether or not to display the underline when using the default border style
    :param label_color:    The foreground color for the group name
    :param columns:        Controls the number of widgets on each row
    :param margin_top:     specifies the top margin in pixels for this group
    """
    return _clean(locals())





def _clean(options):
    cleaned = {k: v for k, v in options.items()
               if v is not None and k != "layout_options"}
    return {**options.get('layout_options', {}), **cleaned}

