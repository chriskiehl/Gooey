'''
Created on Jan 1, 2014

@author: Chris

'''

import wx
from argparse import ArgumentParser
from abc import ABCMeta, abstractmethod


class BuildException(RuntimeError):
	pass 


class AbstractComponent(object):
	'''
	Template pattern-y abstract class for the components. 
	Children must all implement the BuildWidget and getValue 
	methods. 
	'''
	__metaclass__ = ABCMeta
	
	def __init__(self):
		self._widget = None
	
	def Build(self, parent):
		self._widget = self.BuildWidget(parent, self._action)
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		sizer.Add(self.CreateDestNameWidget(parent, self._action))
		sizer.AddSpacer(2)
				
		if self.HasHelpMsg(self._action):
			sizer.Add(self.CreateHelpMsgWidget(parent, self._action))
			sizer.AddSpacer(2)

		if self.HasNargs(self._action):
			sizer.Add(self.AddNargsMsg(parent, self._action))
			
		sizer.Add(self._widget, 0, wx.EXPAND)
		return sizer
		
	def HasHelpMsg(self, action):
		return action.help is not None
	
	def HasNargs(self, action):
		return action.nargs == '+'
	
	def CreateHelpMsgWidget(self, parent, action):
		text = wx.StaticText(parent, label=action.help)
		self.MakeDarkGrey(text)
		return text
	
	def AddNargsMsg(self, parent, action):
		msg = 'Note: at least 1 or more arguments are required'
		return wx.StaticText(parent, label=msg)
	
	def CreateDestNameWidget(self, parent, action):
		text = wx.StaticText(parent, label=str(action.dest).title())
		self.MakeBold(text)
		return text
	
	def AssertInitialization(self, widget, clsname):
		print self._widget
		if not self._widget:
			raise BuildException('%s was not correctly initialized' % clsname)
		
	def MakeBold(self, statictext):
		pointsize = statictext.GetFont().GetPointSize()
		statictext.SetFont(wx.Font(pointsize, wx.FONTFAMILY_DEFAULT,
				wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_BOLD, False))
		
	def MakeDarkGrey(self, statictext):
		darkgray = (54,54,54)
		statictext.SetForegroundColour(darkgray)
		
	
	@abstractmethod
	def BuildWidget(self, parent, action):
		''' 
		Must construct the main widget type for the Action 
		'''
		pass
	
	@abstractmethod
	def GetValue(self):
		'''
		Returns the state of the given widget
		'''
		pass



class Positional(AbstractComponent):
	def __init__(self, action):
		self._action = action
		self._widget = None
		self.contents = None
	
	def BuildWidget(self, parent, action):
		return wx.TextCtrl(parent)
	
	def GetValue(self):
		self.AssertInitialization(self._widget, 'Positional')
		return self._widget.GetValue()

	
class Choice(AbstractComponent):
	def __init__(self, action):
		self._action = action
		self._widget = None
		self.contents = None 
		
	def GetValue(self):
		self.AssertInitialization() 
		return self._widget.GetValue()
	
	def BuildWidget(self, parent, action):
		return wx.ComboBox(
							parent=parent,
							id=-1,
							value='Select Option',
							choices=action.choices, 
							style=wx.CB_DROPDOWN
							) 
	

class Optional(AbstractComponent):
	def __init__(self, action):
		pass



	



		
if __name__ == '__main__':
	parser = ArgumentParser(description='Example Argparse Program')
	parser.add_argument("filename", help="filename")
	action = parser._actions[1]
	positional = Positional(action)
	
	a = getattr
	
		
		
		
		