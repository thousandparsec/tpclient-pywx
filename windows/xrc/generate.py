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

import wx
from wx.xrc import *
"""

classDeclarationTemplate = """\
from winBase import %(windowClass)s

class %(windowName)sBase(%(windowClass)s):
	xrc = '%(fileName)s'

	def OnInit(self):
		\"\"\" This function is called during the class's initialization.
		
		Override it for custom setup (setting additional styles, etc.)\"\"\"
		pass

	def __init__(self, parent, res):
		\"\"\" Pass an initialized wx.xrc.XmlResource into res \"\"\"
		
		res = XmlResource(self.xrc)

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.Pre%(windowClass)s()
		res.LoadOnPanel(pre, parent, "%(windowName)s")
		self.OnInit()
		self.PostCreate(pre)

		# Define variables for the controls"""

controlDeclationTemplate = """\
		self.%(controlName)s = XRCCTRL(self, \"%(controlName)s\")"""

# ------------------------- GeneratePythonForXRC ----------------------------
def GeneratePython(xrcFile, outFile):
	fileName = os.path.basename(xrcFile.name)

	xmldoc = minidom.parse(xrcFile)
	resource = xmldoc.childNodes[0]
	topWindows = [e for e in resource.childNodes
				  if e.nodeType == e.ELEMENT_NODE and e.tagName == "object"]
	print >> outFile, fileHeaderTemplate

	# Generate a class for each top-window object (Frame, Panel, Dialog, etc.)
	for topWindow in topWindows:
		eventFunctions = [] # a list to store the code for the event functions
		windowClass = topWindow.getAttribute("subclass")
		windowClass = re.sub("^wx", "wx.", windowClass)
		windowName = topWindow.getAttribute("name")
		print >> outFile, classDeclarationTemplate % locals()

		# Generate a variable for each control, and standard event handlers
		# for standard controls.
		for control in topWindow.getElementsByTagName("object"):
			controlClass = control.getAttribute("class")
			controlClass = re.sub("^wx", "wx.", controlClass)
			controlName = control.getAttribute("name")
			if controlName != "" and controlClass != "":
				if not "wx" in controlName:
					print >> outFile, controlDeclationTemplate% locals()

		print >> outFile
		print >> outFile, "\n".join(eventFunctions)

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
