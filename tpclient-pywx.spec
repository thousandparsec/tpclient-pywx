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
coll = COLLECT( exe,
               a.binaries,
			   data,
               strip=1,
               upx=0,
               name='disttpclient-pywx')
