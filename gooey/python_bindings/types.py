from typing import Optional, Tuple, List, Union, Mapping, Any, TypeVar, Generic, Dict

from dataclasses import dataclass
from typing_extensions import TypedDict


class MenuHtmlDialog(TypedDict):
    type: str
    menuTitle: str
    caption: Optional[str]
    html: str

class MenuLink(TypedDict):
    type: str
    menuTitle: str
    url: str


class MenuMessageDialog(TypedDict):
    type: str
    menuTitle: str
    message: str
    caption: Optional[str]

class MenuAboutDialog(TypedDict):
    type: str
    menuTitle: str
    name: Optional[str]
    description: Optional[str]
    version: Optional[str]
    copyright: Optional[str]
    license: Optional[str]
    website: Optional[str]
    developer: Optional[str]


MenuItem = Union[
    MenuLink,
    MenuMessageDialog,
    MenuAboutDialog,
    MenuHtmlDialog
]



class TimingOptions(TypedDict):
    show_time_remaining: bool
    hide_time_remaining_on_complete: bool


class GooeyParams(TypedDict):
    # when running with a custom target, there is no need to inject
    # --ignore-gooey into the CLI args
    show_preview_warning: bool
    suppress_gooey_flag: bool
    advanced: bool
    language: str
    target: Optional[str]
    program_name: Optional[str]
    program_description: Optional[str]
    sidebar_title: str
    default_size: Tuple[int, int]
    auto_start: bool
    show_advanced: bool
    run_validators: bool
    encoding: str
    show_stop_warning: bool
    show_success_modal: bool
    show_failure_modal: bool
    force_stop_is_error: bool
    poll_external_updates: bool  # BEING DEPRECATED
    return_to_config: bool
    show_restart_button: bool
    requires_shell: bool
    menu: List[MenuItem]
    clear_before_run: bool
    fullscreen: bool
    # Legacy/Backward compatibility interop
    use_legacy_titles: bool
    required_cols: int
    optional_cols: int
    manual_start: bool
    monospace_display: bool

    image_dir: str
    language_dir: str
    progress_regex: Optional[str]
    progress_expr: Optional[str]
    hide_progress_msg: bool
    timing_options: TimingOptions
    disable_progress_bar_animation: bool
    disable_stop_button: bool
    shutdown_signal: int
    use_events: List[str]

    # Layouts
    navigation: str
    show_sidebar: bool
    tabbed_groups: bool
    group_by_type: bool

    # styles
    body_bg_color: str
    header_bg_color: str
    header_height: int
    header_show_title: bool
    header_show_subtitle: bool
    header_image_center: bool
    footer_bg_color: str
    sidebar_bg_color: str

    # font family, weight, and size are determined at runtime
    terminal_panel_color: str
    terminal_font_color: str
    terminal_font_family: Optional[str]
    terminal_font_weight: Optional[int]
    terminal_font_size: Optional[int]
    richtext_controls: bool
    error_color: str

    use_cmd_args: bool
    dump_build_config: bool
    load_build_config: Optional[str]

# TODO:
# use the syntax here rather than inheritance, as the latter is a type error
# https://jdkandersson.com/2020/01/27/python-typeddict-arbitrary-key-names-with-totality/
# class BuildSpecification(GooeyParams):
#     target: str
#     widgets: str


class BasicField(TypedDict):
    id: str
    type: str
    # required: bool
    # positional: bool
    error: Optional[str]
    enabled: bool
    visible: bool

class Dropdown(BasicField):
    selected: int
    choices: List[str]

class Chooser(BasicField):
    btn_label: str
    value: str


class MultiFileChooser(Chooser):
    pass

class FileChooser(Chooser):
    pass

class FileSaver(Chooser):
    pass

class DirChooser(Chooser):
    pass

class MultiDirChooser(Chooser):
    pass

class DateChooser(Chooser):
    pass

