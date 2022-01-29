import json
from base64 import b64encode
from typing import Optional, List, Dict, Any, Union, Callable

from typing_extensions import TypedDict
import wx

from gooey.gui import events
from gooey.gui.lang.i18n import _
from gooey.python_bindings.types import GooeyParams, Item, Group, TopLevelParser, EnrichedItem, \
    FieldValue
from gooey.util.functional import associn, assoc, associnMany, compact
from gooey.gui.formatters import formatArgument
from gooey.python_bindings.types import FormField
from gooey.gui.constants import VALUE_PLACEHOLDER
from gooey.gui.formatters import add_placeholder
from gooey.python_bindings.types import CommandPieces, PublicGooeyState


class TimingEvent(TypedDict):
    elapsed_time: Optional[str]
    estimatedRemaining: Optional[str]

class ProgressEvent(TypedDict):
    progress: Optional[int]

class ButtonState(TypedDict):
    id: str
    style: str
    label_id: str
    show: bool
    enabled: bool

class ProgressState(TypedDict):
    show: bool
    range: int
    value: int

class TimingState(TypedDict):
    show: bool
    elapsedTime: Optional[str]
    estimated_remaining: Optional[str]

class GooeyState(GooeyParams):
    fetchingUpdate: bool
    screen: str
    title: str
    subtitle: str
    images: Dict[str, str]
    image: str
    buttons: List[ButtonState]
    progress: ProgressState
    timing: TimingState
    subcommands: List[str]
    activeSelection: int
    show_error_alert: bool

class FullGooeyState(GooeyState):
    forms: Dict[str, List[FormField]]
    widgets: Dict[str, Dict[str, Any]]





def extract_items(groups: List[Group]) -> List[Item]:
    if not groups:
        return []
    group = groups[0]
    return group['items'] \
           + extract_items(groups[1:]) \
           + extract_items(group['groups'])


def widgets(descriptor: TopLevelParser) -> List[Item]:
    return extract_items(descriptor['contents'])


def enrichValue(formState: List[FormField], items: List[Item]) -> List[EnrichedItem]:
    formIndex = {k['id']:k for k in formState}
    return [EnrichedItem(field=formIndex[item['id']], **item) for item in items]  # type: ignore


def positional(items: List[Union[Item, EnrichedItem]]):
    return [item for item in items if item['cli_type'] == 'positional']


def optional(items: List[Union[Item, EnrichedItem]]):
    return [item for item in items if item['cli_type'] != 'positional']


def cli_pieces(state: FullGooeyState, formatter=formatArgument) -> CommandPieces:
    parserName = state['subcommands'][state['activeSelection']]
    parserSpec = state['widgets'][parserName]
    formState = state['forms'][parserName]
    subcommand = parserSpec['command'] if parserSpec['command'] != '::gooey/default' else ''
    items = enrichValue(formState, widgets(parserSpec))
    positional_args = [formatter(item) for item in positional(items)]  # type: ignore
    optional_args = [formatter(item) for item in optional(items)]      # type: ignore
    ignoreFlag = '' if state['suppress_gooey_flag'] else '--ignore-gooey'
    return CommandPieces(
        target=state['target'],
        subcommand=subcommand,
        positionals=compact(positional_args),
        optionals=compact(optional_args),
        ignoreFlag=ignoreFlag
    )


def activeFormState(state: FullGooeyState):
    subcommand = state['subcommands'][state['activeSelection']]
    return state['forms'][subcommand]


def buildInvocationCmd(state: FullGooeyState):
    pieces = cli_pieces(state)
    return u' '.join(compact([
        pieces.target,
        pieces.subcommand,
        *pieces.optionals,
        pieces.ignoreFlag,
        '--' if pieces.positionals else '',
        *pieces.positionals]))


def buildFormValidationCmd(state: FullGooeyState):
    pieces = cli_pieces(state, formatter=cmdOrPlaceholderOrNone)
    serializedForm = json.dumps({'active_form': activeFormState(state)})
    b64ecoded = b64encode(serializedForm.encode('utf-8'))
    return ' '.join(compact([
        pieces.target,
        pieces.subcommand,
        *pieces.optionals,
        '--gooey-validate-form',
        '--gooey-state ' + b64ecoded.decode('utf-8'),
        '--' if pieces.positionals else '',
        *pieces.positionals]))


