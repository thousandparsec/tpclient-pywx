"""\
This module contains the Information window. The Information window
displays all objects information.
"""

# Python Imports
import os
import os.path
from types import *

import pprint

# wxPython imports
import wx
import wx.lib.foldpanelbar as fpb

try:
	from extra.GIFAnimationCtrl import GIFAnimationCtrl
except ImportError:
	from wx.animate import GIFAnimationCtrl


from tp.netlib.objects.Structures import ListStructure
from tp.netlib.objects import parameters
from tp.netlib import GenericRS
from tp.netlib import objects

from windows.xrc.panelInformation import panelInformationBase
class panelInformation(panelInformationBase):
	title = _("Information")

	def __init__(self, application, parent):
		panelInformationBase.__init__(self, parent)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.application = application
		self.current = -1
		self.DetailsSizer = self.DetailsPanel.GetSizer()
		self.DetailsPanel.SetWindowStyle(wx.HSCROLL | wx.VSCROLL)
		self.ArgumentsPanel = wx.Panel(self.DetailsPanel, -1)
		self.FoldPanelBar = FoldPanel(self.ArgumentsPanel, self.application)
		bestsize = self.FoldPanelBar.GetPanelsLength(True, True)
		self.DetailsPanel.SetVirtualSize((bestsize[1]/2, bestsize[2]))
		self.application.gui.Binder(self.application.gui.SelectObjectEvent, self.OnSelectObject)
		self.application.gui.Binder(self.application.MediaClass.MediaUpdateEvent,			self.OnMediaUpdate)
		self.application.gui.Binder(self.application.MediaClass.MediaDownloadDoneEvent,		self.OnMediaDownloadDone)
		self.Bind(fpb.EVT_CAPTIONBAR, self.OnSize)

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()
		info.MinSize(self.GetBestSize())
		info.BestSize((self.GetBestSize()[0]*2,self.GetBestSize()[1]))
		info.Left()
		info.Layer(2)
		return info

	def OnMediaUpdate(self, evt):
		if (self.current == -1):
			return
		self.OnSelectObject(self.application.cache.objects[self.current])

	def OnMediaDownloadDone(self, evt):
		if evt is None:
			return
		
		if (self.current == -1):
			return

		if self.FoldPanelBar.waitingimages.has_key(evt.file):
			del self.FoldPanelBar.waitingimages[evt.file]
			self.OnSelectObject(self.application.cache.objects[self.current])

	def OnSelectObject(self, evt):
		if evt.id == self.current:
			return
		self.current = evt.id

		try:
			object = self.application.cache.objects[evt.id]
		except:
			do_traceback()
			return

		self.Title.SetLabel(object.name)

		# Add the object type specific information
	
		self.DetailsPanel.DestroyChildren()
		# Create a new panel
		self.ArgumentsPanel = wx.Panel(self.DetailsPanel, -1)

		self.ArgumentsPanel.SetAutoLayout( True )
		self.ArgumentsSizer = wx.FlexGridSizer( 1, 1, 0, 0)
		self.ArgumentsPanel.SetSizer(self.ArgumentsSizer)
		self.ArgumentsSizer.AddGrowableCol( 0 )
		self.ArgumentsSizer.AddGrowableRow( 0 )
		
		self.FoldPanelBar = FoldPanel(self.ArgumentsPanel, self.application)
		for group in object.properties:
			for parameter in group.structures:
				self.FoldPanelBar.AddPanelForParam(parameter, getattr(object, group.name))
			
		self.ArgumentsSizer.Add(self.FoldPanelBar, 1, wx.GROW|wx.EXPAND|wx.ALIGN_CENTER)
		
		cs = fpb.CaptionBarStyle()
		cs.SetFirstColour(wx.Colour(0, 0, 0))
		cs.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)
		item = self.FoldPanelBar.FoldBar.AddFoldPanel("Parent", collapsed=False, cbstyle=cs)
		panel = infoReferenceObject(item, self.application)
		panel.setObject(self.application.cache.objects[object.parent].name, object.parent)
		self.FoldPanelBar.FoldBar.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			
		otherstring = ""
		otherstring += "Name: %s     ID: %s\n" % (object.name, object.id)
		otherstring += "Modify Time: %s\n" % object.modify_time
		if len(object.desc) > 0:
			otherstring += "Desc: %s" % object.desc

		self.FoldPanelBar.add_panel(["Other", otherstring])

		self.ArgumentsPanel.Layout()

		self.DetailsSizer.Add( self.ArgumentsPanel, flag=wx.GROW|wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		
		bestsize = self.FoldPanelBar.GetPanelsLength(True, True)
		self.DetailsPanel.SetVirtualSize((bestsize[1]/2, bestsize[2]))
		
		self.DetailsPanel.Layout()
		self.DetailsPanel.SetupScrolling(True, True)

	def OnSize(self, evt):
		bestsize = self.FoldPanelBar.GetPanelsLength(True, True)
		self.DetailsPanel.SetVirtualSize((bestsize[1]/2, bestsize[2]))
		self.FoldPanelBar.RedisplayFoldPanelItems()
		self.Layout()

def GetPanelForReference(application, parent, type, id, quantity=-1):
	cache = application.cache
	reftype = GenericRS.Types[type]
	if "Player Action" in reftype:
		pass
	elif "Player" in reftype:
		panel = infoReferencePlayer(parent)
		panel.setPlayer(cache.players[id].name, id, quantity)
		return panel
	elif "Object Action" in reftype:
		pass
	elif "Object" in reftype:
		panel = infoReferenceObject(parent, application)
		panel.setObject(cache.objects[id].name, id, quantity)
		return panel
	elif "Order Type" in reftype:
		panel = infoReferenceOrderDesc(parent)
		if not objects.OrderDescs().has_key(id):
			print "WARNING: Unknown order type with id %s" % id
			return None

		od = objects.OrderDescs()[id]
		panel.setOrderDesc(od._name, id, quantity)
		return panel
	elif "Order Instance" in reftype:
		panel = infoReferenceOrder(parent)
		panel.setOrder(cache.orders[id].name, id, quantity)
		return panel
	elif "Resource Description" in reftype:
		panel = infoReferenceResource(parent)
		panel.setResource(cache.resources[id].name, id, quantity)
		return panel
	elif "Design" in reftype:
		panel = infoReferenceDesign(parent)
		panel.setDesign(cache.designs[id].name, id, quantity)
		return panel
	elif "Board" in reftype:
		pass
	elif "Message" in reftype:
		pass
	
	return None

class ArgumentPanel(object):
	"""\
	Base class for all other Argument panels.
	"""

	pass

from windows.xrc.infoPosition3D import infoPosition3DBase
class infoPosition3D(infoPosition3DBase):
	def __init__(self, parent, application):
		infoPosition3DBase.__init__(self, parent)
		self.application = application
		from windows.main.panelStarMap import panelStarMap
		self.starmap = self.application.gui.main.panels[panelStarMap.title]
		self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)

	def setPositionLabel(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		position = "[%s, %s, %s]" % (x, y, z)
		self.PositionLabel.SetLabel(position)

	def OnButtonPressed(self, evt):
		self.starmap.Canvas.Zoom(1, (self.x, self.y))

from windows.xrc.infoVelocity3D import infoVelocity3DBase
class infoVelocity3D(infoVelocity3DBase):
	def setVelocityLabel(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		velocity = "[%s, %s, %s]" % (x, y, z)
		self.VelocityLabel.SetLabel(velocity)
	
from windows.xrc.infoSize import infoSizeBase
class infoSize(infoSizeBase):
	def setSizeLabel(self, size):
		self.SizeLabel.SetLabel(size)
	
from windows.xrc.infoMedia import infoMediaBase
class infoMedia(infoMediaBase):
		
	def setImage(self, application, imageurl):
		file = application.media.GetFile(imageurl)
		
		if file == None:
			icon = wx.Image(os.path.join(graphicsdir, "unknown-icon.png")).ConvertToBitmap()
			self.Media.SetBitmap(icon)
			self.SetSize(self.Media.GetBestSize())
			self.Layout()
			return False
		else:	
			icon = wx.Image(file).ConvertToBitmap()
			self.Media.SetBitmap(icon)
			self.SetSize(self.Media.GetBestSize())
			self.Layout()
			return True

from windows.xrc.infoInteger import infoIntegerBase
class infoInteger(infoIntegerBase):
	def setIntegerLabel(self, integer):
		self.IntegerLabel.SetLabel(integer)

from windows.xrc.infoReferencePlayer import infoReferencePlayerBase
class infoReferencePlayer(infoReferencePlayerBase):
	def __init__(self, parent):
		infoReferencePlayerBase.__init__(self, parent)
		self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)

	def setPlayer(self, name, id, quantity=-1):
		self.pid = id
		if quantity == -1:
			self.Quantity.SetLabel("")
			self.Spacer.SetSize((0,0))
			self.Spacer.SetMinSize((0,0))
		else:
			self.Quantity.SetLabel(str(quantity))
			self.Spacer.SetSize((10,10))
			self.Spacer.SetMinSize((10,10))
		self.PlayerName.SetLabel(name)
	
	def OnButtonPressed(self, evt):
		# FIXME: Should allow sending a message to the player.
		pass

from windows.xrc.infoReferenceObject import infoReferenceObjectBase
class infoReferenceObject(infoReferenceObjectBase):
	def __init__(self, parent, application):
		infoReferenceObjectBase.__init__(self, parent)
		self.application = application
		self.Bind(wx.EVT_BUTTON, self.OnButtonPressed)

	def setObject(self, name, id, quantity=-1):
		self.oid = id
		if quantity == -1:
			self.Quantity.SetLabel("")
			self.Spacer.SetSize((0,0))
			self.Spacer.SetMinSize((0,0))
		else:
			self.Quantity.SetLabel(str(quantity))
			self.Spacer.SetSize((10,10))
			self.Spacer.SetMinSize((10,10))
		self.ObjectName.SetLabel(name)
	
	def OnButtonPressed(self, evt):
		self.application.Post(self.application.gui.SelectObjectEvent(self.oid))

from windows.xrc.infoReferenceOrder import infoReferenceOrderBase
class infoReferenceOrder(infoReferenceOrderBase):
	def setOrder(self, name, id, quantity=-1):
		self.oid = id
		if quantity == -1:
			self.Quantity.SetLabel("")
			self.Spacer.SetSize((0,0))
			self.Spacer.SetMinSize((0,0))
		else:
			self.Quantity.SetLabel(str(quantity))
			self.Spacer.SetSize((10,10))
			self.Spacer.SetMinSize((10,10))
		self.OrderName.SetLabel(name)

from windows.xrc.infoReferenceOrderDesc import infoReferenceOrderDescBase
class infoReferenceOrderDesc(infoReferenceOrderDescBase):
	def setOrderDesc(self, name, id, quantity=-1):
		self.oid = id
		if quantity == -1:
			self.Quantity.SetLabel("")
			self.Spacer.SetSize((0,0))
			self.Spacer.SetMinSize((0,0))
		else:
			self.Quantity.SetLabel(str(quantity))
			self.Spacer.SetSize((10,10))
			self.Spacer.SetMinSize((10,10))
		self.OrderDescName.SetLabel(name)

from windows.xrc.infoReferenceDesign import infoReferenceDesignBase
class infoReferenceDesign(infoReferenceDesignBase):
	def setDesign(self, name, id, quantity=-1):
		self.did = id
		if quantity == -1:
			self.Quantity.SetLabel("")
			self.Spacer.SetSize((0,0))
			self.Spacer.SetMinSize((0,0))
		else:
			self.Quantity.SetLabel(str(quantity))
			self.Spacer.SetSize((10,10))
			self.Spacer.SetMinSize((10,10))
		self.DesignName.SetLabel(name)

from windows.xrc.infoReferenceResource import infoReferenceResourceBase
class infoReferenceResource(infoReferenceResourceBase):
	def setResource(self, name, id, quantity=-1):
		self.did = id
		if quantity == -1:
			self.Quantity.SetLabel("")
			self.Spacer.SetSize((0,0))
			self.Spacer.SetMinSize((0,0))
		else:
			self.Quantity.SetLabel(str(quantity))
			self.Spacer.SetSize((10,10))
			self.Spacer.SetMinSize((10,10))
		self.ResourceName.SetLabel(name)

from windows.xrc.infoReferenceContainer import infoReferenceContainerBase
class infoReferenceContainer(infoReferenceContainerBase):
	def addPanel(self, panel):
		sizer = self.MainPanel.GetSizer()
		sizer.SetRows(sizer.GetRows()+1)
		sizer.AddGrowableRow(sizer.GetRows()-1)
		sizer.Add(panel, 1, wx.ALL | wx.EXPAND | wx.GROW)
		self.SetSize(self.GetBestSize())
		self.Layout()
		
from windows.xrc.infoOrderQueue import infoOrderQueueBase
class infoOrderQueue(infoOrderQueueBase):
	def setQueueID(self, id):
		self.qid = id
		self.QueueID.SetLabel(str(id))
	
	def setNumOrders(self, num):
		self.NumOrders.SetLabel(str(num))
	
	def setAllowedTypes(self, types):
		self.AllowedTypes.SetLabel(types)

from windows.xrc.infoResourcePanel import infoResourcePanelBase
class infoResourcePanel(infoResourcePanelBase):
	def setValues(self, stored, minable, inaccessible):
		self.StoredValue.SetLabel(str(stored))
		self.MinableValue.SetLabel(str(minable))
		self.InaccessibleValue.SetLabel(str(inaccessible))

from windows.xrc.FoldPanel import FoldPanelBase
class FoldPanel(ArgumentPanel, FoldPanelBase):
	def __init__(self, parent, application):
		FoldPanelBase.__init__(self, parent)
		self.application = application
		self.cache = self.application.cache
		self.waitingimages = {}
		self.Layout()
		
	def add_panel(self, list):
		self.__text = list[0]
		
		cs = fpb.CaptionBarStyle()
		cs.SetFirstColour(wx.Colour(0, 0, 0))
		cs.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)
		item = self.FoldBar.AddFoldPanel(self.__text, collapsed=False, cbstyle=cs)
		self.FoldBar.ApplyCaptionStyle(item, cs)
		if len(list) > 0:
			for data in list[1:]:
				self.FoldBar.AddFoldPanelWindow(item, wx.StaticText(item, -1, data), fpb.FPB_ALIGN_WIDTH, 5, 20) 
		
		self.Layout()
		
	def AddPanelForParam(self, group, parent):
		attr = getattr(parent, group.name)
		cs = fpb.CaptionBarStyle()
		cs.SetFirstColour(wx.Colour(0, 0, 0))
		cs.SetCaptionStyle(fpb.CAPTIONBAR_RECTANGLE)
		item = self.FoldBar.AddFoldPanel(group.name, collapsed=False, cbstyle=cs)
		if isinstance(group, parameters.ObjectParamPosition3d):
			pospanel = infoPosition3D(item, self.application)
			pospanel.setPositionLabel(attr.vector.x, attr.vector.y, attr.vector.z)
			self.FoldBar.AddFoldPanelWindow(item, pospanel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			return
		elif isinstance(group, parameters.ObjectParamVelocity3d) or isinstance(group, parameters.ObjectParamAcceleration3d):
			velpanel = infoVelocity3D(item, self.application)
			velpanel.setVelocityLabel(attr.vector.x, attr.vector.y, attr.vector.z)
			self.FoldBar.AddFoldPanelWindow(item, velpanel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			return
		elif isinstance(group, parameters.ObjectParamSize):
			size = "%s" % attr.size
			sizepanel = infoSize(item)
			sizepanel.setSizeLabel(size)
			self.FoldBar.AddFoldPanelWindow(item, sizepanel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			return
		elif isinstance(group, parameters.ObjectParamMedia):
			url = "%s" % attr.url
			mediapanel = infoMedia(item)
			# FIXME: Do something about multiple media options for the filename?
			imageurls = self.application.media.GetFilenames(url)
			if len(imageurls) <= 0:
				return
			else:
				imageurl = self.application.media.GetFile(imageurls[0])
			result = mediapanel.setImage(self.application, imageurl)
			if not result:
				self.waitingimages[imageurl] = attr
			self.FoldBar.AddFoldPanelWindow(item, mediapanel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			return
		elif isinstance(group, parameters.ObjectParamInteger):
			integer = "%s" % attr.value
			integerpanel = infoInteger(item)
			integerpanel.setIntegerLabel(integer)
			self.FoldBar.AddFoldPanelWindow(item, integerpanel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			return
		elif isinstance(group, parameters.ObjectParmReference):
			panel = GetPanelForReference(self.application, item, attr.type, attr.id)
			if (panel != None):
				self.FoldBar.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			return
		elif isinstance(group, parameters.ObjectParamReferenceQuantityList):
			containerpanel = infoReferenceContainer(item)
			for type, id, number in attr.references:
				panel = GetPanelForReference(self.application, containerpanel, type, id, number)
				if (panel != None):
					containerpanel.addPanel(panel)
				containerpanel.Layout()
			self.FoldBar.AddFoldPanelWindow(item, containerpanel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			return
		elif isinstance(group, parameters.ObjectParamOrderQueue):
			orderpanel = infoOrderQueue(item)
			orderpanel.setQueueID(attr.queueid)
			orderpanel.setNumOrders(attr.numorders)
			types = "["
			if len(attr.ordertypes) > 0:
				for ordertype in attr.ordertypes:
					types += "%s, " % objects.OrderDescs()[ordertype]._name
				types = types[:-2]
			types += "]"
			orderpanel.setAllowedTypes(types)
			self.FoldBar.AddFoldPanelWindow(item, orderpanel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			self.FoldBar.RedisplayFoldPanelItems()
			return
		elif isinstance(group, parameters.ObjectParamResourceList):
			containerpanel = infoReferenceContainer(item)
			for id, stored, minable, unavailable in attr.resources:
				panel = infoResourcePanel(containerpanel)
				panel.setValues(stored, minable, unavailable)
				containerpanel.addPanel(panel)
				containerpanel.Layout()
			self.FoldBar.AddFoldPanelWindow(item, containerpanel, fpb.FPB_ALIGN_WIDTH, 5, 20)
			return

	def GetPanelsLength(self, collapsed, expanded):
		return self.FoldBar.GetPanelsLength(collapsed, expanded)
		
	def RedisplayFoldPanelItems(self):
		self.FoldBar.RedisplayFoldPanelItems()

	def get_value(self):
		return []
