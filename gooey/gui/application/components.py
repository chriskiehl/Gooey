"""
Houses all the supporting rewx components for
the main application window.
"""
import wx  # type: ignore
from typing_extensions import TypedDict

from gooey.gui.components.config import ConfigPage, TabbedConfigPage
from gooey.gui.components.console import Console
from gooey.gui.components.mouse import notifyMouseEvent
from gooey.gui.components.sidebar import Sidebar
from gooey.gui.components.tabbar import Tabbar
from gooey.gui.lang.i18n import _
from gooey.gui.pubsub import pub
from gooey.gui.state import present_time
from gooey.gui.three_to_four import Constants
from gooey.python_bindings import constants
from rewx import components as c  # type: ignore
from rewx import wsx, mount, update  # type: ignore
from rewx.core import Component, Ref  # type: ignore
from rewx.widgets import set_basic_props  # type: ignore


def attach_notifier(parent):
    """
    Recursively attaches the mouseEvent notifier
    to all elements in the tree
    """
    parent.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
    for child in parent.Children:
        attach_notifier(child)


class HeaderProps(TypedDict):
    background_color: str
    title: str
    show_title: bool
    subtitle: str
    show_subtitle: bool


class RHeader(Component):
    def __init__(self, props):
        super().__init__(props)
        self.parentRef = Ref()

    def component_did_mount(self):
        attach_notifier(self.parentRef.instance)

    def render(self):
        if 'running' not in self.props['image_uri']:
            imageProps = {
                'uri': self.props['image_uri'],
                'size': self.props['image_size'],
                'flag': wx.RIGHT,
                'border': 10}
        else:
            imageProps = {
                'size': self.props['image_size'],
                'flag': wx.RIGHT,
                'border': 10}
        return wsx(
            [c.Block, {'orient': wx.HORIZONTAL,
                       'ref': self.parentRef,
                       'min_size': (120, self.props['height']),
                       'background_color': self.props['background_color']},
             [c.Block, {'orient': wx.VERTICAL,
                        'flag': wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                        'proportion': 1,
                        'border': 10},
              [TitleText, {'label': self.props['title'],
                           'show': self.props['show_title'],
                           'wx_name': 'header_title'}],
              [c.StaticText, {'label': self.props['subtitle'],
                              'show': self.props['show_subtitle'],
                              'wx_name': 'header_subtitle'}]],
             [c.StaticBitmap, imageProps]]
        )



class RFooter(Component):
    def __init__(self, props):
        super().__init__(props)
        self.ref = Ref()

    def component_did_mount(self):
        """
        We have to manually wire up LEFT_DOWN handlers
        for every component due to wx limitations.
        See: mouse.py docs for background.
        """
        block: wx.BoxSizer = self.ref.instance
        attach_notifier(block)

    def handle(self, btn):
        def inner(*args, **kwargs):
            pub.send_message(btn['id'])
        return inner

    def render(self):
        return wsx(
            [c.Block, {'orient': wx.VERTICAL,
                       'min_size': (30, 53),
                       'background_color': self.props['bg_color']},
             [c.Block, {'orient': wx.VERTICAL, 'proportion': 1}],
             [c.Block, {'orient': wx.HORIZONTAL,
                        'border': 20,
                        'flag': wx.EXPAND | wx.LEFT | wx.RIGHT,
                        'ref': self.ref},
              [c.Gauge, {'range': 100,
                         'proportion': 1,
                         'value': self.props['progress']['value'],
                         'show': self.props['progress']['show']}],
              [c.StaticText, {'label': present_time(self.props['timing']),
                              'flag': wx.LEFT,
                              'wx_name': 'timing',
                              'show': self.props['timing']['show'],
                              'border': 20}],
              [c.Block, {'orient': wx.HORIZONTAL, 'proportion': 1}],
              *[[c.Button, {**btn,
                            'label': _(btn['label_id']),
                            'min_size': (90, 23),
                            'flag': wx.LEFT,
                            'border': 10,
                            'on_click': self.handle(btn)
                            }]
                for btn in self.props['buttons']]],
             [c.Block, {'orient': wx.VERTICAL, 'proportion': 1}]]
        )


class RNavbar(Component):
    def __init__(self, props):
        super().__init__(props)

    # if self.buildSpec['navigation'] == constants.TABBED:
    #     navigation = Tabbar(self, self.buildSpec, self.configs)
    # else:
    #     navigation = Sidebar(self, self.buildSpec, self.configs)
    #     if self.buildSpec['navigation'] == constants.HIDDEN:
    #         navigation.Hide()
    def render(self):
        return wsx(

        )

def VerticalSpacer(props):
    return wsx([c.Block, {'orient': wx.VERTICAL, 'min_size': (-1, props['height'])}])

