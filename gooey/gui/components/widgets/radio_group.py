import wx
from gooey.gui.components.widgets.bases import BaseWidget
from gooey.gui.lang.i18n import _
from gooey.gui.util import wx_util
from gooey.gui.components.widgets import CheckBox
from gooey.util.functional import getin, findfirst, merge


class RadioGroup(BaseWidget):

    def __init__(self, parent, widgetInfo, *args, **kwargs):
        super(RadioGroup, self).__init__(parent, *args, **kwargs)
        self._parent = parent
        self.info = widgetInfo
        self._id = widgetInfo['id']
        self._options = widgetInfo['options']
        self.widgetInfo = widgetInfo
        self.error = wx.StaticText(self, label='')
        self.radioButtons = self.createRadioButtons()
        self.selected = None
        self.widgets = self.createWidgets()
        self.arrange()


        for button in self.radioButtons:
            button.Bind(wx.EVT_LEFT_DOWN, self.handleButtonClick)

        initialSelection = getin(self.info, ['options', 'initial_selection'], None)
        if initialSelection is not None:
            self.selected = self.radioButtons[initialSelection]
            self.selected.SetValue(True)
        self.handleImplicitCheck()

        self.applyStyleRules()


    def getValue(self):
        for button, widget in zip(self.radioButtons, self.widgets):
            if button.GetValue():  # is Checked
                return merge(widget.getValue(), {'id': self._id})
        else:
            # just return the first widget's value even though it's
            # not active so that the expected interface is satisfied
            return self.widgets[0].getValue()

    def setErrorString(self, message):
        for button, widget in zip(self.radioButtons, self.widgets):
            if button.GetValue():  # is Checked
                widget.setErrorString(message)
        self.Layout()

    def showErrorString(self, b):
        for button, widget in zip(self.radioButtons, self.widgets):
            if button.GetValue():  # is Checked
                widget.showErrorString(b)


    def arrange(self, *args, **kwargs):
        title = getin(self.widgetInfo, ['options', 'title'], _('choose_one'))
        if getin(self.widgetInfo, ['options', 'show_border'], False):
            boxDetails = wx.StaticBox(self, -1, title)
            boxSizer = wx.StaticBoxSizer(boxDetails, wx.VERTICAL)
        else:
            title = wx_util.h1(self, title)
            title.SetForegroundColour(self._options['label_color'])
            boxSizer = wx.BoxSizer(wx.VERTICAL)
            boxSizer.AddSpacer(10)
            boxSizer.Add(title, 0)

        for btn, widget in zip(self.radioButtons, self.widgets):
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(btn,0, wx.RIGHT, 4)
            sizer.Add(widget, 1, wx.EXPAND)
            boxSizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(boxSizer)


    def handleButtonClick(self, event):
        currentSelection = self.selected
        nextSelection = event.EventObject

        if not self.isSameRadioButton(currentSelection, nextSelection):
            self.selected = nextSelection
            self.selected.SetValue(True)
        else:
            # user clicked on an already enabled radio button.
            # if it is not in the required section, allow it to be deselected
            if not self.widgetInfo['required']:
                self.selected.SetValue(False)
                self.selected = None

        self.applyStyleRules()
        self.handleImplicitCheck()


    def isSameRadioButton(self, radioButton1, radioButton2):
        return (getattr(radioButton1, 'Id', 'r1-not-found') ==
                getattr(radioButton2, 'Id', 'r2-not-found'))


    def applyStyleRules(self):
        """
        Conditionally disabled/enables form fields based on the current
        section in the radio group
        """
        # for reasons I have been completely unable to figure out
        # or understand, IFF you've interacted with one of the radio Buttons's
        # child components, then the act of disabling that component will
        # reset the state of the radioButtons thus causing it to forget
        # what should be selected. So, that is why we're collected the initial
        # state of all the buttons and resetting each button's state as we go.
        # it's wonky as hell
        states = [x.GetValue() for x in self.radioButtons]
        for button, selected, widget in zip(self.radioButtons, states, self.widgets):
            if isinstance(widget, CheckBox):
                widget.hideInput()
            if not selected: # not checked
                widget.Disable()
            else:
                widget.Enable()
            button.SetValue(selected)


    def handleImplicitCheck(self):
        """
        Checkboxes are hidden when inside of a RadioGroup as a selection of
        the Radio button is an implicit selection of the Checkbox. As such, we have
        to manually "check" any checkbox as needed.
        """
        for button, widget in zip(self.radioButtons, self.widgets):
            if isinstance(widget, CheckBox):
                if button.GetValue(): # checked
                    widget.setValue(True)
                else:
                    widget.setValue(False)


    def createRadioButtons(self):
        # button groups in wx are statefully determined via a style flag
        # on the first button (what???). All button instances are part of the
        # same group until a new button is created with the style flag RG_GROUP
        # https://wxpython.org/Phoenix/docs/html/wx.RadioButton.html
        # (What???)
        firstButton = wx.RadioButton(self, style=wx.RB_GROUP)
        firstButton.SetValue(False)
        buttons = [firstButton]

        for _ in getin(self.widgetInfo, ['data','widgets'], [])[1:]:
            buttons.append(wx.RadioButton(self))
        return buttons

    def createWidgets(self):
        """
        Instantiate the Gooey Widgets that are used within the RadioGroup
        """
        from gooey.gui.components import widgets
        widgets = [getattr(widgets, item['type'])(self, item)
                   for item in getin(self.widgetInfo, ['data', 'widgets'], [])]
        # widgets should be disabled unless
        # explicitly selected
        for widget in widgets:
            widget.Disable()
        return widgets
