#!/bin/bash

# Script to build GradeMan2-deb-file
# insert apropriate version no:
version='dev'

echo '=== building GradeMan2 version '$version' ==='

# altes paket löschen:
rm grademan2_$version.deb

# copy all files to where they are needed:
mkdir -p build
mkdir -p build/grademan2_$version
cp -ru DEBIAN/ build/grademan2_$version/
#mkdir -p build/grademan2_$version/usr/
#mkdir -p build/grademan2_$version/usr/bin/
cp -ru usr/ build/grademan2_$version/
mkdir -p build/grademan2_$version/usr/share/grademan2/
cp -ru ../GradeMan2/* build/grademan2_$version/usr/share/grademan2/
cp -ru ../GradeMan2Tray.py build/grademan2_$version/usr/bin/grademan2
sed -i 's/chdir("GradeMan2")/chdir("\/usr\/share\/grademan2")/' build/grademan2_$version/usr/bin/grademan2
cd build/

# TODO: rm all __pycache__
rm -r grademan2_$version/usr/share/grademan2/__pycache__/
rm -r grademan2_$version/usr/share/grademan2/latex2mathml/__pycache__/
rm -r grademan2_$version/usr/share/grademan2/mdtex2html/__pycache__/
rm -r grademan2_$version/usr/share/grademan2/modules/__pycache__/
rm -r grademan2_$version/usr/share/grademan2/grademan.sqlite3

# set file rights:
#chown -R dirk:dirk grademan2_$version/
chmod -R =0755 grademan2_$version/
chmod -R =0644 grademan2_$version/DEBIAN/*
chmod -R =0755 grademan2_$version/usr/*
chmod -R =0755 grademan2_$version/usr/bin/*
chmod -R =0755 grademan2_$version/usr/bin/grademan2
#chmod -R -x grademan_$version/usr/share/grademan/
#chmod -R =0755 grademan_$version/usr/share/grademan/*.py

# package files:
chmod =0644 grademan2_$version/usr/share/grademan2/latex2mathml/*
chmod =0644 grademan2_$version/usr/share/grademan2/static/*
chmod =0644 grademan2_$version/usr/share/grademan2/templates/*
chmod =0644 grademan2_$version/usr/share/pixmaps/*
chmod =0644 grademan2_$version/usr/share/doc/grademan2/*
chmod =0644 grademan2_$version/usr/share/man/man1/*
chmod =0644 grademan2_$version/usr/share/applications/*
gzip -9 -n grademan2_$version/usr/share/doc/grademan2/changelog
gzip -9 -n grademan2_$version/usr/share/doc/grademan2/readme.txt
gzip -9 -n grademan2_$version/usr/share/man/man1/*

# md5sum-file automatisch erstellen:
#rm grademan2_$version/DEBIAN/md5sums
cd grademan2_$version # TODO: schöner machen
find . -type f ! -regex '.*.hg.*' ! -regex '.*?debian-binary.*' ! -regex '.*?DEBIAN.*' -printf '%P ' | xargs md5sum >DEBIAN/md5sums
chmod -R =0644 DEBIAN/md5sums
cd ..

# paket bauen als fakeroot:
fakeroot dpkg --build grademan2_$version

# aufräumen: Dateien wieder entpacken:
chmod -R =0755 grademan2_$version/
gzip -d grademan2_$version/usr/share/doc/grademan2/changelog
gzip -d grademan2_$version/usr/share/doc/grademan2/readme.txt
gzip -d grademan2_$version/usr/share/man/man1/*
mv grademan2_$version.deb ../
cd ..

# test ob es dem Standart entspricht:
echo "=== Was I successful? I am checking... (no message = OK): ==="
lintian grademan2_$version.deb

echo "=== If all is fine (no messages when testing): congratulations! ==="

read -p "Press enter to remove buildtree and quit"
rm -r build