class TimeChooser(Chooser):
    pass

class ColourChooser(Chooser):
    pass

class Command(BasicField):
    value: str
    placeholder: str

class Counter(BasicField):
    selected: int
    choices: List[str]

class DropdownFilterable(BasicField):
    value: str
    choices: List[str]

class Listbox(BasicField):
    selected: List[str]
    choices: List[str]

class IntegerField(BasicField):
    value: str
    min: int
    max: int

class DecimalField(BasicField):
    value: float
    min: float
    max: float

class Slider(BasicField):
    value: float
    min: float
    max: float

class Textarea(BasicField):
    value: float
    height: int

class TextField(BasicField):
    value: str
    placeholder: str


class PasswordField(TextField):
    pass


class Checkbox(BasicField):
    checked: bool


class RadioGroup(BasicField):
    selected: Optional[int]
    options: List['FormField']


FormField = Union[
    Textarea,
    Slider,
    Command,
    Counter,
    Checkbox,
    TextField,
    Dropdown,
    Chooser,
    RadioGroup,
    DropdownFilterable,
    Listbox,
    IntegerField
]




class FieldValue(TypedDict):
    """
    The current value of a widget in the UI.
    TODO: Why are things like cmd and cli type tracked IN the
    UI and returned as part of the getValue() call?
    What the hell, young me?
    """
    id: str
    cmd: Optional[str]
    rawValue: str
    placeholder: str
    positional: bool
    required: bool
    enabled: bool
    visible: bool
    test: bool
    error: Optional[str]
    clitype: str
    meta: Any


class PublicGooeyState(TypedDict):
    """
    A minimal representation of Gooey's current UI state
    """
    active_form: List[FormField]


class Group(TypedDict):
    name: str
    items: List['Item']
    groups: List['Group']
    description: str
    options: Dict[Any, Any]


class Item(TypedDict):
    id: str
    type: str
    cli_type: str
    group_name: str
    required: bool
    options: Dict[Any, Any]
    data: 'ItemData'


class EnrichedItem(Item):
    """
    An argparse item paired with its associated Gooey form
    field and current state.
    """
    field: FormField


ItemData = Union['StandardData', 'RadioData']

class StandardData(TypedDict):
    display_name: str
    help: str
    required: bool
    nargs: str
    commands: List[str]
    choices: List[str]
    default: Union[str, List[str]]
    dest: str

class RadioData(TypedDict):
    commands: List[List[str]]
    widgets: List[Item]


class TopLevelParser(TypedDict):
    command: str
    name: str
    help: Optional[str]
    description: str
    contents: List[Group]

A = TypeVar('A')


## TODO: dynamic types

@dataclass(frozen=True, eq=True)
class CommandDetails:
    target: str
    subcommand: str
    positionals: List[FieldValue]
    optionals: List[FieldValue]

@dataclass(frozen=True, eq=True)
class CommandPieces:
    target: str
    subcommand: str
    positionals: List[str]
    optionals: List[str]
    ignoreFlag: str

@dataclass(frozen=True, eq=True)
class Success(Generic[A]):
    value: A

    def map(self, f):
        return Success(f(self.value))
    def flatmap(self, f):
        return f(self.value)
    def onSuccess(self, f):
        f(self.value)
        return self
    def onError(self, f):
        return self
    def isSuccess(self):
        return True
    def getOrThrow(self):
        return self.value

@dataclass(frozen=True, eq=True)
class Failure:
    error: Exception

    def map(self, f):
        return Failure(self.error)
    def flatmap(self, f):
        return Failure(self.error)
    def onSuccess(self, f):
        return self
    def onError(self, f):
        f(self.error)
        return self
    def isSuccess(self):
        return False
    def getOrThrow(self):
        raise self.error

Try = Union[Success[A], Failure]



ValidationResponse = Mapping[str, str]


class InvalidChoiceException(ValueError):
    pass
