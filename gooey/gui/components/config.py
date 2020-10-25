import wx
from wx.lib.scrolledpanel import ScrolledPanel

from gooey.gui.components.util.wrapped_static_text import AutoWrappedStaticText
from gooey.gui.util import wx_util
from gooey.util.functional import getin, flatmap, compact, indexunique
from gooey.gui.lang.i18n import _
from gooey.gui.components.mouse import notifyMouseEvent


class ConfigPage(ScrolledPanel):
    def __init__(self, parent, rawWidgets, buildSpec,  *args, **kwargs):
        super(ConfigPage, self).__init__(parent, *args, **kwargs)
        self.SetupScrolling(scroll_x=False, scrollToTop=False)
        self.rawWidgets = rawWidgets
        self.buildSpec = buildSpec
        self.reifiedWidgets = []
        self.layoutComponent()
        self.Layout()
        self.widgetsMap = indexunique(lambda x: x._id, self.reifiedWidgets)
        self.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        ## TODO: need to rethink what uniquely identifies an argument.
        ## Out-of-band IDs, while simple, make talking to the client program difficult
        ## unless they're agreed upon before hand. Commands, as used here, have the problem
        ## of (a) not being nearly granular enough (for instance,  `-v` could represent totally different
        ## things given context/parser position), and (b) cannot identify positional args.

    def getName(self, group):
        """
        retrieve the group name from the group object while accounting for
        legacy fixed-name manual translation requirements.
        """
        name = group['name']
        return (_(name)
                if name in {'optional_args_msg', 'required_args_msg'}
                else name)


    def firstCommandIfPresent(self, widget):
        commands = widget._meta['commands']
        return commands[0] if commands else ''

    def getPositionalArgs(self):
        return [widget.getValue()['cmd'] for widget in self.reifiedWidgets
                if widget.info['cli_type'] == 'positional']

    def getOptionalArgs(self):
        return [widget.getValue()['cmd'] for widget in self.reifiedWidgets
                if widget.info['cli_type'] != 'positional']


    def isValid(self):
        states = [widget.getValue() for widget in self.reifiedWidgets]
        return not any(compact([state['error'] for state in states]))


    def seedUI(self, seeds):
        radioWidgets = self.indexInternalRadioGroupWidgets()
        for id, values in seeds.items():
            if id in self.widgetsMap:
                self.widgetsMap[id].setOptions(values)
            if id in radioWidgets:
                radioWidgets[id].setOptions(values)

    def indexInternalRadioGroupWidgets(self):
        groups = filter(lambda x: x.info['type'] == 'RadioGroup', self.reifiedWidgets)
        widgets = flatmap(lambda group: group.widgets, groups)
        return indexunique(lambda x: x._id, widgets)


    def displayErrors(self):
        states = [widget.getValue() for widget in self.reifiedWidgets]
        errors = [state for state in states if state['error']]
        for error in errors:
            widget = self.widgetsMap[error['id']]
            widget.setErrorString(error['error'])
            widget.showErrorString(True)
            while widget.GetParent():
                widget.Layout()
                widget = widget.GetParent()

    def resetErrors(self):
        for widget in self.reifiedWidgets:
            widget.setErrorString('')
            widget.showErrorString(False)

    def hideErrors(self):
        for widget in self.reifiedWidgets:
            widget.hideErrorString()


    def layoutComponent(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        for item in self.rawWidgets['contents']:
            self.makeGroup(self, sizer, item, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)

    def makeGroup(self, parent, thissizer, group, *args):
        '''
        Messily builds the (potentially) nested and grouped layout

        Note! Mutates `self.reifiedWidgets` in place with the widgets as they're
        instantiated! I cannot figure out how to split out the creation of the
        widgets from their styling without WxPython violently exploding

        TODO: sort out the WX quirks and clean this up.
        '''

        # determine the type of border , if any, the main sizer will use
        if getin(group, ['options', 'show_border'], False):
            boxDetails = wx.StaticBox(parent, -1, self.getName(group) or '')
            boxSizer = wx.StaticBoxSizer(boxDetails, wx.VERTICAL)
        else:
            boxSizer = wx.BoxSizer(wx.VERTICAL)
            boxSizer.AddSpacer(10)
            if group['name']:
                groupName = wx_util.h1(parent, self.getName(group) or '')
                groupName.SetForegroundColour(getin(group, ['options', 'label_color']))
                groupName.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
                boxSizer.Add(groupName, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 8)

        group_description = getin(group, ['description'])
        if group_description:
            description = AutoWrappedStaticText(parent, label=group_description, target=boxSizer)
            description.SetForegroundColour(getin(group, ['options', 'description_color']))
            description.SetMinSize((0, -1))
            description.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
            boxSizer.Add(description, 1,  wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        # apply an underline when a grouping border is not specified
        # unless the user specifically requests not to show it
        if not getin(group, ['options', 'show_border'], False) and group['name'] \
                and getin(group, ['options', 'show_underline'], True):
            boxSizer.Add(wx_util.horizontal_rule(parent), 0, wx.EXPAND | wx.LEFT, 10)

        ui_groups = self.chunkWidgets(group)

        for uigroup in ui_groups:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            for item in uigroup:
                widget = self.reifyWidget(parent, item)
                if not getin(item, ['options', 'visible'], True):
                    widget.Hide()
                # !Mutate the reifiedWidgets instance variable in place
                self.reifiedWidgets.append(widget)
                sizer.Add(widget, 1, wx.ALL | wx.EXPAND, 5)
            boxSizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 5)

        # apply the same layout rules recursively for subgroups
        hs = wx.BoxSizer(wx.HORIZONTAL)
        for e, subgroup in enumerate(group['groups']):
            self.makeGroup(parent, hs, subgroup, 1, wx.EXPAND)
            if len(group['groups']) != e:
                hs.AddSpacer(5)

            # self.makeGroup(parent, hs, subgroup, 1, wx.ALL | wx.EXPAND, 5)
            itemsPerColumn = getin(group, ['options', 'columns'], 2)
            if e % itemsPerColumn or (e + 1) == len(group['groups']):
                boxSizer.Add(hs, *args)
                hs = wx.BoxSizer(wx.HORIZONTAL)


        group_top_margin = getin(group, ['options', 'margin_top'], 1)

        marginSizer = wx.BoxSizer(wx.VERTICAL)
        marginSizer.Add(boxSizer, 1, wx.EXPAND | wx.TOP, group_top_margin)

        thissizer.Add(marginSizer, *args)


    def chunkWidgets(self, group):
        ''' chunk the widgets up into groups based on their sizing hints '''
        ui_groups = []
        subgroup = []
        for index, item in enumerate(group['items']):
            if getin(item, ['options', 'full_width'], False):
                ui_groups.append(subgroup)
                ui_groups.append([item])
                subgroup = []
            else:
                subgroup.append(item)
            if len(subgroup) == getin(group, ['options', 'columns'], 2) \
                    or item == group['items'][-1]:
                ui_groups.append(subgroup)
                subgroup = []
        return ui_groups


    def reifyWidget(self, parent, item):
        ''' Convert a JSON description of a widget into a WxObject '''
        from gooey.gui.components import widgets
        widgetClass = getattr(widgets, item['type'])
        return widgetClass(parent, item)



class TabbedConfigPage(ConfigPage):
    """
    Splits top-level groups across tabs
    """


    def layoutComponent(self):
        # self.rawWidgets['contents'] = self.rawWidgets['contents'][1:2]
        self.notebook = wx.Notebook(self, style=wx.BK_DEFAULT)

        panels = [wx.Panel(self.notebook) for _ in self.rawWidgets['contents']]
        sizers = [wx.BoxSizer(wx.VERTICAL) for _ in panels]

        for group, panel, sizer in zip(self.rawWidgets['contents'], panels, sizers):
            self.makeGroup(panel, sizer, group, 0, wx.EXPAND)
            panel.SetSizer(sizer)
            panel.Layout()
            self.notebook.AddPage(panel, group['name'])
            self.notebook.Layout()


        _sizer = wx.BoxSizer(wx.VERTICAL)
        _sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(_sizer)
        self.Layout()




