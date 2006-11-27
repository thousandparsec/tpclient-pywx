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
import wx.lib.anchors

# Local Imports
from winBase import *

# Protocol Imports
from tp.netlib import failed, GenericRS

MESSAGE_FILTER = 10000
MESSAGE_TITLE = 10001
MESSAGE_ID = 10002
MESSAGE_HTML = 10003
MESSAGE_PREV = 10004
MESSAGE_GOTO = 10005
MESSAGE_NEXT = 10006
MESSAGE_LINE = 10007
MESSAGE_NEW = 10008
MESSAGE_DEL = 10009

# Shows messages from the game system to the player.
class winMessage(winBase, winShiftMixIn):
	title = _("Messages")

	from defaults import winMessageDefaultPosition as DefaultPosition
	from defaults import winMessageDefaultSize as DefaultSize
	from defaults import winMessageDefaultShow as DefaultShow
	
	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)
		winShiftMixIn.__init__(self)

		panel = wx.Panel(self, -1)
		panel.SetConstraints(wx.lib.anchors.LayoutAnchors(self, 1, 1, 1, 1))
		self.panel = panel
		self.obj = {}

		item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
		item0.AddGrowableCol( 0 )
		item0.AddGrowableRow( 1 )

		item1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		item1.AddGrowableCol( 1 )

		self.filter = wx.CheckBox( panel, MESSAGE_FILTER, _("Filter"), wx.DefaultPosition, wx.local.buttonSize, 0 )
		self.filter.SetFont(wx.local.normalFont)
		item1.Add( self.filter, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )

		self.titletext = wx.StaticText( panel, MESSAGE_TITLE, _("Title"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE )
		self.titletext.SetFont(wx.local.normalFont)
		item1.Add( self.titletext, 0, wx.GROW|wx.ALIGN_CENTRE_HORIZONTAL|wx.ALL, 1 )

		self.counter = wx.StaticText( panel, MESSAGE_ID, _("# of #"), wx.DefaultPosition, wx.local.buttonSize, 0 )
		self.counter.SetFont(wx.local.normalFont)
		item1.Add( self.counter, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )

		item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )

		item5 = wx.FlexGridSizer( 0, 2, 0, 0 )
		item5.AddGrowableCol( 0 )
		item5.AddGrowableRow( 0 )

		# This is the main HTML display!
		item6 = wx.html.HtmlWindow(panel, MESSAGE_HTML, wx.DefaultPosition, wx.Size(200,10))
		item5.Add( item6, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 1 )

		self.html = item6
		if wx.Platform != "__WXMAC__":
