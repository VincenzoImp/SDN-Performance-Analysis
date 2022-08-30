#!/bin/bash


controller="./controllers/controller.py"

usage(){
	echo "usage: run-controller.h [-f file]"
}

while [ "$1" != "" ]; do
	case $1 in
		-f | --file ) shift
			      controller=$1
			      ;;
		* )	      usage
			      exit 1
	esac
	shift
done

sudo mn -c; clear
ryu-manager $controller
