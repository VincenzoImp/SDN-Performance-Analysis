#!/bin/bash

topology="./topologies/topology.py"


usage(){
	echo "usage: run.sh [-f file]"
}


while [ "$1" != "" ]; do
	case $1 in
		-f | --file ) shift
			      topology=$1
			      ;;
		* )  	      usage
			      exit 1

	esac
	shift
done	


sudo python3 $topology
sudo mn -c; clear
exit 0