def SidebarControls(props):
    return wsx(
        [c.Block, {'orient': wx.VERTICAL,
                   'min_size': (180, 0),
                   'size': (180, 0),
                   'show': props.get('show', True),
                   'flag': wx.EXPAND,
                   'proportion': 0,
                   'background_color': props['bg_color']},
         [c.Block, {'orient': wx.VERTICAL,
                    'min_size': (180, 0),
                    'size': (180, 0),
                    'flag': wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
                    'border': 10,
                    'proportion': 1,
                    'background_color': props['bg_color']},
          [VerticalSpacer, {'height': 15}],
          [TitleText, {'label': props['label']}],
          [VerticalSpacer, {'height': 5}],
          [c.ListBox, {'choices': props['options'],
                       'value': props['activeSelection'],
                       'proportion': 1,
                       'on_change': props['on_change'],
                       'flag': wx.EXPAND}],
          [VerticalSpacer, {'height': 10}]]]
    )


def ProgressSpinner(props):
    return wsx(
        [c.Block, {'flag': wx.EXPAND, 'show': props['show']},
         [c.Gauge, {'flag': wx.EXPAND,
                    'value': -1,
                    'size': (-1, 4)}],
         [c.StaticLine, {'style': wx.LI_HORIZONTAL,
                         'flag': wx.EXPAND}]]
    )


def ErrorWarning(props):
    return wsx(
        [c.Block, {'orient': wx.HORIZONTAL,
                   'background_color': '#fdeded',
                   'style': wx.SIMPLE_BORDER,
                   'flag': wx.EXPAND | wx.ALL,
                   'proportion': 0,
                   'border': 5,
                   'min_size': (-1, 45),
                   'show': props.get('show', True)},
         [c.StaticBitmap, {'size': (24, 24),
                           'flag': wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL,
                           'border': 6,
                           'uri': props['uri']}],
         [c.StaticText, {'label': 'Whoops! You have some errors which must be corrected',
                         'flag': wx.ALIGN_CENTER_VERTICAL}]]
    )

def RSidebar(props):
    return wsx(
        [c.Block, {'orient': wx.HORIZONTAL,
                   'show': props.get('show', True),
                   'flag': props['flag'],
                   'proportion': props['proportion'],
                   'ref': props['ref']},
         [SidebarControls, {**props, 'show': props['show_sidebar']}],
         [c.StaticLine, {'style': wx.LI_VERTICAL,
                         'flag': wx.EXPAND,
                         'min_size': (1, -1)}],
         *[[TabbedConfigPage if props['tabbed_groups'] else ConfigPage,
            {'flag': wx.EXPAND,
             'proportion': 3,
             'config': config,
             'show': i == props['activeSelection']}]
           for i, config in enumerate(props['config'].values())]
         ]
    )


def RTabbedLayout(props):
    return wsx(
        [c.Notebook, {'flag': wx.EXPAND | wx.ALL,
                      'show': props.get('show', True),
                      'proportion': 1,
                      'on_change': props['on_change'],
                      'ref': props['ref']},
         *[[c.NotebookItem,
            {'title': props['options'][i], 'selected': props['activeSelection'] == i},
            [TabbedConfigPage if props['tabbed_groups'] else ConfigPage,
             {'flag': wx.EXPAND,
              'proportion': 3,
              'config': config,
              'show': i == props['activeSelection']}]]
           for i, config in enumerate(props['config'].values())]]
    )



def layout_choose():
    def buildNavigation(self):
        """
        Chooses the appropriate layout navigation component based on user prefs
        """
        if self.buildSpec['navigation'] == constants.TABBED:
            navigation = Tabbar(self, self.buildSpec, self.configs)
        else:
            navigation = Sidebar(self, self.buildSpec, self.configs)
            if self.buildSpec['navigation'] == constants.HIDDEN:
                navigation.Hide()
        return navigation


    def buildConfigPanels(self, parent):
        page_class = TabbedConfigPage if self.buildSpec['tabbed_groups'] else ConfigPage

        return [page_class(parent, widgets, self.buildSpec)
                for widgets in self.buildSpec['widgets'].values()]















class TitleText(Component):
    def __init__(self, props):
        super().__init__(props)
        self.ref = Ref()

    def component_did_mount(self):
        text: wx.StaticText = self.ref.instance
        font_size = text.GetFont().GetPointSize()
        text.SetFont(wx.Font(
            int(font_size * 1.2),
            wx.FONTFAMILY_DEFAULT,
            Constants.WX_FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
            False
        ))

    def render(self):
        return wsx([c.StaticText, {**self.props, 'label': self.props['label'], 'ref': self.ref}])


##
## REWX definitions:
##

@mount.register(ConfigPage)  # type: ignore
def config(element, parent):
    return update(element, ConfigPage(parent, element['props']['config'], {'contents': []}))

@update.register(ConfigPage)  # type: ignore
def config(element, instance: ConfigPage):
    set_basic_props(instance, element['props'])
    return instance

@mount.register(TabbedConfigPage)  # type: ignore
def tabbedconfig(element, parent):
    return update(element, TabbedConfigPage(parent, element['props']['config'], {'contents': []}))

@update.register(TabbedConfigPage)  # type: ignore
def tabbedconfig(element, instance: TabbedConfigPage):
    set_basic_props(instance, element['props'])
    return instance

@mount.register(Console)  # type: ignore
def console(element, parent):
    return update(element, Console(parent, element['props']))

@update.register(Console)  # type: ignore
def console(element, instance: Console):
    set_basic_props(instance, element['props'])
    if 'show' in element['props']:
        instance.Show(element['props']['show'])
    return instance

