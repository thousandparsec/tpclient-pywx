
release:
	rm -rf dist
	python setup.py sdist --formats=gztar,zip
	cp dist/* ../web/downloads/tpclient-pywx
	cd ../web/downloads/tpclient-pywx ; cvs add *.* ; cvs commit

clean:
	rm -rf dist
	rm -rf build
