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
from tp.netlib import failed

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
class winMessage(winBase):
	title = _("Messages")

	from defaults import winMessageDefaultPosition as DefaultPosition
	from defaults import winMessageDefaultSize as DefaultSize
	from defaults import winMessageDefaultShow as DefaultShow
	
	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)

		panel = wx.Panel(self, -1)
		panel.SetConstraints(wx.lib.anchors.LayoutAnchors(self, 1, 1, 1, 1))
		self.panel = panel
		self.obj = {}

		# Bits for doing the button changing on shift
		self.timer = wx.Timer(self)
		self.shift = False
		
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
		if wx.Platform == "__WXMAC__":
			self.html.SetFonts("Swiss", "Courier", [10, 12, 14, 16, 20, 24])
		else:
			self.html.SetFonts("Swiss", "Courier", [4, 6, 8, 10, 12, 14, 16])
		self.html.SetPage("")

		item7 = wx.BoxSizer( wx.VERTICAL )

		self.prev = wx.Button( panel, -1, _("Prev"), wx.DefaultPosition, wx.local.buttonSize)
		self.prev.SetFont(wx.local.normalFont)
		item7.Add( self.prev, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessagePrev, self.prev)

		self.first = wx.Button( panel, -1, _("First"), wx.DefaultPosition, wx.local.buttonSize)
		self.first.SetFont(wx.local.normalFont)
		item7.Add( self.first, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageFirst, self.first)
		self.first.Hide()

		goto = wx.Button( panel, -1, _("Goto"), wx.DefaultPosition, wx.local.buttonSize)
		goto.SetFont(wx.local.normalFont)
		item7.Add( goto, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		self.next = wx.Button( panel, -1, _("Next"), wx.DefaultPosition, wx.local.buttonSize)
		self.next.SetFont(wx.local.normalFont)
		item7.Add( self.next, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageNext, self.next)

		self.last = wx.Button( panel, -1, _("Last"), wx.DefaultPosition, wx.local.buttonSize)
		self.last.SetFont(wx.local.normalFont)
		item7.Add( self.last, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageLast, self.last)
		self.last.Hide()

		item11 = wx.StaticLine( panel, MESSAGE_LINE, wx.DefaultPosition, wx.Size(20,-1), wx.LI_HORIZONTAL )
		item11.Enable(False)
		item7.Add( item11, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		new = wx.Button( panel, -1, _("New"), wx.DefaultPosition, wx.local.buttonSize)
		new.SetFont(wx.local.normalFont)
		item7.Add( new, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageNew, new)

		delete = wx.Button( panel, -1, _("Delete"), wx.DefaultPosition, wx.local.buttonSize)
		delete.SetFont(wx.local.normalFont)
		item7.Add( delete, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.Bind(wx.EVT_BUTTON, self.MessageDelete, delete)

		item5.Add( item7, 0, wx.GROW|wx.ALIGN_RIGHT|wx.ALL, 1 )

		item0.Add( item5, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 1 )

		panel.SetAutoLayout(True)
		panel.SetSizer( item0 )
		
		item0.Fit( panel )
		item0.SetSizeHints( panel )
	
		# The current message slot
		self.slot = 0

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
			self.timer.Start(50)
			self.Bind(wx.EVT_TIMER, self.OnIdle, self.timer)
			winBase.Show(self)
		else:
			self.Hide()

	def Hide(self, hide=True):
		if hide:
			self.timer.Stop()
			self.Unbind(wx.EVT_TIMER, self.timer)
			winBase.Hide(self)
		else:
			self.Show()

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
		
	def OnIdle(self, evt):
		shift = wx.GetKeyState(wx.WXK_SHIFT)
		if self.shift == shift:
			return
		
		self.shift = shift
		if self.shift:
			self.ShowFL()
		else:
			self.ShowPN()
		
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
			
		self.BoardSet(evt.slot)

	def BoardSet(self, id, slot=0):
		self.bid = id
		if self.application.cache.messages.has_key(self.bid):
			messages = self.application.cache.messages[self.bid]
		else:
			messages = []

		# Figure out the first non-filter message
		found = slot
		for i in range(slot, len(messages)):
			message = messages[i]
			if self.filtered > Set(message.types):
				continue
			else:
				found = i
				break

		# Set that message as the current
		self.MessageSet(found)
	
	def MessageSet(self, slot):
		if self.application.cache.messages.has_key(self.bid):
			messages = self.application.cache.messages[self.bid]
		else:
			messages = []

		if slot >= len(messages) or slot < 0:
			self.slot = -1
		else:
			self.slot = slot
			
		if self.slot == -1:
			# Is it because we filtered the messages?
			if len(messages) == 0:
				message_subject = _("No messages")
				message_body = self.html_nomessage
			else:
				message_subject = _("All filtered")
				message_body = self.html_allfiltered
				
			message_filter = False
		else:
			message = messages[self.slot]

			if self.filtered > Set(message.types):
				html = self.html_filtered
				message_filter = True
			else:
				html = self.html_message
				message_filter = False
				
			message_subject = message.subject
			message_body = html % message.__dict__

		self.filter.SetValue(message_filter)
		self.titletext.SetLabel(message_subject)
		self.counter.SetLabel(_("%i of %i") % (self.slot+1, len(messages)))
		self.html.SetPage(message_body)

	def MessageFirst(self, evt=None):
		self.slot = -1
		self.MessageNext()

	def MessageNext(self, evt=None):
		print "Going to next message..."
		messages = self.application.cache.messages[self.bid]

		# Find next non-filter message
		slot = self.slot
		for i in range(slot+1, len(messages)):
			message = messages[i]
			if self.filtered > Set(message.types):
				print "Slot %i filtered" % i
				continue
			else:
				print "Using %i" % i
				slot = i
				break

		# Set that message as the current
		self.MessageSet(slot)
	
	def MessageLast(self, evt=None):
		self.slot = len(self.application.cache.messages[self.bid])
		self.MessagePrev()

	def MessagePrev(self, evt=None):
		print "Going to previous message..."
		messages = self.application.cache.messages[self.bid]

		# Find next non-filter message
		slot = self.slot
		for i in range(slot-1, -1, -1):
			message = messages[i]
			if self.filtered > Set(message.types):
				continue
			else:
				slot = i
				break

		# Set that message as the current
		self.MessageSet(slot)
		
	def MessageDelete(self, evt=None):
		# Get the current slot
		slot = self.slot

		if slot == -1:
			return

		# Tell everyone about the change
		self.application.Post(self.application.cache.CacheDirtyEvent("messages", "remove", self.bid, slot, None))

	def MessageGoto(self, slot):
		messages = self.application.cache.messages[self.bid]
		self.MessageSet(slot-1)

	def MessageNew(self, evt=None):
		pass
	
	def MessageFilter(self):
		pass
