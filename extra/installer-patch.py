--- carchive.py.old	2005-03-01 08:37:42.000000000 +1030
+++ carchive.py	2005-02-22 22:14:27.000000000 +1030
@@ -261,3 +261,15 @@
     if flag:
       raise ValueError, "Cannot open compressed archive %s in place"
     return CArchive(self.path, self.pkgstart+dpos, dlen)
+
+  def openEmbeddedZlib(self, name):
+    """Open a CArchive of name NAME embedded within this CArchive."""
+    ndx = self.toc.find(name)
+    if ndx == -1:
+      raise KeyError, "Member '%s' not found in %s" % (name, self.path)
+    (dpos, dlen, ulen, flag, typcd, nm) = self.toc.get(ndx)
+    if flag:
+      raise ValueError, "Cannot open compressed archive %s in place"
+    return archive.ZlibArchive(self.path, self.pkgstart+dpos)
+
+	
