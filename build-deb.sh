#! /bin/sh

# Reset the tree to the checkout
cg-reset
cg-clean -d -x
#cg-restore -f ./tp/netlib/version.py

# Update to the latest version
cg-update

# Update the debian changelog
cd debian; ./update-debian-changelog; cd ..

# Build the deb package
dpkg-buildpackage -us -uc -b -rfakeroot

# Reset the tree to the checkout
cg-reset
cg-clean -d -x
