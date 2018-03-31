pip3 uninstall estring
git rm -r dist
git rm -r build
git rm -r xdict.egg-info
rm -r dist
rm -r build
rm -r elist.egg-info
git add .
git commit -m "remove old build"
