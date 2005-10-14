import wx

if wx.Platform == '__WXMSW__':
	winMainDefaultPosition = {(1024, 768): (0,0), }
	winMainDefaultWidth = {(1024, 768): 1024, }
	winMainDefaultShow = {(1024, 768): True, }

	winInfoDefaultPosition = {(1024, 768): (0,0), }
	winInfoDefaultSize = {(1024, 768): (425, 175), }
	winInfoDefaultShow = {(1024, 768): True, }
	
	winOrderDefaultPosition = {(1024, 768): (0, 176), }
	winOrderDefaultSize = {(1024, 768): (213, 327), }
	winOrderDefaultShow = {(1024, 768): True, }
	
	winMessageDefaultPosition = {(1024, 768): (0, 504), }
	winMessageDefaultSize = {(1024, 768): (396, 163), }
	winMessageDefaultShow = {(1024, 768): True, }
	
	winStarmapDefaultPosition = {(1024, 768): (426, 0), }
	winStarmapDefaultSize = {(1024, 768): (600, 523), }
	winStarMapDefaultShow = {(1024, 768): True, }
	
	winSystemDefaultPosition = {(1024, 768): (769, 523), }
	winSystemDefaultSize = {(1024, 768): (257, 218), }
	winSystemDefaultShow = {(1024, 768): True, }
	
	winDesignDefaultPosition = {(1024, 768): (5, 5), }
	winDesignDefaultSize = {(1024, 768): (1000, 700), }
	winDesignDefaultShow = {(1024, 768): False, }
	
elif wx.Platform == '__WXMAC__':
	winMainDefaultPosition = {(1024, 768): (0,38), }
	winMainDefaultWidth = {(1024, 768): 1024, }
	winMainDefaultShow = {(1024, 768): False, }
	
	winInfoDefaultPosition = {(1024, 768): (3,38), }
	winInfoDefaultSize = {(1024, 768): (423, 173), }
	winInfoDefaultShow = {(1024, 768): True, }
	
	winOrderDefaultPosition = {(1024, 768): (62, 229), }
	winOrderDefaultSize = {(1024, 768): (363, 367), }
	winOrderDefaultShow = {(1024, 768): True, }
	
	winMessageDefaultPosition = {(1024, 768): (1032, 38), }
	winMessageDefaultSize = {(1024, 768): (396, 163), }
	winMessageDefaultShow = {(1024, 768): True, }
	
	winStarMapDefaultPosition = {(1024, 768): (426, 38), }
	winStarMapDefaultSize = {(1024, 768): (600, 523), }
	winStarMapDefaultShow = {(1024, 768): True, }
	
	winSystemDefaultPosition = {(1024, 768): (1032, 218), }
	winSystemDefaultSize = {(1024, 768): (257, 218), }
	winSystemDefaultShow = {(1024, 768): True, }
	
	winDesignDefaultPosition = {(1024, 768): (5, 5), }
	winDesignDefaultSize = {(1024, 768): (1000, 700), }
	winDesignDefaultShow = {(1024, 768): False, }
	
else:
	# Create some default Positioning, good for 1024x768 on linux
	winMainDefaultPosition = {(1024, 768): (0,0), }
	winMainDefaultWidth = {(1024, 768): 419, }
	winMainDefaultShow = {(1024, 768): True, }
	
	winInfoDefaultPosition = {(1024, 768): (1,75), }
	winInfoDefaultSize = {(1024, 768): (425, 176), }
	winInfoDefaultShow = {(1024, 768): True, }
	
	winOrderDefaultPosition = {(1024, 768): (1, 251), }
	winOrderDefaultSize = {(1024, 768): (213, 327), }
	winOrderDefaultShow = {(1024, 768): True, }
	
	winMessageDefaultPosition = {(1024, 768): (1, 578), }
	winMessageDefaultSize = {(1024, 768): (396, 163), }
	winMessageDefaultShow = {(1024, 768): True, }
	
	winStarMapDefaultPosition = {(1024, 768): (426, 0), }
	winStarMapDefaultSize = {(1024, 768): (600, 523), }
	winStarMapDefaultShow = {(1024, 768): True, }
	
	winSystemDefaultPosition = {(1024, 768): (769, 523), }
	winSystemDefaultSize = {(1024, 768): (257, 218), }
	winSystemDefaultShow = {(1024, 768): True, }
	
	winDesignDefaultPosition = {(1024, 768): (5, 5), }
	winDesignDefaultSize = {(1024, 768): (1000, 700), }
	winDesignDefaultShow = {(1024, 768): False, }
