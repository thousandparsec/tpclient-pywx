"""\
This module contains the message window, it displays all the ingame messages and
lets the player filter out unimportant messages.

Messages are displayed using basic HTML.
"""

# Python Imports
from sets import Set

# wxPython Imports
import wx
import wx.html

# Config information
from requirements import graphicsdir

# Local Imports
from windows.winBase import ShiftMixIn

# Protocol Imports
from tp.netlib import GenericRS
from tp.client.ChangeList import ChangeList, ChangeNode

from windows.xrc.winFilterManager import FilterManagerBase
class FilterManager(FilterManagerBase, wx.Frame):
	"""\
	This class is a popup window with a checklist of filters.
	"""
	def __init__(self, control, parent, cache):
		"""\
		Initialize the window, loading data from XRC, and add the resources.
		"""
		FilterManagerBase.__init__(self, parent)
		self.parent = parent
		self.control = control
		
		self.FilterOptions = {}

		self.Bind(wx.EVT_ACTIVATE, self.OnActivate)
		self.Hide()

	def SetOptions(self, filteroptions):
		"""\
		Called to set the filter options, takes a list of strings.
		"""
		self.FilterList.Clear()
		self.FilterList.InsertItems(filteroptions, 0)
	
	def OnActivate(self, evt):
		"""\
		Called when the window becomes active or inactive.
		"""
		if evt.GetActive() == False:
			self.OnDone(evt)

	def Show(self, show=True):
		"""\
		Called when the window is shown.
		"""
		self.Panel.Layout()

		size = self.FilterList.GetBestSize()
		self.FilterList.SetMinSize(size+(10,10))

		self.SetMinSize(self.Panel.GetBestSize()+(10,10))
		self.SetSize(self.Panel.GetBestSize()+(10,10))
		#self.SetMaxSize(size)

		wx.Frame.Show(self)

	def OnDone(self, evt):
		"""\
		Called when the "Done" button is pressed.
		"""
		self.control.PopDown()

class FilterManagerControl(object):
	"""\
	This class is a button that can be clicked to open a checklist of filters,
	and which takes the data from that window to create a list of the checked
	filters.
	"""
	def __init__(self, cache, parent, id, button):
		"""\
		Called to create the button and the popup window.
		"""
		
		self.button = button
		self.button.Bind(wx.EVT_BUTTON, self.OnClick)
		self.cache = cache
		self.parent = parent
		self.selected = []
		self.win = FilterManager(self, self.button, cache)
		self.showfiltered = False
	
	def OnClick(self, evt):
		"""\
		Called when the button is clicked.
		"""
		if not self.win.IsShown():
			self.win.Show()
			self.win.Move(self.button.GetScreenRect().GetTopLeft()-(0,self.win.GetSizeTuple()[1]))
		else:
			self.PopDown()
		
	def PopDown(self):
		"""\
		Closes the popup window and collects the data.
		"""
		i = 0
		while i < self.win.CurrentFilters.GetCount():
			if not self.win.CurrentFilters.IsChecked(i*1):
				i = i+1
				continue
			appendstring = self.win.CurrentFilters.GetString(i)
			self.win.CurrentFilters.Delete(i)
			i = i-1
			try:
				self.selected.remove(appendstring)
			except ValueError:
				i = i+1
				continue
			i = i+1

		for i in range(0, self.win.FilterList.GetCount()):
			if not self.win.FilterList.IsChecked(i):
				continue
			appendstring = self.win.FilterList.GetString(i).split("'")[1]
			try:
				self.selected.index(appendstring)
			except ValueError:
				self.selected.append(appendstring)
			self.win.FilterList.Check(i, 0)
			if (self.win.CurrentFilters.FindString(appendstring) != -1):
				continue
			self.win.CurrentFilters.Append(self.win.FilterList.GetString(i).split("'")[1])
		
		self.showfiltered = self.win.ShowFiltered.IsChecked()
		
		self.parent.RebuildMessageList()
		self.win.Hide()

