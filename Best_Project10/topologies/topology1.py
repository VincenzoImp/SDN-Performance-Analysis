from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from time import sleep
import sys
import os
import requests
import json

class Network_Topology(Topo):

    def build(self, **opts):

        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Adding switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add links
        self.addLink(h1, s1, bw=10, delay='20ms', max_queue_size=100)
        self.addLink(h2, s2, bw=10, delay='20ms', max_queue_size=100)
        self.addLink(h3, s3, bw=10, delay='20ms', max_queue_size=100)
        self.addLink(h4, s3, bw=10, delay='20ms', max_queue_size=100)

        self.addLink(s1, s2, bw=10, delay='20ms', max_queue_size=100)
        self.addLink(s2, s3, bw=10, delay='20ms', max_queue_size=100)


        return


    def run(self, rate_pkts_s):
        
        if not os.path.exists("./data/topology1/"):
            os.mkdir("./data/topology1/")
            os.chmod("./data/topology1/", 775)
        data_dir = "./data/topology1/lambda{}/".format(rate_pkts_s)
        if not os.path.exists(data_dir):
            os.mkdir(data_dir, mode=775)
            os.chmod(data_dir, 775)

        
        net.start()

        net.pingAll()
        
        
        time_ms = 15000
        pkt_size_bytes = 512
        ttl = 64

        h1 = net.getNodeByName('h1')
        h2 = net.getNodeByName('h2')
        h3 = net.getNodeByName('h3')
        h4 = net.getNodeByName('h4')

        h3.cmd("./D-ITG-2.8.1-r1023/bin/ITGRecv -l {}/h3receiver.log &".format(data_dir))
        h4.cmd("./D-ITG-2.8.1-r1023/bin/ITGRecv -l {}/h4receiver.log &".format(data_dir))

        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -C {} -t {} -f {} -l {}/h1h3sender.log &".format(h3.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -C {} -t {} -f {} -l {}/h1h4sender.log &".format(h4.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl, data_dir))
        h2.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -C {} -t {} -f {} -l {}/h2h3sender.log &".format(h3.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl, data_dir))
        h2.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -C {} -t {} -f {} -l {}/h2h4sender.log &".format(h4.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl, data_dir))
        
        sleep(time_ms/1000)

        s1 = net.getNodeByName('s1')
        s2 = net.getNodeByName('s2')
        s3 = net.getNodeByName('s3')

        s1p2 = requests.get("http://0.0.0.0:8080/stats/port/{}/{}".format(int(s1.dpid), 2))
        s2p2 = requests.get("http://0.0.0.0:8080/stats/port/{}/{}".format(int(s2.dpid), 2))

        s2p3 = requests.get("http://0.0.0.0:8080/stats/port/{}/{}".format(int(s2.dpid), 3))
        s3p3 = requests.get("http://0.0.0.0:8080/stats/port/{}/{}".format(int(s3.dpid), 3))

        d = {"s1p2":s1p2, "s2p2":s2p2, "s2p3":s2p3, "s3p3":s3p3}
        for fname, sp in d.items():
            with open("{}/{}.json".format(data_dir, fname), "w") as f:
                json.dump(sp.json(), f)


        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h3receiver.log > {}/h3receiver.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h4receiver.log > {}/h4receiver.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h1h3sender.log > {}/h1h3sender.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h1h4sender.log > {}/h1h4sender.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h2h3sender.log > {}/h2h3sender.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h2h4sender.log > {}/h2h4sender.txt".format(data_dir, data_dir))

        #generate info.json 
        '''
        {
            'end2end': {
                'h1h3': _,
                'h1h4': _,
                'h2h3': _,
                'h2h4': _
            },
            'utilization': {
                's1s2': _,
                's2s3': _
            },
            'max_lambda': _
        }
        '''

        net.stop()
        return


if __name__=='__main__':
    
    try:
        rate_pkts_s = int(sys.argv[1])
        net = Mininet(topo=Network_Topology(), controller=None, link=TCLink)
        c0 = RemoteController('c0', 'localhost', 6633)
        net.addController(c0)
        net.topo.run(rate_pkts_s)
    except IndexError:
        print("usage: ./topologies/topology1.py <lambda-rate>")
