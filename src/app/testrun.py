'''
Created on Dec 8, 2013

@author: Chris
'''

import wx 
import Queue
from dialogs.display_main import MainWindow


if __name__ == '__main__':
	queue = Queue.Queue()
	# stdoutput = sys.stdout
	# out = TestObj(queue)
	# sys.stdout = out

	app = wx.App(False)  
	frame = MainWindow(queue)
	frame.Show(True)     # Show the frame.
	app.MainLoop()