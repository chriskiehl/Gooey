import webbrowser
from functools import partial

import wx

from gooey.gui import three_to_four


class MenuBar(wx.MenuBar):
    """
    Wx.MenuBar handles converting the users list of Menu Groups into
    concrete wx.Menu instances.
    """

    def __init__(self, buildSpec, *args, **kwargs):
        super(MenuBar,self).__init__(*args, **kwargs)
        self.buildSpec = buildSpec
        self.makeMenuItems(buildSpec.get('menu', []))


    def makeMenuItems(self, menuGroups):
        """
        Assign the menu groups list to wx.Menu instances
        and bind the appropriate handlers.
        """
        for menuGroup in menuGroups:
            menu = wx.Menu()
            for item in menuGroup.get('items'):
                option = menu.Append(wx.NewId(), item.get('menuTitle', ''))
                self.Bind(wx.EVT_MENU, self.handleMenuAction(item), option)
            self.Append(menu, '&' + menuGroup.get('name'))


    def handleMenuAction(self, item):
        """
        Dispatch based on the value of the type field.
        """
        handlers = {
            'Link': self.openBrowser,
            'AboutDialog': self.spawnAboutDialog,
            'MessageDialog': self.spawnMessageDialog
        }
        f = handlers[item['type']]
        return partial(f, item)


    def openBrowser(self, item, *args, **kwargs):
        """
        Open the supplied URL in the user's default browser.
        """
        webbrowser.open(item.get('url'))


    def spawnMessageDialog(self, item, *args, **kwargs):
        """
        Show a simple message dialog with the user's message and caption.
        """
        wx.MessageDialog(self, item.get('message', ''),
                               caption=item.get('caption', '')).ShowModal()


    def spawnAboutDialog(self, item, *args, **kwargs):
        """
        Fill the wx.AboutBox with any relevant info the user provided
        and launch the dialog
        """
        aboutOptions = {
            'name': 'SetName',
            'version': 'SetVersion',
            'description': 'SetDescription',
            'copyright': 'SetCopyright',
            'website': 'SetWebSite',
            'developer': 'AddDeveloper',
            'license': 'SetLicense'
        }
        about = three_to_four.AboutDialog()
        for field, method in aboutOptions.items():
            if field in item:
                getattr(about, method)(item[field])

        three_to_four.AboutBox(about)