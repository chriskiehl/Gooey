import wx
import wx.richtext
import re

from gooey.gui.util.ansi import AnsiParser

class RichTextConsole(wx.richtext.RichTextCtrl):
    """
        An advanced rich test console panel supporting some Xterm control codes.
    """

    def __init__(self, parent):
        super(wx.richtext.RichTextCtrl, self).__init__(parent, -1, "", style=wx.richtext.RE_MULTILINE | wx.richtext.RE_READONLY)
        self.regex_urls=re.compile(r'\b((?:file://|https?://|mailto:)[^][\s<>|]*)')
        self.url_colour = wx.Colour(0,0,255)
        self.ansi = AnsiParser()

        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)


    def PreprocessAndWriteText(self, content):
        """Write text into console, while capturing URLs and making 
        them blue, underlined, and clickable.
        """
        textStream=iter(re.split(self.regex_urls, content))
        # The odd elements in textStream are plaintext;
        # the even elements are URLs.
        for plaintext in textStream:
            url=next(textStream, None)
            self.WriteText(plaintext)
            if url:    
                self.BeginTextColour(self.url_colour)
                self.BeginUnderline()
                self.BeginURL(url)
                self.WriteText(url)
                self.EndURL()
                self.EndUnderline()
                self.EndTextColour()
            
    def AppendText(self, content):
        """
        wx method overridden to capture the terminal control character and translate them into wx styles.
        Complexity : o(len(content))
        """
        self.SetInsertionPointEnd()
        for text, style in self.ansi.feed(content):
            textAttr = self.ToTextAttr(style)
            if textAttr is None:
                self.PreprocessAndWriteText(text)
            else:
                self.BeginStyle(textAttr)
                self.PreprocessAndWriteText(text)
                self.EndStyle()
        self.ShowPosition(self.GetInsertionPoint())

    def ToTextAttr(self, style):
        """Convert a parsed style into wx text attributes, or None
        when the text keeps the default look of the console.
        """
        if not any(style):
            return None
        textAttr = wx.richtext.RichTextAttr()
        if style.bold:
            textAttr.SetFontWeight(wx.FONTWEIGHT_BOLD)
        if style.italic:
            textAttr.SetFontStyle(wx.FONTSTYLE_ITALIC)
        if style.underline:
            textAttr.SetFontUnderlined(True)
        if style.foreground is not None:
            textAttr.SetTextColour(wx.Colour(*style.foreground))
        if style.background is not None:
            textAttr.SetBackgroundColour(wx.Colour(*style.background))
        return textAttr

    def Clear(self):
        """
        wx method overridden so the styles of one run do not carry over into the next.
        """
        self.ansi.reset()
        super(RichTextConsole, self).Clear()

    def onMouseWheel(self, event):
        if event.GetModifiers()==2 and event.GetWheelAxis()==wx.MOUSE_WHEEL_VERTICAL:
            if event.GetWheelRotation() >= event.GetWheelDelta():
                r=1.1
            elif event.GetWheelRotation() <= -event.GetWheelDelta():
                r=1.0/1.1
            else:
                return
            self.SetFontScale(self.GetFontScale() * r, True)
        else:
            event.Skip()
