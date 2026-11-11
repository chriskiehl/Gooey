"""
Default colors for Gooey in light and dark mode.
"""

LIGHT_MODE_COLORS = {
    'body_bg_color': '#f0f0f0',
    'header_bg_color': '#ffffff',
    'footer_bg_color': '#f0f0f0',
    'sidebar_bg_color': '#f2f2f2',
    'terminal_panel_color': '#F0F0F0',
    'terminal_font_color': '#000000',
    'label_color': '#000000',
    'help_color': '#363636',
    'description_color': '#363636',
    'dialog_bg_color': '#ffffff',
}

DARK_MODE_COLORS = {
    'body_bg_color': '#292A31',
    'header_bg_color': '#19191D',
    'footer_bg_color': '#292A31',
    'sidebar_bg_color': '#292A31',
    'terminal_panel_color': '#3A3A44',
    'terminal_font_color': '#ffffff',
    'label_color': '#ffffff',
    'help_color': '#EDEDF0',
    'description_color': '#E1E1E3',
    'dialog_bg_color': '#292A31',
}


def is_dark_mode():
    """
    Check whether the system draws windows with a dark background.

    wx can only check the system appearance once a wx.App exists. Without
    one, wx crashes on Linux (GTK) instead of raising an error, so light
    mode is assumed until the App has been created.

    Returns
    -------
    bool
        True when a wx.App exists and its windows have a dark background.
    """
    import wx
    return wx.GetApp() is not None and wx.SystemSettings.GetAppearance().IsUsingDarkBackground()


def get_default_colors():
    """
    Get the default colors that match the system appearance.

    Returns
    -------
    dict
        The default colors, keyed by Gooey option name.
    """
    return DARK_MODE_COLORS if is_dark_mode() else LIGHT_MODE_COLORS
