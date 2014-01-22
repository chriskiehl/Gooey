'''
Created on Dec 22, 2013

@author: Chris
'''

class Controller(object):
	'''
	Main controller for the gui. 
	
	All controlls are delegated to this central control point. 
	It's kind of a bi-directional observer sort of thing, thus 
	weirdly initialized with references to the BaseWindows panels, 
	and then 'registered' with the panels . 
	
	
	
	Args: 
		base			 = Reference to the Basewindow
		head_panel = reference to the BaseWindow's Head Panel 	  
		body_panel = reference to the BaseWindow's Body Panel 	  
		footer_panel = reference to the BaseWindow's Footer Panel 	  
	'''
	
	def __init__(self, base, head_panel, body_panel, footer_panel):
		self._base = base
		self._head = head_panel
		self._body = body_panel 
		self._foot = footer_panel
	
	def OnConfigCancel(self, event):
		print 'OnCongigCancel pressed!'
	
	def OnConfigNext(self, event):
		cmd_line_args = self._body.GetOptions()
		
		
	def OnMainCancel(self, event):
		print 'OnMaingCancel pressed!'
	def OnMainNext(self, event):
		print 'OnCongigNext pressed!'
	
		
		
