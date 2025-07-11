import wx  # type: ignore
import wx.richtext  # type: ignore
import colored  # type: ignore
import re
from gooey.python_bindings import types as t


class RichTextConsole(wx.richtext.RichTextCtrl):
    """
        An advanced rich test console panel supporting some Xterm control codes.
    """

    def __init__(self, parent):
        super(wx.richtext.RichTextCtrl, self).__init__(parent, -1, "", style=wx.richtext.RE_MULTILINE | wx.richtext.RE_READONLY)
        self.regex_urls=re.compile(r'\b((?:file://|https?://|mailto:)[^][\s<>|]*)')
        self.url_colour = wx.Colour(0,0,255)
        self.esc = colored.library.Library.ESC
        self.end = colored.library.Library.END
        self.noop = lambda *args, **kwargs: None

        self.actionsMap = {
            colored.style('bold'): self.BeginBold,
            colored.style('res_bold'): self.EndBold,
            colored.style('underline'): self.BeginUnderline,
            colored.style('res_underline'): self.EndUnderline,
            colored.style('reset'): self.EndAllStyles,
        }

        # Actions for coloring text
        for index, hex in colored.library.Library.HEX_COLORS.items():
            escSeq = colored.fore(index)
            wxcolor = wx.Colour(int(hex[1:3],16), int(hex[3:5],16), int(hex[5:],16), alpha=wx.ALPHA_OPAQUE)
            # NB : we use a default parameter to force the evaluation of the binding
            self.actionsMap[escSeq] = lambda bindedColor=wxcolor: self.BeginTextColour(bindedColor)
            
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
        unprocIndex = 0
        while True:
            # Invariant : unprocIndex is the starting index of the unprocessed part of the buffer
            escPos = content.find(self.esc, unprocIndex)
            if escPos == -1:
                break
            # Invariant : found an escape sequence starting at escPos
            # NB : we flush all the characters before the escape sequence, if any
            if content[unprocIndex:escPos]:
                self.PreprocessAndWriteText(content[unprocIndex:escPos])
            endEsc = content.find(self.end, escPos)
            if endEsc == -1:
                unprocIndex = escPos + len(self.esc)
                continue
            # Invariant : end of sequence has been found
            self.actionsMap.get(content[escPos:endEsc+1], self.noop)()
            unprocIndex = endEsc + 1
        # Invariant : unprocessed end of buffer is escape-free, ready to be printed
        self.PreprocessAndWriteText(content[unprocIndex:])
        self.ShowPosition(self.GetInsertionPoint())

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
