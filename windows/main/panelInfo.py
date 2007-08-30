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

try:
	from extra.GIFAnimationCtrl import GIFAnimationCtrl
except ImportError:
	from wx.animate import GIFAnimationCtrl

# Network imports
from tp.netlib.objects.ObjectExtra.Universe import Universe
from tp.netlib.objects.ObjectExtra.Galaxy import Galaxy
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Planet import Planet
from tp.netlib.objects.ObjectExtra.Fleet import Fleet

from windows.xrc.panelInformation import panelInformationBase
class panelInformation(panelInformationBase):
	title = _("Information")

	def __init__(self, application, parent):
		panelInformationBase.__init__(self, parent)

		self.application = application
		self.current = -1

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()
		info.MinSize(self.GetBestSize())
		info.Bottom()
		info.Layer(1)
		return info

	def OnSelectObject(self, evt):
		print "winInfo SelectObject", evt
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
		s = ""
		for key, value in object.__dict__.items():
			if key.startswith("_") or key in \
				('protocol', 'sequence', 'otype', 'length', 'order_types', 'order_number', 'contains'):
				continue

			if key == "ships":
				s += _("Ships: ")
				# FIXME: This is a hack :/
				for t, number in value:
					if self.application.cache.designs.has_key(t):
						design = self.application.cache.designs[t]
						s += "%s %s, " % (number, design.name)
					else:
						print _("Unknown Design id:"), t
						s += "%s %s, " % (number, _("Unknown (type: %s)") % t)
				s = s[:-2] + "\n"
				continue

			if key == "resources":
				s += _("Resources:\n")
				for t, surface, minable, inaccess in value:
					if surface+minable+inaccess == 0:
						continue
					if self.application.cache.resources.has_key(t):
						res = self.application.cache.resources[t]
						s+="\t"
						if surface > 0:
							if len(res.unit_singular) > 0:
								s+=_("%s %s of %s on surface, ") % (surface, \
									[res.unit_singular, res.unit_plural][surface > 1],
									[res.name_singular, res.name_plural][surface > 1])
							else:
								s+=_("%s %s on surface, ") % (surface, [res.name_singular, res.name_plural][surface > 1])

						if minable > 0:
							if len(res.unit_singular) > 0:
								s+=_("%s %s of %s minable, ") % (minable, \
									[res.unit_singular, res.unit_plural][minable > 1],
									[res.name_singular, res.name_plural][minable > 1])
							else:
								s+=_("%s %s minable, ") % (minable, [res.name_singular, res.name_plural][minable > 1])

						if inaccess > 0:
							if len(res.unit_singular) > 0:
								s+=_("%s %s of %s inaccessible, ") % (inaccess, \
									[res.unit_singular, res.unit_plural][inaccess > 1],
									[res.name_singular, res.name_plural][inaccess > 1])
							else:
								s+=_("%s %s inaccessible, ") % (inaccess, [res.name_singular, res.name_plural][inaccess > 1])

						s = s[:-2]+"\n"
					else:
						s+= _("\tUnknown Resource %i, S: %i, M: %i, I: %s\n") % (t, surface, minable, inaccess)
				continue

			key = key.title()
			if type(value) == StringType:
				s += "%s: %s\n" % (key, value)
			elif type(value) in (ListType, TupleType):
				s += "%s: " % (key,)
				for i in value:
					s += "%s, " % (i,)
				s = s[:-2] + "\n"
			else:
				s += "%s: %s\n" % (key, value)

		self.Details.SetValue(s)

