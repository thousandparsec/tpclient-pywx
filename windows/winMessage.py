"""\
This module contains the message window, it displays all the ingame messages and
lets the player filter out unimportant messages.

Messages are displayed using basic HTML.
"""

# Python Imports
from copy import deepcopy

# wxPython Imports
import wx
import wx.html
import wx.lib.anchors

# Local Imports
from winBase import *

class wxMessage:

	def render(self):
		# Render the message, first you need to convert the <link> to wx objects

		# Then return the real HTML stuff
		pass

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
	title = "Messages"
	
	def __init__(self, application, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, message_list=[]):
		winBase.__init__(self, application, parent, pos, size, style|wx.TAB_TRAVERSAL)

		panel = wx.Panel(self, -1)
		panel.SetConstraints(wx.lib.anchors.LayoutAnchors(self, 1, 1, 1, 1))
		self.obj = {}

		item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
		item0.AddGrowableCol( 0 )
		item0.AddGrowableRow( 1 )

		item1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		item1.AddGrowableCol( 0 )
		item1.AddGrowableCol( 1 )
		item1.AddGrowableCol( 2 )

		item2 = wx.CheckBox( panel, MESSAGE_FILTER, "Filter", wx.DefaultPosition, wx.DefaultSize, 0 )
		item2.SetFont(wx.local.normalFont)
		item1.AddWindow( item2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )

		item3 = wx.StaticText( panel, MESSAGE_TITLE, "Title", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		item3.SetFont(wx.local.normalFont)
		item1.AddWindow( item3, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		self.obj['title'] = item3

		item4 = wx.StaticText( panel, MESSAGE_ID, "# of #", wx.DefaultPosition, wx.DefaultSize, 0 )
		item4.SetFont(wx.local.normalFont)
		item1.AddWindow( item4, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )

		self.obj['counter'] = item4

		item0.AddSizer( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )

		item5 = wx.FlexGridSizer( 0, 2, 0, 0 )
		item5.AddGrowableCol( 0 )
		item5.AddGrowableRow( 0 )

		# This is the main HTML display!
		item6 = wx.html.HtmlWindow(panel, MESSAGE_HTML, wx.DefaultPosition, wx.Size(200,10))
		item5.AddWindow( item6, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 1 )

		self.html = item6
		self.html.SetFonts("Swiss", "Courier", [4, 6, 8, 10, 12, 14, 16])
		self.html.SetPage(self.nomessage)

		item7 = wx.BoxSizer( wx.VERTICAL )

		button_size = wx.Size(50,20)

		item8 = wx.Button( panel, MESSAGE_PREV, "Prev", wx.DefaultPosition, button_size, 0 )
		item8.SetFont(wx.local.normalFont)
		item7.AddWindow( item8, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )

		item9 = wx.Button( panel, MESSAGE_GOTO, "Goto", wx.DefaultPosition, button_size, 0 )
		item9.SetFont(wx.local.normalFont)
		item7.AddWindow( item9, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		item10 = wx.Button( panel, MESSAGE_NEXT, "Next", wx.DefaultPosition, button_size, 0 )
		item10.SetFont(wx.local.normalFont)
		item7.AddWindow( item10, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		item11 = wx.StaticLine( panel, MESSAGE_LINE, wx.DefaultPosition, wx.Size(20,-1), wx.LI_HORIZONTAL )
		item11.Enable(False)
		item7.AddWindow( item11, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		item12 = wx.Button( panel, MESSAGE_NEW, "New", wx.DefaultPosition, button_size, 0 )
		item12.SetFont(wx.local.normalFont)
		item7.AddWindow( item12, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		item13 = wx.Button( panel, MESSAGE_DEL, "Delete", wx.DefaultPosition, button_size, 0 )
		item13.SetFont(wx.local.normalFont)
		item7.AddWindow( item13, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		item5.AddSizer( item7, 0, wx.GROW|wx.ALIGN_RIGHT|wx.ALL, 1 )

		item0.AddSizer( item5, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 1 )

		panel.SetAutoLayout(True)
		panel.SetSizer( item0 )
		
		item0.Fit( panel )
		item0.SetSizeHints( panel )
		
		self.SetSize(size)
		self.SetPosition(pos)

		# Contains the messages
		self.messages = []
		# The current message
		self.current = 0
		# Contains the message types to be filtered
		self.filter = []

		self.MessageSet([])

	filtered = """\
<html>
<body>
<center>
	<table COLS=1 WIDTH="100%" BACKGROUND="./graphics/filtered.png">
		<tr>
			<td><b>From:</b> %s</td>
		</tr>
		<tr>
			<td><b>Subject:</b> %s</td>
		</tr>
		<tr>
			<td>Related: %s</td>
		</tr>
		<tr>
			<td>%s</td>
		</tr>
	</table>
</center>
</body>
</html>"""

	message = """\
<html>
<body>
<center>
	<table COLS=1 WIDTH="100%">
		<tr>
			<td><b>From:</b> %s</td>
		</tr>
		<tr>
			<td><b>Subject:</b> %s</td>
		</tr>
		<tr>
			<td>Related: %s</td>
		</tr>
		<tr>
			<td>%s</td>
		</tr>
	</table>
</center>
</body>
</html>"""

	nomessage = """\
<html>
<body>
<center>
	<table COLS=1 WIDTH="100%">
		<tr>
			<td><b>From:</b> SYSTEM</td>
		</tr>
		<tr>
			<td><b>Subject:</b> You are unloved!
		</tr>
		<tr>
			<td>
			You have recived no messages this turn!<br><br>
			Actually if you didn't recive any messages it most proberly
			means that your results file is missing so your client
			couldn't load it. Check that you have a results file and
			reload/restart the client.
			</td>
		</tr>
	 </table>
</center>
</body>
</html>"""

	allfiltered = """\
<html>
<body>
<center>
	<table COLS=1 WIDTH="100%">
		<tr>
			<td><b>From:</b> SYSTEM</td>
		</tr>
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

	def MessageSet(self, list):

		# Updates the bits and pieces
		self.messages = deepcopy(list)

		# If no messages display this text
		if len(self.messages) == 0:
			self.html.SetPage(self.nomessage)
			self.obj['title'].SetLabel("No messages")
			self.obj['counter'].SetLabel("%i of %i" % (0, 0))
			return

		# Else get a message
		count = 0
		for message in self.messages:
			if message.type not in self.filter:
				self.current = count
				# FIXME: Set the title to something intresting
				self.obj['title'].SetLabel("")
				self.obj['counter'].SetLabel("%i of %i" % (self.current, len(self.messages)))
				self.html.SetPage(self.message % message.render())
				return
			count += 1

		self.html.SetPage(self.allfiltered)
		return

	def MessageNext(self):
		# Check we arn't at the last message
		if self.current >= len(self.messages):
			self.current = len(self.messages)-1
			return

		# Cycle through message list until we get to our one
		count = 0
		for message in self.messages[self.current:]:
			if message.type not in self.filter:
				self.current += count
				self.obj['counter'].SetLabel("%i of %i" % (self.current, len(self.messages)))
				self.html.SetPage(self.messages % message.render())
				return
			count += 1
		
	def MessagePrev(self):
		# Check we arn't at the last message
		if self.current <= 0:
			self.current = len(self.messages)-1
			return
		
		# Cycle through message list until we get to our one
		count = self.current
		while count >= 0:
			if self.messages[count].type not in self.filter:
				self.current = count
				self.html.SetPage(self.message % self.messages[count].render())
				self.obj['counter'].SetLabel("%i of %i" % (self.current, len(self.messages)))
				return
			count -= 1
		
	def MessageGoto(self, no):
		if no > len(self.messages) or no < 0:
			return

		if self.message.type in self.filter:
			html = self.filtered
		else:
			html = self.message

		self.current = no
		self.obj['counter'].SetLabel("%i of %i" % (self.current, len(self.messages)))
		self.html.SetPage(html % self.messages[no].render())

	def MessageFilter(self):
		pass
