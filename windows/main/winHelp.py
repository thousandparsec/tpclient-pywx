"""\
This module contains the System window. The System window displays all objects
at this current location and "quick" details about them.
"""

# Python imports
from types import TupleType
from copy import deepcopy

# wxPython imports
import wx

# Local imports
from windows.winBase import winReportXRC, ShiftMixIn
from windows.xrc.winHelp import winHelpBase

# Show the universe
class winHelp(winReportXRC, winHelpBase):
	title = _("Help")
	
	def __init__(self, application, parent):
		winHelpBase.__init__(self, parent)
		winReportXRC.__init__(self, application, parent)

		self.Message.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnLinkEvent)

	def OnLinkEvent(self, evt):
		link = evt.GetLinkInfo().GetHref()
		from extra.Opener import open

		protocol, url = link.split('://')
		if protocol == "local":
			if url == "serverbrowser":
				self.application.gui.Show(self.application.gui.servers)
		else:
			open(link)

		self.OnClose(None)

	def Show(self, show=True):
		if show:
			self.CenterOnParent()
			winReportXRC.Show(self)
		else:
			self.Hide()

	def OnClose(self, evt):
		self.Hide()

	def SetMessage(self, subject, body):
		self.Subject.SetLabel(_(subject))
		self.Message.SetPage(_(body))

	message_NoObjects_Subject = _("Warning - No Objects...")
	message_NoObjects_Body    = _("""
<p>
It appears that you do not own any objects. This may be for a number of
reasons:
</p>
<ul>
	<li>You have logged in as a guest user.
	<p>
		On most servers guest users can only login and view the universe. They
own no objects and can not issue orders. This is good to checkout what the
Universe is like, but not if you actually want to play the game.
	</p><p>
		Most servers allow you to create accounts right from this client! This
can be done by clicking "Find" on the Login window to bring up the 
server browser. <a href="local://serverbrowser">(Open server browser window.)</a>
	</p><br /></li>
	<li>You have been defeated.
	<p>
		If you have not logged in for a long time, all your objects may have
been conquered or destroyed. Some servers may let you create a new account and
start again.
	</p><br /></li>
	<li>There is a problem.
	<p>
		There could be a bug in some of the software, if you are sure neither
of the two cases above are correct please report it 
<a href="http://sourceforge.net/tracker/?func=add&group_id=132078&atid=723099">here</a>.
	</p></li>
</ul>
""")
 
