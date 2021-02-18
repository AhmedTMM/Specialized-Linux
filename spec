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
	install $1
fi
if [ $1 == "--sync" ]
  then
	sync
fi
#Load function to load all the needed variables
load () {
    export FAKEROOT=$()
}
#Install function
install () {
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
	install ${depend[i]}
	$i += 1
	echo $i
	done
    else
    echo "Installing $2 looking up right now"
    grep -oP "DESC=\K.*" /etc/spec/repos/spec/$2
    echo "Installing that right now"
    linkwget=$(grep -oP "INSTALLWGET=\K.*" /etc/spec/repos/spec/$2)
    mkdir /tmp/spec/work
    cd /tmp/spec/work
    wget -O /tmp/spec/work/$2 $linkwget
    cd $2
    bash autogen.sh
    bash configure $OPTIONS $USE --PREFIX=/usr
    bash make $MAKEOPTS
    bash make DESTDIR=$FAKEROOT install
fi
fi
fi    
}
#sync function
sync () {
    echo "Syncing with ahmed repository"
    cd /var/db/spec/repos
    rm -rf spec
    wget https://ahmedserver.ml/repos/spec
}