from windows.xrc.panelMessage import panelMessageBase
class panelMessage(panelMessageBase, ShiftMixIn):
	title = _("Messages")

	def __init__(self, application, parent):
		panelMessageBase.__init__(self, parent)
		ShiftMixIn.__init__(self)

		self.application = application
		self.Message.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnLinkEvent)
		
		self.FilterManager = FilterManagerControl(self.application.cache, self, -1, self.Filter)

		# The current message slot
		self.node = None

		self.application.gui.Binder(self.application.CacheClass.CacheUpdateEvent, self.OnCacheUpdate)
		self.Layout()

	def OnLinkEvent(self, evt):
		link = evt.GetLinkInfo().GetHref()
		from extra.Opener import open
		open(link)

	html_filtered = """\
<html>
<body>
<center>
	<table cols=1 width="100%%" background="%GRAPHICS/graphics/filtered.png">
		<tr>
			<td><b>Subject:</b> %(subject)s</td>
		</tr>
		<tr>
			<td>%(body)s</td>
		</tr>
	</table>
</center>
</body>
</html>""".replace("%GRAPHICS", graphicsdir)

	html_message = """\
<html>
<body>
<center>
	<table cols=1 width="100%%">
		<tr>
			<td><b>Subject:</b> %(subject)s</td>
		</tr>
		<tr>
			<td>%(body)s</td>
		</tr>
	</table>
</center>
</body>
</html>""".replace("%GRAPHICS", graphicsdir)

	html_nomessage = """\
<html>
<body>
<center>
	<table cols=1 width="100%">
		<tr>
			<td><b>Subject:</b> You are unloved!
		</tr>
		<tr>
			<td>
			You have received no messages this turn!<br><br>
			Actually if you didn't receive any messages it most probably
			means that your client couldn't load the results from the server.
			Try reload/restart the client.
			</td>
		</tr>
	 </table>
</center>
</body>
</html>"""

	html_allfiltered = """\
<html>
<body>
<center>
	<table cols=1 width="100%" background="%GRAPHICS/graphics/filtered.png">
		<tr>
			<td><b>Subject:</b> All messages filtered
		</tr>
		<tr>
			<td>All messages you have received this turn have been filtered.</td>
		</tr>
	</table>
</center>
</body>
</html>""".replace("%GRAPHICS", graphicsdir)

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()
		info.MinSize(self.GetBestSize())
		info.BestSize(self.GetBestSize())
		info.Right()
		info.Layer(1)
		info.CaptionVisible(True)
		info.Caption(self.title)
		return info

	def Show(self, show=True):
		if show:
			self.ShiftStart()
			panelMessageBase.Show(self)
		else:
			self.Hide()

	def Hide(self, hide=True):
		if hide:
			self.ShiftStop()
			panelMessageBase.Hide(self)
		else:
			self.Show()
		
	def OnShiftDown(self, evt):
		self.ShowFL()
	
	def OnShiftUp(self, evt):
		self.ShowPN()
	
	def ShowPN(self):
		self.First.Hide()
		self.Last.Hide()
		
		self.Prev.Show()
		self.Next.Show()

		self.Layout()

	def ShowFL(self):
		self.Prev.Hide()
		self.Next.Hide()

		self.First.Show()
		self.Last.Show()
		
		self.Layout()
		
	def OnCacheUpdate(self, evt=None):
		"""\
		Called when the cache is updated.
		"""
		# If it's a full cache update
		if evt.what == None:
			self.BoardSet(0)
			return
		
		# Only intrested in an order has been updated and we are currently looking at that
		if evt.what != "messages" or evt.id != self.bid:
			return
			
		self.BoardSet(0, evt.node)

	@property
	def message(self):
		"""\
		Returns the currently displayed message.
		"""
		return self.node.CurrentOrder

	@property
	def messages(self):
		"""\
		Returns all the messages for the current board.
		"""
		if not self.application.cache.messages.has_key(self.bid):
			return []
		
		return self.messagelist
	
	def RebuildMessageList(self):
		self.messagelist=ChangeList()
		
		if len(self.messages) == 0:
			message_subject = _("No messages")
			message_counter = _(" ")
			message_body = self.html_nomessage
			message_filter = False
			message_buttons = [False, False, False, False]
			
			self.Title.SetLabel(message_subject)
			self.Counter.SetLabel(message_counter)
			self.Message.SetPage(message_body)

			self.Prev.Enable(message_buttons[0])
			self.First.Enable(message_buttons[0])
			self.Goto.Enable(message_buttons[1])
			self.Last.Enable(message_buttons[2])
			self.Next.Enable(message_buttons[2])
			self.Delete.Enable(message_buttons[3])
		
		for node in self.application.cache.messages[self.bid]:
			message = node.CurrentOrder
			messagefiltered = False
			for reference, id in message.references:
				id = message.references.GetReferenceValue(reference, id)
				for filtertype in self.FilterManager.selected:
					if ("%s" % GenericRS.Types[reference] == "%s" % filtertype or GenericRS.Types[reference] + ": %s" % id == "%s" % filtertype):
						messagefiltered = True
			if messagefiltered:
				if self.FilterManager.showfiltered:
					message.set_types("filtered")
					self.messagelist.append(ChangeNode(message))
			else:
				self.messagelist.append(ChangeNode(message))
								
			if not self.messages.first is None:
				self.MessageSet(node=self.messages.first)

	def BoardSet(self, id, node=None):
		"""\
		Set the currently displayed board to id.
		"""
		self.bid = id
		
		self.RebuildMessageList()
	
	def MessageSet(self, direction=None, node=None):
		"""\
		Set the currently displayed message to the given node.
		"""
		# Are there any messages?
		if len(self.messages) == 0:
			message_subject = _("No messages")
			message_counter = ""
			message_body = self.html_nomessage
			message_filter = False
			message_buttons = [False, False, False, False]

		else:
			if not direction is None:
				if direction > 0 and not self.node.right is None:
					self.node = self.node.right

				elif direction < 0 and not self.node.left.left is None:
					self.node = self.node.left

				else:
					raise SystemError("Need to give a direction or node")

			elif not node is None:
				assert node in self.messages
				self.node = node
			else:
				raise SystemError("Need to give a direction or node")

			message_subject = self.message.subject
			message_filter = (self.message.types == "filtered")
			if message_filter:
				message_body = self.html_filtered % self.message.__dict__
			else:
				message_body = self.html_message % self.message.__dict__
			
			self.filteroptions = []
			for reference, id in self.message.references:
				id = self.message.references.GetReferenceValue(reference, id)
				self.filteroptions.append("All '" + GenericRS.Types[reference] + "' messages")
				self.filteroptions.append("All '" + GenericRS.Types[reference] + ": %s' messages" % id)
			self.FilterManager.win.SetOptions(self.filteroptions)
						
			message_buttons = [
				not self.node.left.left is None, 
				GenericRS.Types["Object"] in self.message.references.types,
				not self.node.right is None,
				True
			]
			message_counter = _("%(msgnum)i of %(allmsgs)i") % {'msgnum': self.messages.index(self.node)+1, 'allmsgs': len(self.messages)}

		self.Title.SetLabel(message_subject)
		self.Counter.SetLabel(message_counter)
		self.Message.SetPage(message_body)

		self.Prev.Enable(message_buttons[0])
		self.First.Enable(message_buttons[0])
		self.Goto.Enable(message_buttons[1])
		self.Last.Enable(message_buttons[2])
		self.Next.Enable(message_buttons[2])
		self.Delete.Enable(message_buttons[3])

	def OnFirst(self, evt=None):
		self.MessageSet(node=self.messages.first)

	def OnNext(self, evt=None):
		self.MessageSet(1)
	
	def OnFilter(self, evt=None):
		self.MessageFilter()
	
	def OnLast(self, evt=None):
		self.MessageSet(node=self.messages.last)

	def OnPrev(self, evt=None):
		self.MessageSet(-1)
		
	def OnDelete(self, evt=None):
		if len(self.messages) == 0:
			print "OnDelete: No messages to delete."
			return
			
		node = self.application.cache.messages[self.bid].find(self.node._what)
		
		if node == None:
			print "OnDelete: Failed to find message to remove."
			return
			
		# Tell everyone about the change
		self.application.Post(self.application.cache.apply("messages", "remove", self.bid, node, None), source=self)

	def OnGoto(self, slot):
		# Select the object this message references
		ids = []
		for reference, id in self.message.references:
			if reference == GenericRS.Types["Object"]:
				try:
					obj = self.application.cache.objects[id]
					ids.append(id)
				except KeyError:
					pass

		if len(ids) > 1:
			menu = wx.Menu()
			for id in ids:
				try:
					obj = self.application.cache.objects[id]
					menu.Append(-1, "%s (%s)" % (obj.name, obj.id))
				except KeyError:
					pass
			self.Bind(wx.EVT_MENU, self.MessageGotoMenu)
			x, y = self.Goto.GetPosition()
			self.PopupMenu(menu, (x,y+self.Goto.GetSize()[1]))

		elif len(ids) == 1:
			self.application.Post(self.application.gui.SelectObjectEvent(ids[0]), source=self)

	def MessageGotoMenu(self, evt):
		menu = evt.GetEventObject()
		item = menu.FindItemById(evt.GetId())

		id = int(item.GetLabel().split('(')[-1][:-1])
		self.application.Post(self.application.gui.SelectObjectEvent(id), source=self)

	def MessageNew(self, evt=None):
		pass
	
	def MessageFilter(self):
		self.RebuildMessageList()
