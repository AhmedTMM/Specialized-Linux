#!/bin/bash
if [ $# -eq 0 ]
  then
    echo "No arguments supplied not cool man try --help"
fi
if [ $1 == "--help" ]
  then
	echo "--install (PackageName)	- This installs the package."
	echo "--sync			- This syncs your computer to the database."
fi
if [ $1 == "--install" ]
  then
    echo "Starting install"
    isitthere=$(cat /etc/spec/repos/spec/$2 | grep "No such file or directory")
    if [ -z "isitthere" ]
          then
	  echo "this doesnt exist you bafoon"
    else
    #Dependency part of this
    export depend1=$(grep -oP "DEPENDENCEYS=\K.*" /etc/spec/repos/spec/$2)
    depend=( $depend1 )
    echo ${depend[@]}
    echo "Depenceys are ${depend[*]}"
   if [ ! ${#depend[@]} -eq 0 ]
	then
   for i in 0 .. ${#depend[@]}
	do
        echo $i
        mkdir /tmp/spec && mkdir /tmp/spec/work
	cd /tmp/spec/work
        echo ${depend[i]}
	spec --install ${depend[i]}
	$i += 1
	echo $i
	done
    else
    echo "Installing $2 looking up right now"
    grep -oP "DESC=\K.*" /etc/spec/repos/spec/$2
    echo "Installing that right now"
    linkgit=$(grep -oP "INSTALLGIT=\K.*" /etc/spec/repos/spec/$2)
    linkwget=$(grep -oP "INSTALLWGET=\K.*" /etc/spec/repos/spec/$2)
    cd /tmp/spec/work
    wget -O /tmp/spec/work/$2 $linkwget
    git clone $linkgit $2
    cd $2
    if [ -z "$configure" ]
        then
	bash autogen.sh
	bash configure
        make $USE $MAKEOPTS
        make install
    else
    bash make $USE $MAKEOPTS
    bash make install
fi
fi
fi
fi
if [ $1 == "--sync" ]
  then
    echo "Syncing with ahmed repository"
    cd /etc/spec/repos
    rm -rf spec
    git clone https://github.com/AhmedTMM/spec.git
fi
