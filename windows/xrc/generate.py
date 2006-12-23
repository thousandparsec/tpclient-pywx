# This script generates boilerplate classes out of an XRC resource file.
# For each top-level windows (Panel, Frame or Dialog) a class is generated
# and all the controls become attributes of the class.

import sys
import re
import os
from xml.dom import minidom

# --------------------------- Template definitions --------------------------
fileHeaderTemplate = """\
# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers
"""

classDeclarationTemplate = """\
class %(windowName)sBase:
	xrc = '%(fileName)s'

	def PreCreate(self, pre):
		\"\"\" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle().\"\"\"
		pass

	def __init__(self, parent, *args, **kw):
		\"\"\" Pass an initialized wx.xrc.XmlResource into res \"\"\"
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Figure out what Frame class is actually our base...
		bases = set()
		def findbases(klass, set):
			for base in klass.__bases__:
				set.add(base)
				findbases(base, set)
		findbases(self.__class__, bases)

		for base in bases:
			if base.__name__.endswith("Frame"):
				break
		
		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = getattr(wx, "Pre%%s" %% base.__name__)()
		res.LoadOnFrame(pre, parent, "%(windowName)s")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls"""

IDmap = {
	"wxID_CANCEL":		"Cancel",
	"wxID_SAVE":		"Save",
	"wxID_SAVEAS":		"SaveAs",
	"wxID_NEW":			"New",
	"wxID_OK":			"Okay",
	"wxID_FIND":		"Find",
	"wxID_REFRESH":		"Refresh",
	"wxID_PREFERENCES":	"Config",
}

Template_Default = """\
		self.%(controlName)s = XRCCTRL(self, "%(controlID)s")"""
Template_Button = """\
		self.%(controlName)s = XRCCTRL(self, "%(controlID)s")
		if hasattr(self, "On%(controlName)s"):
			self.Bind(wx.EVT_BUTTON, self.On%(controlName)s, self.%(controlName)s)
"""
Template_ToggleButton = """\
		self.%(controlName)s = XRCCTRL(self, "%(controlID)s")
		if hasattr(self, "On%(controlName)s"):
			self.Bind(wx.EVT_TOGGLEBUTTON, self.On%(controlName)s, self.%(controlName)s)
"""
Template_BitmapButton = Template_Button

def Generate_wxFrame(xrcFile, topWindow, outFile):
	fileName = os.path.basename(xrcFile.name)

	windowClass = topWindow.getAttribute("subclass")
	if len(windowClass) == 0:
		windowClass = topWindow.getAttribute("class")
	windowClass = re.sub("^wx", "wx.", windowClass)

	windowName = topWindow.getAttribute("name")
	print "'%s' '%s'"% (windowClass, windowName)
	print >> outFile, classDeclarationTemplate % locals()
	
	eventFunctions = [] # a list to store the code for the event functions

	# Generate a variable for each control, and standard event handlers
	# for standard controls.
	for control in topWindow.getElementsByTagName("object"):
		controlClass = control.getAttribute("class")
		controlClass = re.sub("^wx", "wx.", controlClass)
		controlName = control.getAttribute("name")
		# Ignore anything which is still got a wx name...
		if controlName in IDmap:
			controlID = controlName
			controlName = IDmap[controlName]
		else:
			controlID = controlName

		if "wx" in controlName:
			continue
		if controlName != "" and controlClass != "":
			print controlName, controlClass
			try:
				template = globals()["Template_%s" % controlClass.replace('wx.', '')]
			except KeyError:
				template = globals()["Template_Default"]

			print >> outFile, template % locals()

	print >> outFile
	print >> outFile, "\n".join(eventFunctions)
	print eventFunctions

#Generate_wxWizard = Generate_wxDialog

# ------------------------- GeneratePythonForXRC ----------------------------
def GeneratePython(xrcFile, outFile):
	xmldoc = minidom.parse(xrcFile)
	resource = xmldoc.childNodes[0]
	topWindows = [e for e in resource.childNodes
				  if e.nodeType == e.ELEMENT_NODE and e.tagName == "object"]
	print topWindows
	print >> outFile, fileHeaderTemplate

	# Generate a class for each top-window object (Frame, Panel, Dialog, etc.)
	for topWindow in topWindows:

		# Figure out if this is a Panel, Frame or Wizard
		windowClass = topWindow.getAttribute("class")
		globals()["Generate_"+windowClass](xrcFile, topWindow, outFile)

# --------------------- Main ----------------

def Usage():
	print """
xrcpy -- Python boilerplate code generator for XRC resources.

Usage : python pyxrc.py <resource.xrc>

The Python code is printed to the standard output.
"""

def main():
	if len(sys.argv) != 2:
		Usage()
	else:
		inFilename = sys.argv[1]
		outFilename = os.path.splitext(inFilename)[0] + ".py"

		try:
			inStream = file(inFilename)
			try:
				outStream = file(outFilename, "w")
			except IOError:
				print >> sys.stderr, "Can't open '%s'!" % outFilename
			else:
				GeneratePython(inStream, outStream)
				print "Result stored in %s." % outFilename
		except IOError:
			print >> sys.stderr, "Can't open '%s'!" % inFilename


if __name__  == "__main__":
	main()
