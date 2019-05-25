import wx
import wx.richtext
import colored
import re

kColorList = ["#000000", "#800000", "#008000", "#808000", "#000080", "#800080", "#008080", "#c0c0c0",
    "#808080", "#ff0000", "#00ff00", "#ffff00", "#0000ff", "#ff00ff", "#00ffff", "#ffffff", "#000000",
    "#00005f", "#000087", "#0000af", "#0000d7", "#0000ff", "#005f00", "#005f5f", "#005f87", "#005faf",
    "#005fd7", "#005fff", "#008700", "#00875f", "#008787", "#0087af", "#0087d7", "#0087ff", "#00af00",
    "#00af5f", "#00af87", "#00afaf", "#00afd7", "#00afff", "#00d700", "#00d75f", "#00d787", "#00d7af",
    "#00d7d7", "#00d7ff", "#00ff00", "#00ff5f", "#00ff87", "#00ffaf", "#00ffd7", "#00ffff", "#5f0000",
    "#5f005f", "#5f0087", "#5f00af", "#5f00d7", "#5f00ff", "#5f5f00", "#5f5f5f", "#5f5f87", "#5f5faf",
    "#5f5fd7", "#5f5fff", "#5f8700", "#5f875f", "#5f8787", "#5f87af", "#5f87d7", "#5f87ff", "#5faf00",
    "#5faf5f", "#5faf87", "#5fafaf", "#5fafd7", "#5fafff", "#5fd700", "#5fd75f", "#5fd787", "#5fd7af",
    "#5fd7d7", "#5fd7ff", "#5fff00", "#5fff5f", "#5fff87", "#5fffaf", "#5fffd7", "#5fffff", "#870000",
    "#87005f", "#870087", "#8700af", "#8700d7", "#8700ff", "#875f00", "#875f5f", "#875f87", "#875faf",
    "#875fd7", "#875fff", "#878700", "#87875f", "#878787", "#8787af", "#8787d7", "#8787ff", "#87af00",
    "#87af5f", "#87af87", "#87afaf", "#87afd7", "#87afff", "#87d700", "#87d75f", "#87d787", "#87d7af",
    "#87d7d7", "#87d7ff", "#87ff00", "#87ff5f", "#87ff87", "#87ffaf", "#87ffd7", "#87ffff", "#af0000",
    "#af005f", "#af0087", "#af00af", "#af00d7", "#af00ff", "#af5f00", "#af5f5f", "#af5f87", "#af5faf",
    "#af5fd7", "#af5fff", "#af8700", "#af875f", "#af8787", "#af87af", "#af87d7", "#af87ff", "#afaf00",
    "#afaf5f", "#afaf87", "#afafaf", "#afafd7", "#afafff", "#afd700", "#afd75f", "#afd787", "#afd7af",
    "#afd7d7", "#afd7ff", "#afff00", "#afff5f", "#afff87", "#afffaf", "#afffd7", "#afffff", "#d70000",
    "#d7005f", "#d70087", "#d700af", "#d700d7", "#d700ff", "#d75f00", "#d75f5f", "#d75f87", "#d75faf",
    "#d75fd7", "#d75fff", "#d78700", "#d7875f", "#d78787", "#d787af", "#d787d7", "#d787ff", "#d7af00",
    "#d7af5f", "#d7af87", "#d7afaf", "#d7afd7", "#d7afff", "#d7d700", "#d7d75f", "#d7d787", "#d7d7af",
    "#d7d7d7", "#d7d7ff", "#d7ff00", "#d7ff5f", "#d7ff87", "#d7ffaf", "#d7ffd7", "#d7ffff", "#ff0000",
    "#ff005f", "#ff0087", "#ff00af", "#ff00d7", "#ff00ff", "#ff5f00", "#ff5f5f", "#ff5f87", "#ff5faf",
    "#ff5fd7", "#ff5fff", "#ff8700", "#ff875f", "#ff8787", "#ff87af", "#ff87d7", "#ff87ff", "#ffaf00",
    "#ffaf5f", "#ffaf87", "#ffafaf", "#ffafd7", "#ffafff", "#ffd700", "#ffd75f", "#ffd787", "#ffd7af",
    "#ffd7d7", "#ffd7ff", "#ffff00", "#ffff5f", "#ffff87", "#ffffaf", "#ffffd7", "#ffffff", "#080808",
    "#121212", "#1c1c1c", "#262626", "#303030", "#3a3a3a", "#444444", "#4e4e4e", "#585858", "#626262",
    "#6c6c6c", "#767676", "#808080", "#8a8a8a", "#949494", "#9e9e9e", "#a8a8a8", "#b2b2b2", "#bcbcbc",
    "#c6c6c6", "#d0d0d0", "#dadada", "#e4e4e4", "#eeeeee"]

class RichTextConsole(wx.richtext.RichTextCtrl):
    """
        An advanced rich test console panel supporting some Xterm control codes.
    """

    def __init__(self, parent):
        super(wx.richtext.RichTextCtrl, self).__init__(parent, -1, "", style=wx.richtext.RE_MULTILINE | wx.richtext.RE_READONLY)
        self.regex_urls=re.compile(r'\b((?:file://|https?://|mailto:)[^][\s<>|]*)')
        self.url_colour = wx.Colour(0,0,255)
        self.esc = colored.style.ESC
        self.end = colored.style.END
        self.noop = lambda *args, **kwargs: None

        self.actionsMap = {
            colored.style.BOLD: self.BeginBold,
            colored.style.RES_BOLD: self.EndBold,
            colored.style.UNDERLINED: self.BeginUnderline,
            colored.style.RES_UNDERLINED: self.EndUnderline,
            colored.style.RESET: self.EndAllStyles,
        }

        # Actions for coloring text
        for index, hex in enumerate(kColorList):
            escSeq = '{}{}{}'.format(colored.fore.ESC, index, colored.fore.END)
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
