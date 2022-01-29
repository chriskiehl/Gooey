import os

import itertools

from gooey.gui.util.quoting import quote
from gooey.python_bindings.types import EnrichedItem, FormField
from gooey.gui.constants import VALUE_PLACEHOLDER, RADIO_PLACEHOLDER
from gooey.util.functional import assoc, associnMany


def value(field: FormField):
    if field['type'] in ['Checkbox', 'BlockCheckbox']:
        return field['checked']   # type: ignore
    elif field['type'] in ['Dropdown', 'Listbox', 'Counter']:
        return field['selected']   # type: ignore
    elif field['type'] == 'RadioGroup':
        if field['selected'] is not None:  # type: ignore
            return value(field['options'][field['selected']])  # type: ignore
        else:
            return None
    else:
        return field['value'] # type: ignore


def add_placeholder(field: FormField, placeholder=VALUE_PLACEHOLDER):
    """
    TODO: Docs about placeholders
    """
    if field['type'] in ['Checkbox', 'CheckBox', 'BlockCheckbox']:
        # there's no sane placeholder we can make for this one, as
        # it's kind of a nonsensical case: a required optional flag.
        # We set it to True here, which is equally nonsensical, but
        # ultimately will allow the validation to pass. We have no
        # way of passing a placeholder without even MORE monket patching
        # of the user's parser to rewrite the action type
        return assoc(field, 'checked', True)
    elif field['type'] in ['Dropdown', 'Listbox', 'Counter']:
        return assoc(field, 'selected', placeholder)
    elif field['type'] == 'RadioGroup':
        # We arbitrarily attach a placeholder for first RadioGroup option
        # and mark it as the selected one.
        return {
            **field,
            'selected': 0,
            'options': [
                add_placeholder(field['options'][0], placeholder=RADIO_PLACEHOLDER),  # type: ignore
                *field['options'][1:]  # type: ignore
            ]
        }
    else:
        return assoc(field, 'value', placeholder)


def formatArgument(item: EnrichedItem):
    if item['type'] in ['Checkbox', 'CheckBox', 'BlockCheckbox']:
        return checkbox(item['data'], value(item['field']))
    elif item['type'] == 'MultiFileChooser':
        return multiFileChooser(item['data'], value(item['field']))
    elif item['type'] == 'Textarea':
        return textArea(item['data'], value(item['field']))
    elif item['type'] == 'CommandField':
        return textArea(item['data'], value(item['field']))
    elif item['type'] == 'Counter':
        return counter(item['data'], value(item['field']))
    elif item['type'] == 'Dropdown':
        return dropdown(item['data'], value(item['field']))
    elif item['type'] == 'Listbox':
        return listbox(item['data'], value(item['field']))
    elif item['type'] == 'RadioGroup':
        selected = item['field']['selected']  # type: ignore
        if selected is not None:
            formField = item['field']['options'][selected]  # type: ignore
            argparseDefinition = item['data']['widgets'][selected]  # type: ignore
            return formatArgument(assoc(argparseDefinition, 'field', formField))  # type: ignore
        else:
            return None
    else:
        return general(item['data'], value(item['field']))


def placeholder(item: EnrichedItem):
    pass


def checkbox(metadata, value):
    return metadata['commands'][0] if value else None


def multiFileChooser(metadata, value):
    paths = ' '.join(quote(x) for x in value.split(os.pathsep) if x)
    if metadata['commands'] and paths:
        return u'{} {}'.format(metadata['commands'][0], paths)
    return paths or None


def textArea(metadata, value):
    if metadata['commands'] and value:
        return '{} {}'.format(metadata['commands'][0], quote(value.encode('unicode_escape')))
    else:
        return quote(value.encode('unicode_escape')) if value else ''


def commandField(metadata, value):
    if metadata['commands'] and value:
        return u'{} {}'.format(metadata['commands'][0], value)
    else:
        return value or None


def counter(metatdata, value):
    '''
    Returns
      str(option_string * DropDown Value)
      e.g.
      -vvvvv
    '''
    if not str(value).isdigit():
        return None
    command = str(metatdata['commands'][0]).strip()
    return ' '.join(itertools.repeat(command, int(value)))


def dropdown(metadata, value):
    if value == 'Select Option':
        return None
    elif metadata['commands'] and value:
        return u'{} {}'.format(metadata['commands'][0], quote(value))
    else:
        return quote(value) if value else ''


def listbox(meta, value):
    if meta['commands'] and value:
        return u'{} {}'.format(meta['commands'][0], ' '.join(map(quote, value)))
    else:
        return ' '.join(map(quote, value)) if value else ''


def general(metadata, value):
    if metadata.get('commands') and value:
        if not metadata.get('nargs'):
            v = quote(value)
        else:
            v = value
        return u'{0} {1}'.format(metadata['commands'][0], v)
    else:
        if not value:
            return None
        elif not metadata.get('nargs'):
            return quote(value)
        else:
            return value