#			pass
#			self.html.SetFonts("Swiss", "Courier", [10, 12, 14, 16, 20, 24])
#		else:
			self.html.SetFonts("Swiss", "Courier", [4, 6, 8, 10, 12, 14, 16])
		self.html.SetPage("")

		item7 = wx.BoxSizer( wx.VERTICAL )

		self.prev = wx.Button( panel, -1, _("Prev"), wx.DefaultPosition, wx.local.buttonSize)
		self.prev.SetFont(wx.local.normalFont)
		item7.Add( self.prev, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessagePrev, self.prev)
		self.prev.SetToolTip(wx.ToolTip(_("Goto previous message.")))

		self.first = wx.Button( panel, -1, _("First"), wx.DefaultPosition, wx.local.buttonSize)
		self.first.SetFont(wx.local.normalFont)
		item7.Add( self.first, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageFirst, self.first)
		self.first.Hide()
		self.first.SetToolTip(wx.ToolTip(_("Goto first message.")))

		self.goto = wx.Button( panel, -1, _("Goto"), wx.DefaultPosition, wx.local.buttonSize)
		self.goto.SetFont(wx.local.normalFont)
		item7.Add( self.goto, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageGoto, self.goto)
		self.goto.Disable()
		self.goto.SetToolTip(wx.ToolTip(_("Goto object talked about in this message.")))

		self.next = wx.Button( panel, -1, _("Next"), wx.DefaultPosition, wx.local.buttonSize)
		self.next.SetFont(wx.local.normalFont)
		item7.Add( self.next, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageNext, self.next)
		self.next.SetToolTip(wx.ToolTip(_("Goto next message.")))

		self.last = wx.Button( panel, -1, _("Last"), wx.DefaultPosition, wx.local.buttonSize)
		self.last.SetFont(wx.local.normalFont)
		item7.Add( self.last, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageLast, self.last)
		self.last.Hide()
		self.last.SetToolTip(wx.ToolTip(_("Goto last message.")))

		item11 = wx.StaticLine( panel, MESSAGE_LINE, wx.DefaultPosition, wx.Size(20,-1), wx.LI_HORIZONTAL )
		item11.Enable(False)
		item7.Add( item11, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		new = wx.Button( panel, -1, _("New"), wx.DefaultPosition, wx.local.buttonSize)
		new.SetFont(wx.local.normalFont)
		item7.Add( new, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageNew, new)
		new.Disable()

		self.delete = wx.Button( panel, -1, _("Delete"), wx.DefaultPosition, wx.local.buttonSize)
		self.delete.SetFont(wx.local.normalFont)
		item7.Add( self.delete, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageDelete, self.delete)

		item5.Add( item7, 0, wx.GROW|wx.ALIGN_RIGHT|wx.ALL, 1 )

		item0.Add( item5, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 1 )

		panel.SetAutoLayout(True)
		panel.SetSizer( item0 )
		
		item0.Fit( panel )
		item0.SetSizeHints( panel )
	
		# The current message slot
		self.slot = 0
		self.position = 0
		self.dirty = True

		# Contains the message types to be filtered
		self.filtered = Set()

	html_filtered = """\
<html>
<body>
<center>
	<table cols=1 width="100%%" background="./graphics/filtered.png">
		<tr>
			<td><b>Subject:</b> %(subject)s</td>
		</tr>
		<tr>
			<td>%(body)s</td>
		</tr>
	</table>
</center>
</body>
</html>"""

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
</html>"""

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
			You have recived no messages this turn!<br><br>
			Actually if you didn't recive any messages it most proberly
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
	<table cols=1 width="100%" background="./graphics/filtered.png">
		<tr>
			<td><b>Subject:</b> All messages filtered
		</tr>
		<tr>
			<td>All messages you have recived this turn have been filtered.</td>
		</tr>
	</table>
</center>
</body>
</html>"""

	def Show(self, show=True):
		if show:
			self.ShiftStart()
			winBase.Show(self)
		else:
			self.Hide()

	def Hide(self, hide=True):
		if hide:
			self.ShiftStop()
			winBase.Hide(self)
		else:
			self.Show()
		
	def OnShiftDown(self, evt):
		self.ShowFL()
	
	def OnShiftUp(self, evt):
		self.ShowPN()
	
	def ShowPN(self):
		self.first.Hide()
		self.last.Hide()
		
		self.prev.Show()
		self.next.Show()

		self.panel.Layout()

	def ShowFL(self):
		self.prev.Hide()
		self.next.Hide()

		self.first.Show()
		self.last.Show()
		
		self.panel.Layout()
		
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

		self.filter.SetValue(message_filter)
		self.titletext.SetLabel(message_subject)
		self.counter.SetLabel(message_counter)
		self.html.SetPage(message_body)

		self.prev.Enable(message_buttons[0])
		self.first.Enable(message_buttons[0])
		self.goto.Enable(message_buttons[1])
		self.last.Enable(message_buttons[2])
		self.next.Enable(message_buttons[2])
		self.delete.Enable(message_buttons[3])

	def MessageFirst(self, evt=None):
		self.MessageSet(-len(self.messages))

	def MessageNext(self, evt=None):
		self.MessageSet(1)
	
	def MessageLast(self, evt=None):
		self.MessageSet(len(self.messages))

	def MessagePrev(self, evt=None):
		self.MessageSet(-1)
		
	def MessageDelete(self, evt=None):
		# Get the current slot
		slot = self.slot

		if slot == -1:
			return

		# Tell everyone about the change
		self.application.Post(self.application.cache.CacheDirtyEvent("messages", "remove", self.bid, slot, None))

	def MessageGoto(self, slot):
		# Select the object this message references
		id = None
		for reference, id in self.message.references:
			if reference == GenericRS.Types["Object"]:
				break
		if not id is None:
			self.application.Post(self.application.gui.SelectObjectEvent(id))

	def MessageNew(self, evt=None):
		pass
	
	def MessageFilter(self):
		pass