def buildOnCompleteCmd(state: FullGooeyState, was_success: bool):
    pieces = cli_pieces(state)
    serializedForm = json.dumps({'active_form': activeFormState(state)})
    b64ecoded = b64encode(serializedForm.encode('utf-8'))
    return u' '.join(compact([
        pieces.target,
        pieces.subcommand,
        *pieces.optionals,
        '--gooey-state ' + b64ecoded.decode('utf-8'),
        '--gooey-run-is-success' if was_success else '--gooey-run-is-failure',
        '--' if pieces.positionals else '',
        *pieces.positionals]))


def buildOnSuccessCmd(state: FullGooeyState):
    return buildOnCompleteCmd(state, True)

def buildOnErrorCmd(state: FullGooeyState):
    return buildOnCompleteCmd(state, False)


def cmdOrPlaceholderOrNone(item: EnrichedItem) -> Optional[str]:
    # Argparse has a fail-fast-and-exit behavior for any missing
    # values. This poses a problem for dynamic validation, as we
    # want to collect _all_ errors to be more useful to the user.
    # As such, if there is no value currently available, we pass
    # through a stock placeholder values which allows GooeyParser
    # to handle it being missing without Argparse exploding due to
    # it actually being missing.
    if item['cli_type'] == 'positional':
        return formatArgument(item) or VALUE_PLACEHOLDER
    elif item['cli_type'] != 'positional' and item['required']:
        # same rationale applies here. We supply the argument
        # along with a fixed placeholder (when relevant i.e. `store`
        # actions)
        return formatArgument(item) or formatArgument(assoc(item, 'field', add_placeholder(item['field'])))
    else:
        # Optional values are, well, optional. So, like usual, we send
        # them if present or drop them if not.
        return formatArgument(item)




def combine(state: GooeyState, params: GooeyParams, formState: List[FormField]) -> FullGooeyState:
    """
    I'm leaving the refactor of the form elements to another day.
    For now, we'll just merge in the state of the form fields as tracked
    in the UI into the main state blob as needed.
    """
    subcommand = list(params['widgets'].keys())[state['activeSelection']]
    return FullGooeyState(**{
        **state,
        **params,
        'forms': {subcommand: formState}
    })


def enable_buttons(state, to_enable: List[str]):
    updated = [{**btn, 'enabled': btn['label_id'] in to_enable}
               for btn in state['buttons']]
    return assoc(state, 'buttons', updated)



def activeCommand(state, params: GooeyParams):
    """
    Retrieve the active sub-parser command as determined by the
    current selection.
    """
    return list(params['widgets'].keys())[state['activeSelection']]


def mergeExternalState(state: FullGooeyState, extern: PublicGooeyState) -> FullGooeyState:
    # TODO: insane amounts of helpful validation
    subcommand = state['subcommands'][state['activeSelection']]
    formItems: List[FormField] = state['forms'][subcommand]
    hostForm: List[FormField] = extern['active_form']
    return associn(state, ['forms', subcommand], hostForm)


def show_alert(state: FullGooeyState):
    return assoc(state, 'show_error_alert', True)

def has_errors(state: FullGooeyState):
    """
    Searches through the form elements (including down into
    RadioGroup's internal options to find the presence of
    any errors.
    """
    return any([item['error'] or any(x['error'] for x in item.get('options', []))
                for items in state['forms'].values()
                for item in items])


