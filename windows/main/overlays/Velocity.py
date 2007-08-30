"""\
This overlay displays a line showing where objects may end up based on their
current velocity.
"""
# Python imports
import os
from math import *

import numpy as N

# wxPython imports
import wx
from extra.wxFloatCanvas import FloatCanvas
from extra.wxFloatCanvas.RelativePoint import RelativePoint
from extra.wxFloatCanvas.Icon import Icon

from extra.wxFloatCanvas.NavCanvas import NavCanvas

