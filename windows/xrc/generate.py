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

# Local imports
from requirements import location
"""

frameTemplate = """\
class %(windowName)sBase:
	\"\"\"\\
Unlike a normal XRC generated class, this is a not a full class but a MixIn.
Any class which uses this as a base must also inherit from a proper wx object
such as the wx.Frame class.

This is so that a the same XRC can be used for both MDI and non-MDI frames.
\"\"\"

	xrc = os.path.join(location(), "windows", "xrc", '%(fileName)s')

	def PreCreate(self, pre):
		\"\"\" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle().\"\"\"
		pass

	def __init__(self, parent, *args, **kw):
		\"\"\" Pass an initialized wx.xrc.XmlResource into res \"\"\"
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Figure out what Frame class (MDI, MiniFrame, etc) is actually our base...
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

panelTemplate = """\
class %(windowName)sBase(wx.Panel):
	xrc = os.path.join(location(), "windows", "xrc", '%(fileName)s')

	def PreCreate(self, pre):
		\"\"\" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle().\"\"\"
		pass

	def __init__(self, parent, *args, **kw):
		\"\"\" Pass an initialized wx.xrc.XmlResource into res \"\"\"
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.PrePanel()
		res.LoadOnPanel(pre, parent, "%(windowName)s")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls"""

wizardTemplate = """\
class %(windowName)sBase(wx.wizard.Wizard):
	xrc = os.path.join(location(), "windows", "xrc", '%(fileName)s')

	def PreCreate(self, pre):
		\"\"\" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle().\"\"\"
		pass

	def __init__(self, parent, *args, **kw):
		\"\"\" Pass an initialized wx.xrc.XmlResource into res \"\"\"
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.wizard.PreWizard()
		res.LoadOnObject(pre, parent, 'SinglePlayerWizard', 'wxWizard')
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls"""

IDmap = {
	"wxID_CANCEL":		"Cancel",
	"wxID_CLOSE":		"Close",
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
Template_CheckBox = """\
		self.%(controlName)s = XRCCTRL(self, "%(controlID)s")
		if hasattr(self, "On%(controlName)s"):
			self.Bind(wx.EVT_CHECKBOX, self.On%(controlName)s, self.%(controlName)s)
"""

Template_ToggleButton = """\
		self.%(controlName)s = XRCCTRL(self, "%(controlID)s")
		if hasattr(self, "On%(controlName)s"):
			self.Bind(wx.EVT_TOGGLEBUTTON, self.On%(controlName)s, self.%(controlName)s)
"""
Template_BitmapButton = Template_Button
Template_ComboBox = """\
		self.%(controlName)s = XRCCTRL(self, "%(controlID)s")
		if hasattr(self, "On%(controlName)s"):
			self.Bind(wx.EVT_COMBOBOX, self.On%(controlName)s, self.%(controlName)s)
			self.Bind(wx.EVT_TEXT_ENTER, self.On%(controlName)s, self.%(controlName)s)
		if hasattr(self, "OnDirty%(controlName)s"):
			self.Bind(wx.EVT_TEXT, self.On%(controlName)s, self.%(controlName)s)
"""
Template_Choice = """\
		self.%(controlName)s = XRCCTRL(self, "%(controlID)s")
		if hasattr(self, "On%(controlName)s"):
			self.%(controlName)s.Bind(wx.EVT_CHOICE, self.On%(controlName)s)
"""

def Generate_wxFrame(xrcFile, topWindow, outFile):
	fileName = os.path.basename(xrcFile.name)

	windowClass = topWindow.getAttribute("subclass")
	if len(windowClass) == 0:
		windowClass = topWindow.getAttribute("class")
	windowClass = re.sub("^wx", "wx.", windowClass)

	windowName = topWindow.getAttribute("name")
	print "'%s' is a '%s'"% (windowName, windowClass)
	print >> outFile, frameTemplate % locals()
	
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
			print '\t', controlName, (3-(len(controlName)+1)/8)*'\t', "is a", controlClass
			try:
				template = globals()["Template_%s" % controlClass.replace('wx.', '')]
			except KeyError:
				template = globals()["Template_Default"]

			print >> outFile, template % locals()

	print >> outFile
	print >> outFile, "\n".join(eventFunctions)

def Generate_wxPanel(xrcFile, topWindow, outFile):
	fileName = os.path.basename(xrcFile.name)

	windowClass = topWindow.getAttribute("subclass")
	if len(windowClass) == 0:
		windowClass = topWindow.getAttribute("class")
	windowClass = re.sub("^wx", "wx.", windowClass)

	windowName = topWindow.getAttribute("name")
	print "'%s' is a '%s'"% (windowName, windowClass)
	print >> outFile, panelTemplate % locals()
	
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
			print '\t', controlName, (3-(len(controlName)+1)/8)*'\t', "is a", controlClass
			try:
				template = globals()["Template_%s" % controlClass.replace('wx.', '')]
			except KeyError:
				template = globals()["Template_Default"]

			print >> outFile, template % locals()

	print >> outFile
	print >> outFile, "\n".join(eventFunctions)

def Generate_wxWizard(xrcFile, topWindow, outFile):
	fileName = os.path.basename(xrcFile.name)

	windowClass = topWindow.getAttribute("subclass")
	if len(windowClass) == 0:
		windowClass = topWindow.getAttribute("class")
	windowClass = re.sub("^wx", "wx.", windowClass)

	windowName = topWindow.getAttribute("name")
	print "'%s' is a '%s'"% (windowName, windowClass)
	print >> outFile, wizardTemplate % locals()
	
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
			print '\t', controlName, (3-(len(controlName)+1)/8)*'\t', "is a", controlClass
			try:
				template = globals()["Template_%s" % controlClass.replace('wx.', '')]
			except KeyError:
				template = globals()["Template_Default"]

			print >> outFile, template % locals()

	print >> outFile
	print >> outFile, "\n".join(eventFunctions)


# ------------------------- GeneratePythonForXRC ----------------------------
def GeneratePython(xrcFile, outFile):
	xmldoc = minidom.parse(xrcFile)
	resource = xmldoc.childNodes[0]
	topWindows = [e for e in resource.childNodes
				  if e.nodeType == e.ELEMENT_NODE and e.tagName == "object"]
	print >> outFile, fileHeaderTemplate

	# Generate a class for each top-window object (Frame, Panel, Dialog, etc.)
	for topWindow in topWindows:
		# Figure out if this is a Panel, Frame or Wizard
		windowClass = topWindow.getAttribute("class")
		windowName  = topWindow.getAttribute("name")

		globals()["Generate_"+windowClass](xrcFile, topWindow, outFile)

# --------------------- Main ----------------

def Usage():
	print """
xrcpy -- Python boilerplate code generator for XRC resources.

Usage : python pyxrc.py <resource.xrc>

The Python code is printed to the standard output.
"""

from wx.tools.pywxrc import XmlResourceCompiler

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

				comp = XmlResourceCompiler()
				comp.MakeGetTextOutput([inFilename], '.translation')

				transStream = file('.translation', 'r')
				outStream.write('def strings():\n')
				outStream.write('\tpass\n')
				outStream.write(transStream.read().replace('_(', '\t_('))
				transStream.close()

				os.unlink('.translation')

				print "Result stored in %s." % outFilename
		except IOError:
			print >> sys.stderr, "Can't open '%s'!" % inFilename
		except KeyError, e:
			print >> sys.stderr, "There was an error outputting .py file for '%s'" % inFilename
			print >> sys.stderr, "No such key %s" % e
			os.unlink(outFilename)
		print >> sys.stderr


if __name__  == "__main__":
	main()
