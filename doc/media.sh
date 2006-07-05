#! /bin/sh
find media/ -type f | egrep "common-2d|tpclient-pywx" | grep -- "-small" > MEDIA-ALL
cat MEDIA-ALL | grep -v animation > MEDIA-SMALL
diff --old-line-format="%L" --unchanged-line-format= MEDIA-ALL MEDIA-SMALL > MEDIA-LARGE
rm MEDIA-ALL
