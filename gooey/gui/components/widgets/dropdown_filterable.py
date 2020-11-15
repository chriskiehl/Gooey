from contextlib import contextmanager

import wx
import wx.html

import gooey.gui.events as events
from gooey.gui.components.filtering.prefix_filter import PrefixSearch
from gooey.gui.components.mouse import notifyMouseEvent
from gooey.gui.components.widgets.dropdown import Dropdown
from gooey.gui.lang.i18n import _
from gooey.gui.pubsub import pub

__ALL__ = ('FilterableDropdown',)


class FilterableDropdown(Dropdown):
    """
    TODO: tests for gooey_options
    TODO: documentation
    A dropdown with auto-complete / filtering behaviors.

    This is largely a recreation of the `AutoComplete` functionality baked
    into WX itself.

    Background info:
    The Dropdown's listbox and its Autocomplete dialog are different components.
    This means that if the former is open, the latter cannot be used. Additionally,
    this leads to annoying UX quirks like the boxes having different styles and sizes.
    If we ignore the UX issues, a possible solution for still leveraging the current built-in
    AutoComplete functionality would have been to capture EVT_TEXT and conditionally
    close the dropdown while spawning the AutoComplete dialog, but due to
    (a) non-overridable behaviors and (b) lack a fine grained events, this cannot be
    done in a seamless manner.

    FAQ:
    Q: Why does it slide down rather than hover over elements like the native ComboBox?
    A: The only mecahnism for layering in WX is the wx.PopupTransientWindow. There's a long
       standing issue in wxPython which prevents ListBox/Ctrl from capturing events when
       inside of a PopupTransientWindow (see: https://tinyurl.com/y28ngh7v)

    Q: Why is visibility handled by changing its size rather than using Show/Hide?
    A: WX's Layout engine is strangely quirky when it comes to toggling visibility.
       Repeated calls to Layout() after the first show/hide cycle no longer produce
       the same results. I have no idea why. I keep checking it thinking I'm crazy, but
       alas... seems to be the case.
    """
    gooey_options = {
        'placeholder': str,
        'empty_message': str,
        'max_size': str
    }
    def __init__(self, *args, **kwargs):
        # these are declared here and created inside
        # of getWidget() because the structure of all
        # this inheritance garbage is broken.
        self.listbox = None
        self.model = None
        super(FilterableDropdown, self).__init__(*args, **kwargs)
        self.SetDoubleBuffered(True)

    def interpretState(self, model):
        """
        Updates the UI to reflect the current state of the model.
        """
        if self.widget.GetValue() != self.model.displayValue:
            self.widget.ChangeValue(model.displayValue)

        self.listbox.Clear()
        self.listbox.SetItemCount(len(self.model.suggestions))
        if len(self.model.suggestions) == 1:
            # I have no clue why this is required, but without
            # manually flicking the virtualized listbox off/on
            # it won't paint the update when there's only a single
            # item being displayed
            self.listbox.Show(False)
            self.listbox.Show(self.model.suggestionsVisible)
        if model.selectedSuggestion > -1:
            self.listbox.SetSelection(model.selectedSuggestion)
            self.widget.SetInsertionPoint(-1)
            self.widget.SetSelection(999, -1)
        else:
            self.listbox.SetSelection(-1)
        self.estimateBestSize()
        self.listbox.Show(self.model.suggestionsVisible)
        self.Layout()
        self.GetParent().Layout()

    def onComponentInitialized(self):
        self.widget.GetTextCtrl().Bind(wx.EVT_TEXT, self.onTextInput)
        self.widget.GetTextCtrl().Bind(wx.EVT_CHAR_HOOK, self.onKeyboardControls)
        self.widget.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        self.widget.GetTextCtrl().Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)
        self.listbox.Bind(wx.EVT_LISTBOX, self.onClickSuggestion)
        pub.subscribe(events.LEFT_DOWN, self.onMouseClick)
        self.widget.SetHint(self._options.get('placeholder', ''))

    def getWidget(self, parent, *args, **options):
        # self.widget = wx.ComboCtrl(parent)
        self.comboCtrl = wx.ComboCtrl(parent)
        self.comboCtrl.OnButtonClick = self.onButton
        self.foo = ListCtrlComboPopup()
        self.comboCtrl.SetPopupControl(self.foo)
        self.listbox = VirtualizedListBox(self)
        self.listbox.OnGetItem = self.OnGetItem
        # model is created here because the design of these widget
        # classes is broken.
        self.model = FilterableDropdownModel(self._meta['choices'], self._options, listeners=[self.interpretState])
        # overriding this to false removes it from tab behavior.
        # and keeps the tabbing at the top-level widget level
        self.listbox.AcceptsFocusFromKeyboard = lambda *args, **kwargs: False
        return self.comboCtrl

    def OnGetItem(self, n):
        return self.model.suggestions[n]

    def getSublayout(self, *args, **kwargs):
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self.widget, 1, wx.EXPAND)
        verticalSizer.Add(layout, 0, wx.EXPAND)
        verticalSizer.Add(self.listbox, 0, wx.EXPAND)
        self.listbox.SetMaxSize(self.model.maxSize)
        self.listbox.Hide()
        self.Layout()
        return verticalSizer

    def setOptions(self, options):
        self.model.updateChoices(options)
        if not self.model.actualValue in options:
            self.model.updateActualValue('')

    def setValue(self, value):
        self.model.updateActualValue(value)

    def onButton(self):
        if self.model.suggestionsVisible:
            self.model.hideSuggestions()
        else:
            self.model.showSuggestions()

    def onClickSuggestion(self, event):
        self.model.acceptSuggestion(self.model.suggestions[event.Selection])
        event.Skip()

    def onMouseClick(self, wxEvent):
        """
        Closes the suggestions when the user clicks anywhere
        outside of the current widget.
        """
        if wxEvent.EventObject not in (self.widget, self.widget.GetTextCtrl()):
            self.model.hideSuggestions()
            wxEvent.Skip()
        else:
            wxEvent.Skip()

    def onTextInput(self, event):
        """Processes the user's input and show relevant suggestions"""
        self.model.handleTextInput(event.GetString())

    def onKeyboardControls(self, event):
        """
        Handles any keyboard events relevant to the
        control/navigation of the suggestion box.
        All other events are passed through via `Skip()`
        and bubble up to `onTextInput` to be handled.
        """
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.model.ignoreSuggestions()
        elif event.GetKeyCode() in (wx.WXK_TAB, wx.WXK_RETURN):
            self.model.acceptSuggestion(self.model.displayValue)
            event.Skip()
        elif event.GetKeyCode() in (wx.WXK_DOWN, wx.WXK_UP):
            if not self.model.suggestionsVisible:
                self.model.generateSuggestions(self.model.displayValue)
                self.model.showSuggestions()
            else:
                if self.listbox.OnGetItem(0) != self.model.noMatch:
                    self.ignore = True
                    if event.GetKeyCode() == wx.WXK_DOWN:
                        self.model.incSelectedSuggestion()
                    else:
                        self.model.decSelectedSuggestion()
        else:
            # for some reason deleting text doesn't
            # trigger the usual evt_text event, even though
            # it IS a modification of the text... so handled here.
            if event.GetKeyCode() == wx.WXK_DELETE:
                self.model.handleTextInput('')
            event.Skip()

    def estimateBestSize(self):
        """
        Restricts the size of the dropdown based on the number
        of items within it. This is a rough estimate based on the
        current font size.
        """
        padding = 11
        rowHeight = self.listbox.GetFont().GetPixelSize()[1] + padding
        maxHeight = self.model.maxSize[1]
        self.listbox.SetMaxSize((-1, min(maxHeight, len(self.model.suggestions) * rowHeight)))
        self.listbox.SetMinSize((-1, min(maxHeight, len(self.model.suggestions) * rowHeight)))
        self.listbox.SetSize((-1, -1))



