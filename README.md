# Usage

#### This project uses [Mininet](http://mininet.org/) to simmulate SDN topologies. 

- Note : The Controller application and the Mininet topology must be running on separate terminals.

#### Controller

- The controller can be started by simply executing the `run_controller.sh` bash script: 
```
     bash run_controller.h [-f <controller-file>]
```
- By default, the controller will run `controller1.py` located within the `controllers` directory. 

#### Mininet Topology

- The Mininet Topology can be test by running the `test-topo.sh` bash script:
```
     bash test_topo.sh [-f <topology-file>] [--start <lamda-int-rate>] [--stop <lamda-int-rate>] [--step <lamda-int-rate>]
```
- By default, the topology will run `topology2.py` located within the `topologies` directory. 
- By default, start = 2, stop = 200, step = 2.


#### Plot test results

- The Graps can be plot by running the `plot_graphs.sh` bash script:
```
     bash plot_graphs.sh [-f <topology-file>] [--start <lamda-int-rate>] [--stop <lamda-int-rate>] [--step <lamda-int-rate>]
```
- By default, the script will generate plots about `topology2.py` located within the `topologies` directory. 
- By default, start = 2, stop = 200, step = 2.








