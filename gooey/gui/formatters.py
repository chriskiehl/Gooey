import os

import itertools

from gooey.gui.util.quoting import quote
from python_bindings.types import Item


def formatArgument(item: Item, value):
    if item['type'] in ['CheckBox', 'BlockCheckbox']:
        return checkbox(item['data'], value)
    elif item['type'] == 'MultiFileChooser':
        return multiFileChooser(item['data'], value)
    elif item['type'] == 'Textarea':
        return textArea(item['data'], value)
    elif item['type'] == 'CommandField':
        return textArea(item['data'], value)
    elif item['type'] == 'Counter':
        return counter(item['data'], value)
    elif item['type'] == 'Dropdown':
        return dropdown(item['data'], value)
    elif item['type'] == 'Listbox':
        return listbox(item['data'], value)
    else:
        return general(item['data'], value)



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