class VirtualizedListBox(wx.html.HtmlListBox):
    def __init__(self, *args, **kwargs):
        super(VirtualizedListBox, self).__init__(*args, **kwargs)
        self.SetItemCount(1)

    def OnGetItem(self, n):
        return ''




class FilterableDropdownModel(object):
    """
    The model/state for the FilterableDropdown. While this is still one
    big ball of mutation (hard to get away from in WX), it serves the purpose
    of keeping data transforms independent of presentation concerns.
    """
    gooey_options = {
        'placeholder': str,
        'empty_message': str,
        'max_size': str
    }
    def __init__(self, choices, options, listeners=[], *args, **kwargs):
        self.listeners = listeners
        self.actualValue = ''
        self.displayValue = ''
        self.dropEvent = False
        self.suggestionsVisible = False
        self.noMatch = options.get('no_matches', _('dropdown.no_matches'))
        self.choices = choices
        self.suggestions = choices
        self.selectedSuggestion = -1
        self.suggestionsVisible = False
        self.maxSize = (-1, options.get('max_size', 80))
        self.strat = PrefixSearch(choices, options.get('search_strategy', {}))

    def __str__(self):
        return str(vars(self))

    @contextmanager
    def notify(self):
        try:
            yield
        finally:
            for listener in self.listeners:
                listener(self)

    def updateChoices(self, choices):
        """Update the available choices in response
        to a dynamic update"""
        self.choices = choices
        self.strat.updateChoices(choices)

    def handleTextInput(self, value):
        if self.dropEvent:
            self.dropEvent = False
        else:
            with self.notify():
                self.actualValue = value
                self.displayValue = value
                self.selectedSuggestion = -1
                self.generateSuggestions(value)
                self.suggestionsVisible = True

    def updateActualValue(self, value):
        with self.notify():
            self.actualValue = value
            self.displayValue = value

    def acceptSuggestion(self, suggestion):
        """Accept the currently selected option as the user's input"""
        with self.notify():
            self.actualValue = suggestion
            self.displayValue = suggestion
            self.suggestionsVisible = False
            self.selectedSuggestion = -1

    def ignoreSuggestions(self):
        """
        Ignore the suggested values and replace the
        user's original input.
        """
        with self.notify():
            self.displayValue = self.actualValue
            self.suggestionsVisible = False
            self.selectedSuggestion = -1

    def generateSuggestions(self, prompt):
        suggestions = self.strat.findMatches(prompt)
        final_suggestions = suggestions if suggestions else [self.noMatch]
        self.suggestions = final_suggestions

    def incSelectedSuggestion(self):
        with self.notify():
            nextIndex = (self.selectedSuggestion + 1) % len(self.suggestions)
            suggestion = self.suggestions[nextIndex]
            self.selectedSuggestion = nextIndex
            self.displayValue = suggestion
            self.dropEvent = True

    def decSelectedSuggestion(self):
        with self.notify():
            currentIndex = max(-1, self.selectedSuggestion - 1)
            nextIndex = currentIndex % len(self.suggestions)
            nextDisplay = self.suggestions[nextIndex]
            self.displayValue = nextDisplay
            self.selectedSuggestion = nextIndex
            self.dropEvent = True

    def hideSuggestions(self):
        with self.notify():
            self.suggestionsVisible = False

    def showSuggestions(self):
        with self.notify():
            self.generateSuggestions(self.displayValue)
            self.suggestionsVisible = True

    def isShowingSuggestions(self):
        """
        Check if we're currently showing the suggestion dropdown
        by checking if we've made it's height non-zero.
        """
        return self.suggestionsVisible


class ListCtrlComboPopup(wx.ComboPopup):
    """
    This is an empty placeholder to satisfy the interface of
    the ComboCtrl which uses it. All Popup behavior is handled
    inside of `FilterableDropdown`. See its docs for additional
    details.
    """
    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.lc = None

    def Create(self, parent):
        # this ComboCtrl requires a real Wx widget be created
        # thus creating a blank static text object
        self.lc = wx.StaticText(parent)
        return True

    def GetControl(self):
        return self.lc

