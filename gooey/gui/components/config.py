import wx
from wx.lib.scrolledpanel import ScrolledPanel

from gooey.gui.util import wx_util
from gooey.util.functional import getin, flatmap, merge, compact, indexunique
from gooey.gui.components.widgets.radio_group import RadioGroup


class ConfigPage(ScrolledPanel):
    def __init__(self, parent, rawWidgets, *args, **kwargs):
        super(ConfigPage, self).__init__(parent, *args, **kwargs)
        self.SetupScrolling(scroll_x=False, scrollToTop=False)
        self.rawWidgets = rawWidgets
        self.reifiedWidgets = []
        self.layoutComponent()
        self.widgetsMap = indexunique(lambda x: x._id, self.reifiedWidgets)
        ## TODO: need to rethink what uniquely identifies an argument.
        ## Out-of-band IDs, while simple, make talking to the client program difficult
        ## unless they're agreed upon before hand. Commands, as used here, have the problem
        ## of (a) not being nearly granular enough (for instance,  `-v` could represent totally different
        ## things given context/parser position), and (b) cannot identify positional args.


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
            self.makeGroup(self, sizer, item, 0, wx.EXPAND)
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
            boxDetails = wx.StaticBox(parent, -1, group['name'] or '')
            boxSizer = wx.StaticBoxSizer(boxDetails, wx.VERTICAL)
        else:
            boxSizer = wx.BoxSizer(wx.VERTICAL)
            boxSizer.AddSpacer(10)
            if group['name']:
                boxSizer.Add(wx_util.h1(parent, group['name'] or ''), 0, wx.TOP | wx.BOTTOM | wx.LEFT, 8)

        group_description = getin(group, ['description'])
        if group_description:
            description = wx.StaticText(parent, label=group_description)
            boxSizer.Add(description, 0,  wx.EXPAND | wx.LEFT, 10)

        # apply an underline when a grouping border is not specified
        if not getin(group, ['options', 'show_border'], False) and group['name']:
            boxSizer.Add(wx_util.horizontal_rule(parent), 0, wx.EXPAND | wx.LEFT, 10)

        ui_groups = self.chunkWidgets(group)

        for uigroup in ui_groups:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            for item in uigroup:
                widget = self.reifyWidget(parent, item)
                # !Mutate the reifiedWidgets instance variable in place
                self.reifiedWidgets.append(widget)
                sizer.Add(widget, 1, wx.ALL, 5)
            boxSizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 5)

        # apply the same layout rules recursively for subgroups
        hs = wx.BoxSizer(wx.HORIZONTAL)
        for e, subgroup in enumerate(group['groups']):
            self.makeGroup(parent, hs, subgroup, 1, wx.ALL | wx.EXPAND, 5)
            if e % getin(group, ['options', 'columns'], 2) \
                    or e == len(group['groups']):
                boxSizer.Add(hs, *args)
                hs = wx.BoxSizer(wx.HORIZONTAL)

        thissizer.Add(boxSizer, *args)


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




