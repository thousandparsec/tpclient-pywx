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

from windows.xrc.panelMessage import panelMessageBase
class panelMessage(panelMessageBase, ShiftMixIn):
	title = _("Messages")

	def __init__(self, application, parent):
		panelMessageBase.__init__(self, parent)
		ShiftMixIn.__init__(self)

		self.application = application
		self.Message.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnLinkEvent)

		# The current message slot
		self.slot = 0
		self.position = 0
		self.dirty = True

		# Contains the message types to be filtered
		self.filtered = Set()

		self.application.gui.Binder(self.application.CacheClass.CacheUpdateEvent, self.OnCacheUpdate)

	def OnLinkEvent(self, evt):
		link = evt.GetLinkInfo().GetHref()
		print link
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
		info.Bottom()
		info.Layer(1)
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
			
		self.BoardSet(0, evt.slot)
		self.dirty = True

	def message(self):
		"""\
		Returns the currently displayed message.
		"""
		return self.messages[self.slot]
	message = property(message)

	def messages(self):
		"""\
		Returns all the messages for the current board.
		"""
		if self.application.cache.messages.has_key(self.bid):
			return self.application.cache.messages[self.bid]
		else:
			return []
	messages = property(messages)

	def messages_unfiltered(self):
		"""\
		Returns a list of the slots for unfiltered messages.
		"""
		if self.dirty:
			unfiltered = []
			for i in range(0, len(self.messages)):
				if self.filtered > Set(self.messages[i].types):
					continue
				unfiltered.append(i)
			self.__unfiltered = unfiltered
			return unfiltered
		else:
			return self.__unfiltered 
	messages_unfiltered = property(messages_unfiltered)

	def BoardSet(self, id, slot=0):
		"""\
		Set the currently displayed board to id.
		"""
		self.bid = id
		self.MessageSet(direction=0)
	
	def MessageSet(self, direction=None, slot=None):
		"""\
		Set the currently displayed message to the given slot.

		Only shows messages which havn't been filtered.
		Giving -1 will find first unfiltered message.
		"""
		# Are there any messages?
		if len(self.messages) == 0:
			message_subject = _("No messages")
			message_counter = _("")
			message_body = self.html_nomessage
			message_filter = False
			message_buttons = [False, False, False, False]

		# Well are there any 
		elif len(self.messages_unfiltered) == 0:
			print "All messages were filtered"
			message_subject = _("All filtered")
			message_counter = _("")
			message_body = self.html_allfiltered
			message_filter = False
			message_buttons = [False, False, False, False]

		elif direction != None or slot != None:
			# Are we going to a specific message?
			if slot != None:
				if slot > len(self.messages) or slot < 0:
					raise IOError("Tried to go to a place that doesn't exist!")

				self.slot = slot

				# Find the closest unfiltered position
				for i in range(1, len(self.messages_unfiltered)):
					if self.messages_unfiltered[i] > self.slot:
						self.position = i-1

			# Are we just going in a general direction
			if direction != None:
				self.position += direction

				# Can't go of the end
				if self.position >= len(self.messages_unfiltered):
					self.position = len(self.messages_unfiltered)-1
				if self.position < 0:
					self.position = 0
				
				self.slot = self.messages_unfiltered[self.position]

			message_subject = self.message.subject
			if self.slot in self.messages_unfiltered:
				message_body = self.html_message % self.message.__dict__
			else:
				message_body = self.html_filtered % self.message.__dict__

			print "references", self.message.references
			
			message_filter = not self.slot in self.messages_unfiltered
			message_buttons = [
				self.position > 0, 
				GenericRS.Types["Object"] in self.message.references.types,
				self.position < len(self.messages_unfiltered)-1,
				True
			]
			message_counter = _("%i of %i") % (self.slot+1, len(self.messages))

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
		self.MessageSet(-len(self.messages))

	def OnNext(self, evt=None):
		self.MessageSet(1)
	
	def OnLast(self, evt=None):
		self.MessageSet(len(self.messages))

	def OnPrev(self, evt=None):
		self.MessageSet(-1)
		
	def OnDelete(self, evt=None):
		# Get the current slot
		slot = self.slot

		if slot == -1:
			return

		# Tell everyone about the change
		self.application.Post(self.application.cache.CacheDirtyEvent("messages", "remove", self.bid, slot, None), source=self)

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
		pass
