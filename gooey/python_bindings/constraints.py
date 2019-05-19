"""
Basic constraints to ensure GooeyParser is fed all the info it needs
for various widget classes.

TODO: this should all live in the build_config stage here where it is used
within the GooeyParser directly. As is, logic is fragmented across files. Some
assertions happen in argparse_to_json, while others happen in GooeyParser.

Whenever refactoring happens, these should be removed from GooeyParser.
"""
from textwrap import dedent

def is_required(action):
    return action.required

def is_hidden(options):
    return not options.get('visible', True)

def has_validator(options):
    return bool(options.get('validator'))

def has_default(action):
    return bool(action.default)

def assert_visibility_requirements(action, options):
    if action.required and is_hidden(options) \
            and not (has_validator(options) or has_default(action)):
        raise ValueError(dedent(
            '''
            When using Gooey's hidden field functionality, you must either '
      
              (a) provide a default value, or '
              (b) provide a custom validator'
              
            Without one of those, your users will be unable to advance past 
            the configuration screen as they cannot interact with your 
            hidden field, and the default validator requires something to 
            be present for fields marked as `required`.  
            '''
        ))

def assert_listbox_constraints(widget, **kwargs):
    if widget and widget == 'Listbox':
        if not 'nargs' in kwargs or kwargs['nargs'] not in ['*', '+']:
            raise ValueError(
                'Gooey\'s Listbox widget requires that nargs be specified.\n'
                'Nargs must be set to either `*` or `+` (e.g. nargs="*")'
            )

