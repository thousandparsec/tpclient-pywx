"""\
This module contains the message window, it displays all the ingame messages and
lets the player filter out unimportant messages.

Messages are displayed using basic HTML.
"""

from copy import deepcopy

from winBase import winBase

from wxPython.wx import *
from wxPython.lib.anchors import LayoutAnchors
from wxPython.html import *

#from common.message import Message

class wxMessage: #(Message):

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
	
	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE, message_list=[]):	
		winBase.__init__(self, application, parent, pos, size, style|wxTAB_TRAVERSAL)

		font = wxFont(8, wxDEFAULT, wxNORMAL, wxNORMAL)

		panel = wxPanel(self, -1)
		panel.SetConstraints(LayoutAnchors(self, 1, 1, 1, 1))
		self.obj = {}

		item0 = wxFlexGridSizer( 0, 1, 0, 0 )
		item0.AddGrowableCol( 0 )
		item0.AddGrowableRow( 1 )

		item1 = wxFlexGridSizer( 0, 3, 0, 0 )
		item1.AddGrowableCol( 0 )
		item1.AddGrowableCol( 1 )
		item1.AddGrowableCol( 2 )

		item2 = wxCheckBox( panel, MESSAGE_FILTER, "Filter", wxDefaultPosition, wxDefaultSize, 0 )
		item2.SetFont(font)
		item1.AddWindow( item2, 0, wxALIGN_CENTER_VERTICAL|wxALL, 1 )

		item3 = wxStaticText( panel, MESSAGE_TITLE, "Title", wxDefaultPosition, wxDefaultSize, wxALIGN_CENTRE )
		item3.SetFont(font)
		item1.AddWindow( item3, 0, wxGROW|wxALIGN_CENTRE|wxALL, 1 )

		self.obj['title'] = item3

		item4 = wxStaticText( panel, MESSAGE_ID, "# of #", wxDefaultPosition, wxDefaultSize, 0 )
		item4.SetFont(font)
		item1.AddWindow( item4, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 1 )

		self.obj['counter'] = item4

		item0.AddSizer( item1, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 1 )

		item5 = wxFlexGridSizer( 0, 2, 0, 0 )
		item5.AddGrowableCol( 0 )
		item5.AddGrowableRow( 0 )

		# This is the main HTML display!
		item6 = wxHtmlWindow(panel, MESSAGE_HTML, wxDefaultPosition, wxSize(200,160))
		item5.AddWindow( item6, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 1 )

		self.html = item6
		self.html.SetFonts("Swiss", "Courier", [6, 8, 10, 12, 14, 16, 18])
		self.html.SetPage(self.nomessage)

		item7 = wxBoxSizer( wxVERTICAL )

		item8 = wxButton( panel, MESSAGE_PREV, "Prev", wxDefaultPosition, wxDefaultSize, 0 )
		item8.SetFont(font)
		item7.AddWindow( item8, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 1 )

		item9 = wxButton( panel, MESSAGE_GOTO, "Goto", wxDefaultPosition, wxDefaultSize, 0 )
		item9.SetFont(font)
		item7.AddWindow( item9, 0, wxALIGN_CENTRE|wxALL, 1 )

		item10 = wxButton( panel, MESSAGE_NEXT, "Next", wxDefaultPosition, wxDefaultSize, 0 )
		item10.SetFont(font)
		item7.AddWindow( item10, 0, wxALIGN_CENTRE|wxALL, 1 )

		item11 = wxStaticLine( panel, MESSAGE_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
		item11.Enable(false)
		item7.AddWindow( item11, 0, wxALIGN_CENTRE|wxALL, 1 )

		item12 = wxButton( panel, MESSAGE_NEW, "New", wxDefaultPosition, wxDefaultSize, 0 )
		item12.SetFont(font)
		item7.AddWindow( item12, 0, wxALIGN_CENTRE|wxALL, 1 )

		item13 = wxButton( panel, MESSAGE_DEL, "Delete", wxDefaultPosition, wxDefaultSize, 0 )
		item13.SetFont(font)
		item7.AddWindow( item13, 0, wxALIGN_CENTRE|wxALL, 1 )

		item5.AddSizer( item7, 0, wxGROW|wxALIGN_RIGHT|wxALL, 1 )

		item0.AddSizer( item5, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 1 )

		panel.SetAutoLayout( true )
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
	</html>
	"""

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
	</html>
	"""

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
			<td>You have recived no messages this turn!<br><br>
			Actually if you didn't recive any messages it most proberly
			means that your results file is missing so your client
			couldn't load it. Check that you have a results file and
			reload/restart the client.
			</td>
		  </tr>
		 </table>
	</center>
	</body>
	</html>
	"""

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
	</html>
	"""

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
