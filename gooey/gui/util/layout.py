import wx

def get_layout_direction(lang):
    lang_info = wx.Locale.FindLanguageInfo(lang)
    if lang_info is not None:
        layout_direction = lang_info.LayoutDirection
        return layout_direction
