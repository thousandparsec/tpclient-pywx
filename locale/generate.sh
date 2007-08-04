#! /bin/sh
cd ..
xgettext -j -L python --from-code utf-8 -o ./locale/tpclient-pywx.pot `find -name \*.py` tpclient-pywx