def initial_state(params: GooeyParams) -> GooeyState:
    buttons = [
        ('cancel', events.WINDOW_CANCEL, wx.ID_CANCEL),
        ('start', events.WINDOW_START, wx.ID_OK),
        ('stop', events.WINDOW_STOP, wx.ID_OK),
        ('edit', events.WINDOW_EDIT,wx.ID_OK),
        ('restart', events.WINDOW_RESTART, wx.ID_OK),
        ('close', events.WINDOW_CLOSE, wx.ID_OK),
    ]
    # helping out the type system
    params: Dict[str, Any] = params
    return GooeyState(
        **params,
        fetchingUpdate=False,
        screen='FORM',
        title=params['program_name'],
        subtitle=params['program_description'],
        image=params['images']['configIcon'],
        buttons=[ButtonState(
            id=event_id,
            style=style,
            label_id=label,
            show=label in ('cancel', 'start'),
            enabled=True)
            for label, event_id, style in buttons],
        progress=ProgressState(
            show=False,
            range=100,
            value=0 if params['progress_regex'] else -1
        ),
        timing=TimingState(
            show=False,
            elapsed_time=None,
            estimatedRemaining=None,
        ),
        show_error_alert=False,
        subcommands=list(params['widgets'].keys()),
        activeSelection=0
    )

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


def consoleScreen(_: Callable[[str], str], state: GooeyState):
    return {
        **state,
        'screen': 'CONSOLE',
        'title': _("running_title"),
        'subtitle': _('running_msg'),
        'image': state['images']['runningIcon'],
        'buttons': [{**btn,
                     'show': btn['label_id'] == 'stop',
                     'enabled': True}
                    for btn in state['buttons']],
        'progress': {
            'show': not state['disable_progress_bar_animation'],
            'range': 100,
            'value': 0 if state['progress_regex'] else -1
        },
        'timing': {
            'show': state['timing_options']['show_time_remaining'],
            'elapsed_time': None,
            'estimatedRemaining': None
        },
        'show_error_alert': False
     }


def editScreen(_: Callable[[str], str], state: FullGooeyState):
    use_buttons = ('cancel', 'start')
    return associnMany(
        state,
        ('screen', 'FORM'),
        ('buttons', [{**btn,
                      'show': btn['label_id'] in use_buttons,
                      'enabled': True}
                     for btn in state['buttons']]),
        ('image', state['images']['configIcon']),
        ('title', state['program_name']),
        ('subtitle', state['program_description']))


def beginUpdate(state: GooeyState):
    return {
        **enable_buttons(state, ['cancel']),
        'fetchingUpdate': True
    }

def finishUpdate(state: GooeyState):
    return {
        **enable_buttons(state, ['cancel', 'start']),
        'fetchingUpdate': False
    }


def finalScreen(_: Callable[[str], str], state: GooeyState) -> GooeyState:
    use_buttons = ('edit', 'restart', 'close')
    return associnMany(
        state,
        ('screen', 'CONSOLE'),
        ('buttons', [{**btn,
                      'show': btn['label_id'] in use_buttons,
                      'enabled': True}
                     for btn in state['buttons']]),
        ('image', state['images']['successIcon']),
        ('title', _('finished_title')),
        ('subtitle', _('finished_msg')),
        ('progress.show', False),
        ('timing.show', not state['timing_options']['hide_time_remaining_on_complete']))


def successScreen(_: Callable[[str], str], state: GooeyState) -> GooeyState:
    return associnMany(
        finalScreen(_, state),
        ('image', state['images']['successIcon']),
        ('title', _('finished_title')),
        ('subtitle', _('finished_msg')))


def errorScreen(_: Callable[[str], str], state: GooeyState) -> GooeyState:
    return associnMany(
        finalScreen(_, state),
        ('image', state['images']['errorIcon']),
        ('title', _('finished_title')),
        ('subtitle', _('finished_error')))


def interruptedScreen(_: Callable[[str], str], state: GooeyState):
    next_state = errorScreen(_, state) if state['force_stop_is_error'] else successScreen(_, state)
    return assoc(next_state, 'subtitle', _('finished_forced_quit'))


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


def present_time(timer):
    estimate_time_remaining = timer['estimatedRemaining']
    elapsed_time_value = timer['elapsed_time']
    if elapsed_time_value is None:
        return ''
    elif estimate_time_remaining is not None:
        return f'{elapsed_time_value}<{estimate_time_remaining}'
    else:
        return f'{elapsed_time_value}'
