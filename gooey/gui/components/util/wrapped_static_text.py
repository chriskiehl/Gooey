import wx
from wx.lib.wordwrap import wordwrap



class AutoWrappedStaticText(wx.StaticText):
    """
    Copy/pasta of wx.lib.agw.infobar.AutoWrapStaticText with 3 modifications:

        1. Extends wx.StaticText rather than GenStaticText
        2. Does not set the fore/background colors to sys defaults
        3. takes an optional `target` parameter for sizing info

    The behavior of GenStaticText's background color is pretty buggy cross-
    platform. It doesn't reliably match its parent components background
    colors[0] (for instance when rendered inside of a Notebook) which leads to
    ugly 'boxing' around the text components.

    There is either a bug in WX, or or human error on my end, which causes
    EVT_SIZE events to continuously spawn from this (and AutoWrapStaticText) but
    with ever decreasing widths (in response to the SetLabel action in the
    wrap handler). The end result is a single skinny column of letters.

    The work around is to respond the EVT_SIZE event, but follow the size of the
    `target` component rather than relying on the size of the event.

    [0] more specifically, they'll match 1:1 on paper, but still ultimately
    render differently.
    """

    def __init__(self, parent, *args, **kwargs):
        self.target = kwargs.pop('target', None)
        super(AutoWrappedStaticText, self).__init__(parent, *args, **kwargs)
        self.label = kwargs.get('label')
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.parent = parent


    def OnSize(self, event):
        """
        Handles the ``wx.EVT_SIZE`` event for :class:`AutoWrapStaticText`.

        :param `event`: a :class:`wx.SizeEvent` event to be processed.
        """

        event.Skip()
        if self.target:
            self.Wrap(self.target.GetSize().width)
        else:
            self.Wrap(self.parent.GetSize()[0])

    def Wrap(self, width):
        """
        This functions wraps the controls label so that each of its lines becomes at
        most `width` pixels wide if possible (the lines are broken at words boundaries
        so it might not be the case if words are too long).

        If `width` is negative, no wrapping is done.

        :param integer `width`: the maximum available width for the text, in pixels.

        :note: Note that this `width` is not necessarily the total width of the control,
         since a few pixels for the border (depending on the controls border style) may be added.
        """

        if width < 0:
            return

        self.Freeze()

        dc = wx.ClientDC(self)
        dc.SetFont(self.GetFont())
        text = wordwrap(self.label, width, dc)
        self.SetLabel(text, wrapped=True)

        self.Thaw()

    def SetLabel(self, label, wrapped=False):
        """
        Sets the :class:`AutoWrapStaticText` label.

        All "&" characters in the label are special and indicate that the following character is
        a mnemonic for this control and can be used to activate it from the keyboard (typically
        by using ``Alt`` key in combination with it). To insert a literal ampersand character, you
        need to double it, i.e. use "&&". If this behaviour is undesirable, use :meth:`~Control.SetLabelText` instead.

        :param string `label`: the new :class:`AutoWrapStaticText` text label;
        :param bool `wrapped`: ``True`` if this method was called by the developer using :meth:`~AutoWrapStaticText.SetLabel`,
         ``False`` if it comes from the :meth:`~AutoWrapStaticText.OnSize` event handler.

        :note: Reimplemented from :class:`wx.Control`.
        """

        if not wrapped:
            self.label = label

        wx.StaticText.SetLabel(self, label)
