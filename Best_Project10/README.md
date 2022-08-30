# Usage

#### This project uses [Mininet](http://mininet.org/) to simmulate SDN topologies. 

- Note : The Controller application and the Mininet CLI must be running on separate terminals.

#### Controller

- The controller can be started by simply executing the `run-controller.sh` bash script: 
```
     bash run-controller.sh 
```
- By default, the controller will run `controller.py` located within the `controllers` directory. 

- The `run-controller.sh` script will accept three flags:
	- `-f` or `--file` to specify a path to a custom controller file. 

#### Mininet Topology

- The Mininet Topology can be built by running the `build-topo.sh` bash script:
```
     bash build-topo.sh 
```
- By default, the topology will run `topology.py` located within the `topology` directory. 

- The `build-topo.sh` script will accept these flags as parameters:
	- `-f` or `--file` to specify the path to a custom topology file.



