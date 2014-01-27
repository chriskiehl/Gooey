'''
Created on Dec 22, 2013

@author: Chris
'''

import wx 
import sys
import traceback
from multiprocessing.dummy import Pool, Process
from model.i18n import I18N

YES = 5103
NO 	= 5104

class Controller(object):
	'''
	Main controller for the gui. 
	
	All controlls are delegated to this central control point. 
	
	Args: 
		base_frame	 = Reference to the Basewindow
		head_panel	 = reference to the BaseWindow's Head Panel 	  
		body_panel 	 = reference to the BaseWindow's Body Panel 	  
		footer_panel = reference to the BaseWindow's Footer Panel
		model				 = configuration model 	  
	'''
	
	def __init__(self, base_frame, head_panel, body_panel, 
							footer_panel, model):
		self._base = base_frame
		self._head = head_panel
		self._body = body_panel 
		self._foot = footer_panel
		
		self._model = model
		
		self._payload_runner = Process(target=self.RunClientCode).start
		
		self._translator = I18N()
	
	def OnCancelButton(self, event):
		msg = self._translator['sure_you_want_to_exit']
		dlg = wx.MessageDialog(None, msg, 
													self._translator['close_program'], wx.YES_NO)
		result = dlg.ShowModal()
		print result
		if result == YES:
			dlg.Destroy()
			self._base.Destroy()
			sys.exit()
		dlg.Destroy()
			
	def OnStartButton(self, event):
		cmd_line_args = self._body.GetOptions()
		if not self._model.IsValidArgString(cmd_line_args):
			error_msg = self._model.GetErrorMsg(cmd_line_args)
			self.ShowArgumentErrorDlg(error_msg) 
			return 
		self._model.AddToArgv(cmd_line_args)
		self._base.NextPage()
		self._payload_runner()

	def OnCancelRunButton(self, event):
		pass
		
		
	def RunClientCode(self):
		pool = Pool(1)
		try:
			pool.apply(self._base._payload)
			self.ShowGoodFinishedDialog()
		except:
			self.ShowBadFinishedDialog(traceback.format_exc())
			
	def ShowDialog(self, title, content, style):
		a = wx.MessageDialog(None, content, title, style)	
		a.ShowModal()
		a.Destroy()

	def ShowGoodFinishedDialog(self):
		self.ShowDialog(self._translator["execution_finished"], 
									self._translator['success_message'],
									wx.ICON_INFORMATION)
		
	def ShowBadFinishedDialog(self, error_msg):
		msg = self._translator['uh_oh'].format(error_msg)
		self.ShowDialog(self._translator['error_title'], msg, wx.ICON_ERROR)
		
		
		

		

