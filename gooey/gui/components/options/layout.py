from pyrsistent import pmap

from gooey.gui.components.options.validation import validate_color, _unit

layout_validators = {
    'label_color': validate_color,
    'label_bg_color': validate_color,
    'help_color': validate_color,
    'help_bg_color': validate_color,
    'error_color': validate_color,
    'error_bg_color': validate_color,
    # 'show_label': validate_bool,
    # 'show_help': validate_bool,
    # 'visible': validate_bool,
    # 'full_width': validate_bool
}




def layout_options(label_color=None,
                   label_bg_color=None,
                   help_color=None,
                   help_bg_color=None,
                   error_color=None,
                   error_bg_color=None,
                   show_label=True,
                   show_help=True,
                   visible=True,
                   full_width=False):

    options = pmap({k:v for k,v in locals().items() if v is not None})
    failures = {}
    for k,v in options.items():
        validator = layout_validators.get(k, _unit)
        err, success = validator(v)
        if err:
            failures[k] = err

    if failures:
        raise ValueError(failures)
    return options
