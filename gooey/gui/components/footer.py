import sys
import wx

from gooey.gui import events
from gooey.gui.lang.i18n import _
from gooey.gui.pubsub import pub
from gooey.gui.components.mouse import notifyMouseEvent


class Footer(wx.Panel):
    '''
    Footer section used on the configuration
    screen of the application
    '''

    def __init__(self, parent, buildSpec, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.buildSpec = buildSpec

        self.SetMinSize((30, 53))
        # TODO: The was set to True for the timer addition
        #       however, it leads to 'tearing' issues when resizing
        #       the GUI in windows. Disabling until I can dig into it.
        self.SetDoubleBuffered(False)
        # components
        self.cancel_button = None
        self.start_button = None
        self.progress_bar = None
        self.close_button = None
        self.stop_button = None
        self.restart_button = None
        self.edit_button = None
        self.buttons = []

        self.layouts = {}

        self._init_components()
        self._do_layout()

        for button in self.buttons:
            self.Bind(wx.EVT_BUTTON, self.dispatch_click, button)
            self.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent, button)
        self.Bind(wx.EVT_LEFT_DOWN, notifyMouseEvent)


    def updateTimeRemaining(self,*args,**kwargs):
        estimate_time_remaining = kwargs.get('estimatedRemaining')
        elapsed_time_value = kwargs.get('elapsed_time')
        if elapsed_time_value is None:
            return
        elif estimate_time_remaining is not None:
            self.time_remaining_text.SetLabel(f"{elapsed_time_value}<{estimate_time_remaining}")
            return
        else:
            self.time_remaining_text.SetLabel(f"{elapsed_time_value}")


    def updateProgressBar(self, *args, **kwargs):
        '''
         value, disable_animation=False
        :param args:
        :param kwargs:
        :return:
        '''
        value = kwargs.get('progress')
        pb = self.progress_bar
        if value is None:
            return
        if value < 0:
            pb.Pulse()
        else:
            value = min(int(value), pb.GetRange())
            if pb.GetValue() != value:
                # Windows 7 progress bar animation hack
                # http://stackoverflow.com/questions/5332616/disabling-net-progressbar-animation-when-changing-value
                if self.buildSpec['disable_progress_bar_animation'] \
                        and sys.platform.startswith("win"):
                    if pb.GetRange() == value:
                        pb.SetValue(value)
                        pb.SetValue(value - 1)
                    else:
                        pb.SetValue(value + 1)
                pb.SetValue(value)


    def showButtons(self, *buttonsToShow):
        for button in self.buttons:
            button.Show(False)
        for button in buttonsToShow:
            getattr(self, button).Show(True)
        self.Layout()


    def _init_components(self):
        self.cancel_button = self.button(_('cancel'), wx.ID_CANCEL, event_id=events.WINDOW_CANCEL)
        self.stop_button = self.button(_('stop'), wx.ID_OK, event_id=events.WINDOW_STOP)
        self.start_button = self.button(_('start'), wx.ID_OK, event_id=int(events.WINDOW_START))
        self.close_button = self.button(_("close"), wx.ID_OK, event_id=int(events.WINDOW_CLOSE))
        self.restart_button = self.button(_('restart'), wx.ID_OK, event_id=int(events.WINDOW_RESTART))
        self.edit_button = self.button(_('edit'), wx.ID_OK, event_id=int(events.WINDOW_EDIT))

        self.progress_bar = wx.Gauge(self, range=100)

        self.time_remaining_text = wx.StaticText(self)

        self.buttons = [self.cancel_button, self.start_button,
                        self.stop_button, self.close_button,
                        self.restart_button, self.edit_button]

        if self.buildSpec['disable_stop_button']:
            self.stop_button.Enable(False)


    def _do_layout(self):
        self.SetBackgroundColour(self.buildSpec['footer_bg_color'])
        self.stop_button.Hide()
        self.restart_button.Hide()

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        h_sizer.Add(self.progress_bar, 1,
                    wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)
        
        h_sizer.Add(self.time_remaining_text,0,wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)

        h_sizer.AddStretchSpacer(1)
        h_sizer.Add(self.cancel_button, 0,wx.RIGHT, 20)
        h_sizer.Add(self.start_button, 0, wx.RIGHT, 20)
        h_sizer.Add(self.stop_button, 0, wx.RIGHT, 20)

        v_sizer.AddStretchSpacer(1)
        v_sizer.Add(h_sizer, 0, wx.EXPAND)

        h_sizer.Add(self.edit_button, 0, wx.RIGHT, 10)
        h_sizer.Add(self.restart_button, 0, wx.RIGHT, 10)
        h_sizer.Add(self.close_button, 0, wx.RIGHT, 20)
        self.edit_button.Hide()
        self.restart_button.Hide()
        self.close_button.Hide()
        self.progress_bar.Hide()

        v_sizer.AddStretchSpacer(1)
        self.SetSizer(v_sizer)

    def button(self, label=None, style=None, event_id=-1):
        return wx.Button(
            parent=self,
            id=event_id,
            size=(90, -1),
            label=label,
            style=style)

    def dispatch_click(self, event):
        pub.send_message(event.GetId())

    def hide_all_buttons(self):
        for button in self.buttons:
            button.Hide()
