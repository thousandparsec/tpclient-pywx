#----------------------------------------------------------------------------
# Name:		wxPython.lib.mixins.listctrl
# Purpose:	 Helpful mix-in classes for wxListCtrl
#
# Author:	  Robin Dunn
#
# Created:	 15-May-2001
# RCS-ID:	  $Id: listctrl.py,v 1.2 2003/07/02 10:18:50 mithro Exp $
# Copyright:   (c) 2001 by Total Control Software
# Licence:	 wxWindows license
#----------------------------------------------------------------------------

from wxPython.wx import *
import locale


class wxListCtrlAutoWidthMixin:
	""" A mix-in class that automatically resizes the last column to take up
		the remaining width of the wxListCtrl.

		This causes the wxListCtrl to automatically take up the full width of
		the list, without either a horizontal scroll bar (unless absolutely
		necessary) or empty space to the right of the last column.

		NOTE:	This only works for report-style lists.

		WARNING: If you override the EVT_SIZE event in your wxListCtrl, make
				 sure you call event.Skip() to ensure that the mixin's
				 _OnResize method is called.

		This mix-in class was written by Erik Westra <ewestra@wave.co.nz>
	"""
	def __init__(self):
		""" Standard initialiser.
		"""
		self._lastColMinWidth = None

		EVT_SIZE(self, self._onResize)
		EVT_LIST_COL_END_DRAG(self, self.GetId(), self._onResize)


	def resizeLastColumn(self, minWidth):
		""" Resize the last column appropriately.

			If the list's columns are too wide to fit within the window, we use
			a horizontal scrollbar.  Otherwise, we expand the right-most column
			to take up the remaining free space in the list.

			This method is called automatically when the wxListCtrl is resized;
			you can also call it yourself whenever you want the last column to
			be resized appropriately (eg, when adding, removing or resizing
			columns).

			'minWidth' is the preferred minimum width for the last column.
		"""
		self._lastColMinWidth = minWidth
		self._doResize()

	# =====================
	# == Private Methods ==
	# =====================

	def _onResize(self, event):
		""" Respond to the wxListCtrl being resized.

			We automatically resize the last column in the list.
		"""
		try:
			wxCallAfter(self._doResize)
			event.Skip()
		except:
			event.Skip()
			self._doResize()


	def _doResize(self):
		""" Resize the last column as appropriate.

			If the list's columns are too wide to fit within the window, we use
			a horizontal scrollbar.  Otherwise, we expand the right-most column
			to take up the remaining free space in the list.

			We remember the current size of the last column, before resizing,
			as the preferred minimum width if we haven't previously been given
			or calculated a minimum width.  This ensure that repeated calls to
			_doResize() don't cause the last column to size itself too large.
		"""
		numCols = self.GetColumnCount()
		if numCols == 0: return # Nothing to resize.

		if self._lastColMinWidth == None:
			self._lastColMinWidth = self.GetColumnWidth(numCols - 1)

		# We're showing the vertical scrollbar -> allow for scrollbar width
		# NOTE: on GTK, the scrollbar is included in the client size, but on
		# Windows it is not included
		listWidth = self.GetClientSize().width
		if wxPlatform != '__WXMSW__':
			if self.GetItemCount() > self.GetCountPerPage():
				scrollWidth = wxSystemSettings_GetSystemMetric(wxSYS_VSCROLL_X)
				listWidth = listWidth - scrollWidth

		totColWidth = 0 # Width of all columns except last one.
		for col in range(numCols-1):
			totColWidth = totColWidth + self.GetColumnWidth(col)

		lastColWidth = self.GetColumnWidth(numCols - 1)

		if totColWidth + self._lastColMinWidth > listWidth:
			# We haven't got the width to show the last column at its minimum
			# width -> set it to its minimum width and allow the horizontal
			# scrollbar to show.
			self.SetColumnWidth(numCols-1, self._lastColMinWidth)
			return

		# Resize the last column to take up the remaining available space.

		self.SetColumnWidth(numCols-1, listWidth - totColWidth)
