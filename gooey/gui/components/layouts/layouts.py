import wx


def standard_layout(title, subtitle, widget):
    container = wx.BoxSizer(wx.VERTICAL)

    container.Add(title)
    container.AddSpacer(2)

    if subtitle:
        container.Add(subtitle, 1, wx.EXPAND)
        container.AddSpacer(2)
    else:
        container.AddStretchSpacer(1)

    container.Add(widget, 0, wx.EXPAND)
    return container
