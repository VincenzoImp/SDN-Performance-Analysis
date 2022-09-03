#!/bin/bash


controller="./controllers/controller1.py"
gui="./gui/gui_topology.py"

usage(){
	echo "usage: run_controller.h [-f <controller-file>]"
}

while [ "$1" != "" ]; do
	case $1 in
		-f ) 
			shift
			controller=$1
		;;
		*  )
			usage
			exit 1
	esac
	shift
done

sudo mn -c
clear
ryu-manager --observe-links $gui $controller
clear
