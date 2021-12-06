from typing import Optional

from typing_extensions import TypedDict
import wx

from gooey.gui import events
from gui.lang.i18n import _
from gooey.python_bindings.types import GooeyParams
from gooey.util.functional import associn, assoc, associnMany


class TimingEvent(TypedDict):
    elapsed_time: Optional[str]
    estimatedRemaining: Optional[str]


class ProgressEvent(TypedDict):
    progress: Optional[int]


def initial_state(params: GooeyParams):
    buttons = [
        ('cancel', events.WINDOW_CANCEL, wx.ID_CANCEL),
        ('start', events.WINDOW_START, wx.ID_OK),
        ('stop', events.WINDOW_STOP, wx.ID_OK),
        ('edit', events.WINDOW_EDIT,wx.ID_OK),
        ('restart', events.WINDOW_RESTART, wx.ID_OK),
        ('close', events.WINDOW_CLOSE, wx.ID_OK),
    ]
    return {
        'screen': 'CONSOLE',
        'title': 'running_title',
        'subtitle': 'running_msg',
        'images': params['images'],
        'buttons': [{
            'id': event_id,
            'style': style,
            'label_id': label,
            'show': False}
            for label, event_id, style in buttons],
        'progress': {
            'show': True, # params['disable_progress_bar_animation'],
            'range': 100,
            'value': 0 if params['progress_regex'] else -1
        },
        'timing': {
            'visible': True, #params['timing_options']['show_time_remaining'],
            'elapsed_time': '00:00', # None,
            'estimatedRemaining': '00:00', # None,
        },
        'activeSelection': 1
     }

def header_props(state, params):
    return {
            'background_color': params['header_bg_color'],
            'title': params['program_name'],
            'subtitle': params['program_description'],
            'height': params['header_height'],
            'image_uri': ims['images']['configIcon'],
            'image_size': (six.MAXSIZE, params['header_height'] - 10)
    }


def form_page(state):
    return {
        **state,
        'buttons': [{**btn, 'show': btn['label_id'] in ('start', 'cancel')}
                    for btn in state['buttons']]
    }


def start(state, event, params: GooeyParams):
    return {
        'screen': 'CONSOLE',
        'title': event['title'],
        'subtitle': event['subtitle'],
        'buttons': [{**btn, 'visible': btn['id'] == 'stop'}
                    for btn in state['buttons']],
        'progress': {
            'visible': params['disable_progress_bar_animation'],
            'range': 100,
            'value': 0 if params['progress_regex'] else -1
        },
        'timing': {
            'visible': params['timing_options']['show_time_remaining'],
            'elapsed_time': None,
            'estimatedRemaining': None
        }
     }



def updateProgress(state, event: ProgressEvent):
    return associn(state, ['progress', 'value'], event['progress'] or 0)


def updateTime(state, event):
    return associnMany(
        state,
        ('timing.elapsed_time', event['elapsed_time']),
        ('timing.estimatedRemaining', event['estimatedRemaining'])
    )






def update_time(state, event: TimingEvent):
    return {
        **state,
        'timer': {
            **state['timer'],
            'elapsed_time': event['elapsed_time'],
            'estimatedRemaining': event['estimatedRemaining']
        }
    }




def update_progress(state, event: ProgressEvent):
    return associn(state, ['progress', 'value'], event['value'])




def present_time(timer):
    estimate_time_remaining = timer['estimatedRemaining']
    elapsed_time_value = timer['elapsed_time']
    if elapsed_time_value is None:
        return ''
    elif estimate_time_remaining is not None:
        return f'{elapsed_time_value}<{estimate_time_remaining}'
    else:
        return f'{elapsed_time_value}'

