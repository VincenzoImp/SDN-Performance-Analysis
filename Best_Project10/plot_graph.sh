#!/bin/bash

topology="./topologies/topology2.py"
start=5
stop=500
step=5

usage(){
	echo "usage: plot_graph.sh [-f <topology-file>] [--start <lamda-int-rate>] [--stop <lamda-int-rate>] [--step <lamda-int-rate>]"
}

while [ "$1" != "" ]; do
	case $1 in
		-f ) 
			shift
			topology=$1
		;;
        --start ) 
			shift
			start=$1
		;;
        --stop ) 
			shift
			stop=$1
		;;
        --step ) 
			shift
			step=$1
		;;
		*  )
			usage
			exit 1
	esac
	shift
done

python3 ./utils/generate_graph.py $topology $start $stop $step
clear