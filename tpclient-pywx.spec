import glob
extra = glob.glob("./code/tp/netlib/objects/*Extra/*.py")
a = Analysis([
				os.path.join(HOMEPATH,'support/_mountzlib.py'),
				'./code/tpclient-pywx/main.py'
			] + extra,
             pathex=['/home/tim/Desktop/Downloads/installer', './code', './code/tp/netlib'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts  + [('v', '', 'OPTION')],
          exclude_binaries=1,
          name='buildtpclient-pywx/tpclient-pywx',
          debug=1,
          strip=1,
          upx=1,
          console=1 )
data = Tree("./code/tpclient-pywx/graphics", "graphics/", excludes=("CVS",))
bin = a.binaries - (('_tkinter', 'EXTENSION'), ('readline', 'EXTENSION'))

print "Finding extra depends,"
import os
rest = []
oldlength, newlength = -1, 0
while oldlength != newlength:
	oldlength = len(rest)
	
	for name, file, type in bin:
		print "For %s ." % name,
		deps = os.popen("ldd %s | grep lib | sed -e's/.*lib/lib/' -e's/ (.*$//' | sort | uniq" % file, "r").read()
		deps = deps.split('\n')[:-1]

		for dep in deps:
			print "\b.",
			location = os.popen("whereis %s | sed -e's/.*: //' -e's| /.*$||'" % dep).read().strip()
			if not (dep, location, 'BINARY') in rest:
				print "\n\tFound %s " % dep,
				rest.append((dep, location, 'BINARY'))

		print

	bin = bin + rest
	newlength = len(rest)


bin = bin - ( 
	("lib-2.0.so.0", "BINARY"),
	("lib/ld-linux.so.2", 'BINARY'),
	("libc.so.6", 'BINARY'), 
	("/lib/tls/libc-2.3.2.so", "BINARY"), 
	("libgcc_s.so.1", 'BINARY'),
	('libstdc++.so.5', 'BINARY'),
	("libX11.so.6", "BINARY"), 
	("libXcursor.so.1", 'BINARY'),
	("libXext.so.6", "BINARY"), 
	("libXft.so.2", 'BINARY'),
	("libXi.so.6", 'BINARY'), 
	("libXrandr.so.2", "BINARY"), 
	("libXrender.so.1", 'BINARY'),
	("libdl.so.2", 'BINARY'), 
	("libpthread.so.0", 'BINARY'), 
	("libm.so.6", 'BINARY'),  )

coll = COLLECT( exe,
               bin,
			   data,
               strip=1,
               upx=1,
               name='disttpclient-pywx')
