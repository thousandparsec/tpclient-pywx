"""\
This module contains the winDownloadManager class, which shows downloading media.
"""
# Python Imports
import os
import os.path
from types import *
import wx
import time
import pprint

from tp.netlib.objects import parameters
from tp.netlib import GenericRS
from tp.netlib import objects
from requirements import graphicsdir
from windows.winBase import winReportXRC

from tp.client import objectutils

from windows.xrc.DownloadProgressPanel import DownloadProgressPanelBase
class DownloadProgressPanel(DownloadProgressPanelBase):
	def __init__(self, application, parent, manager):
		DownloadProgressPanelBase.__init__(self, parent)
		self.application = application
		self.manager = manager
		self.progress = []
		self.averages = []
		self.done = False
		self.Cancel.Bind(wx.EVT_BUTTON, self.OnCancel)

	def SetFile(self, name):
		self.file = name
		self.FileName.SetLabel(name)

	def GetFile(self):
		return self.file

	def OnCancel(self, evt):
		if self.done:
			self.manager.RemoveFile(self.file)
		else:
			self.application.media.StopFile(self.file)

	def OnProgress(self, evt):
		self.Show()

		self.Layout()
		self.Update()

		#print "winPicture.MediaDownloadProgress", evt.file

		self.progress.append((time.time(), evt.progress))
		# Trim off the oldest samples
		while len(self.progress) > 200:
			self.progress.pop(0)

		if len(self.progress) < 2:
			return

		average = []
		time1, progress1 = self.progress[0]
		for time2, progress2 in self.progress[1:]:
			average.append((progress2-progress1)/(time2-time1))
			time1, progress1 = time2, progress2

		# Calculate an average
		average = sum(average)/len(average)

		self.Progress.SetRange(evt.size)
		self.Progress.SetValue(evt.progress)

		if average < 10e3:
			self.Speed.SetLabel("%.2f kb/s" % (average/1e3))
		elif average < 1e6:
			self.Speed.SetLabel("%.0f kb/s" % (average/1e3))
		else:
			self.Speed.SetLabel("%.2f mb/s" % (average/1e6))

		self.averages.append(average)

		aaverage = (self.progress[-1][1]-self.progress[0][1])/(self.progress[-1][0]-self.progress[0][0])
		if aaverage == 0:
			eta = 0	
		else:
			eta = (evt.size - evt.progress)/aaverage
		if eta > 60:
			eta = (int(eta)//60, eta-int(eta)//60*60)
			self.ETA.SetLabel("%im %is" % eta)
		else:
			self.ETA.SetLabel("%is" % eta)

		self.Layout()
		self.Update()
	
	def OnFinished(self):
		self.Progress.SetValue(self.Progress.GetRange())
		self.Cancel.SetLabel("Hide")
		self.ETA.SetLabel("Done")
		self.Speed.SetLabel("0 kb/s")
		self.done = True

from windows.xrc.winDownloadManager import winDownloadManagerBase
class winDownloadManager(winReportXRC, winDownloadManagerBase):
	title = _("Downloads")

	def __init__(self, application, parent):
		winDownloadManagerBase.__init__(self, parent)
		winReportXRC.__init__(self, application, parent)
	
		self.parent = parent
		self.application = application
		self.Bind(wx.EVT_SHOW, self.OnShow)
		self.Bind(wx.EVT_ACTIVATE, self.OnShow)
		self.application.gui.Binder(self.application.MediaClass.MediaDownloadProgressEvent, self.OnMediaDownloadProgress)
		self.application.gui.Binder(self.application.MediaClass.MediaDownloadDoneEvent,	self.OnMediaDownloadDone)
		self.application.gui.Binder(self.application.MediaClass.MediaDownloadAbortEvent, self.OnMediaDownloadAborted)
		self.files = []

	def OnShow(self, evt):
		downloadingfiles = self.application.media.getDownloading()
		
		for downloadingfile in downloadingfiles:
			if downloadingfile in self.files:
			        continue
				
			self.files.append(downloadingfile)
			panel = DownloadProgressPanel(self.application, self.MainPanel, self)
			panel.SetFile(downloadingfile)
			self.MainPanel.GetSizer().SetRows(self.MainPanel.GetSizer().GetRows()+1)
			self.MainPanel.GetSizer().AddGrowableRow(self.MainPanel.GetSizer().GetRows()-1)
			self.MainPanel.GetSizer().Add(panel, 1, wx.EXPAND|wx.GROW|wx.ALL)
		

	def OnMediaDownloadProgress(self, evt):
		if not evt.file in self.files:
			self.files.append(evt.file)
			panel = DownloadProgressPanel(self.application, self.MainPanel, self)
			panel.SetFile(evt.file)
			self.MainPanel.GetSizer().SetRows(self.MainPanel.GetSizer().GetRows()+1)
			self.MainPanel.GetSizer().AddGrowableRow(self.MainPanel.GetSizer().GetRows()-1)
			self.MainPanel.GetSizer().Add(panel, 1, wx.EXPAND|wx.GROW|wx.ALL)
		
		panelnum = self.files.index(evt.file)
		panel = self.MainPanel.GetSizer().GetItem(panelnum).GetWindow()
		
		panel.OnProgress(evt)
		self.SetSize(self.MainPanel.GetBestSize())
		self.Layout()
		
	def OnMediaDownloadDone(self, evt):
		for myfile in self.files:
			if not evt.file in myfile:
				continue
			
			index = self.files.index(myfile)
			panel = self.MainPanel.GetSizer().GetItem(index).GetWindow()
			panel.OnFinished()
			#self.files.remove(file)
			#self.MainPanel.GetSizer().Remove(index)
			break
			
		self.SetSize(self.MainPanel.GetBestSize())
		self.Layout()
	
	def OnMediaDownloadAborted(self, evt):
		self.RemoveFile(evt.file)
	
	def RemoveFile(self, filename):
		for file in self.files:
			if not filename in file:
				continue
			
			index = self.files.index(file)
			panel = self.MainPanel.GetSizer().GetItem(index).GetWindow()
			panel.OnFinished()
			self.files.remove(file)
			self.MainPanel.GetSizer().Remove(index)
			break
			
		self.SetSize(self.MainPanel.GetBestSize())
		self.Layout()
			
