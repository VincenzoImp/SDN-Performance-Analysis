from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from time import sleep
import sys
import os
import requests
import json


class Network_Topology(Topo):

    def build(self, **opts):

        self.BW = 20

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
        self.addLink(h1, s1, port1=1, port2=1, bw=self.BW, delay='20ms', max_queue_size=10)
        self.addLink(h2, s2, port1=1, port2=1, bw=self.BW, delay='20ms', max_queue_size=10)
        self.addLink(h3, s3, port1=1, port2=1, bw=self.BW, delay='20ms', max_queue_size=10)
        self.addLink(h4, s3, port1=1, port2=2, bw=self.BW, delay='20ms', max_queue_size=10)

        self.addLink(s1, s2, port1=2, port2=2, bw=self.BW, delay='20ms', max_queue_size=10)
        self.addLink(s2, s3, port1=3, port2=3, bw=self.BW, delay='20ms', max_queue_size=10)

        return


    def run(self, rate_pkts_s):
        
        if not os.path.exists("./data/topology1/"):
            os.mkdir("./data/topology1/")
        data_dir = "./data/topology1/lambda{}/".format(rate_pkts_s)
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)

        net.start()

        net.pingAll()
        
        print("streaming in progress ...")

        time_ms = 20000
        pkt_size_bytes = 512
        ttl = 64
        time_s = time_ms/1000

        h1 = net.getNodeByName('h1')
        h2 = net.getNodeByName('h2')
        h3 = net.getNodeByName('h3')
        h4 = net.getNodeByName('h4')

        h3.cmd("./D-ITG-2.8.1-r1023/bin/ITGRecv -l {}/h3receiver.log &".format(data_dir))
        h4.cmd("./D-ITG-2.8.1-r1023/bin/ITGRecv -l {}/h4receiver.log &".format(data_dir))

        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -O {} -t {} -f {} -l {}/h1h3sender.log &".format(h3.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -O {} -t {} -f {} -l {}/h1h4sender.log &".format(h4.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl, data_dir))
        h2.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -O {} -t {} -f {} -l {}/h2h3sender.log &".format(h3.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl, data_dir))
        h2.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -O {} -t {} -f {} -l {}/h2h4sender.log &".format(h4.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl, data_dir))
        
        sleep(time_ms/1000)

        switches_data = {}
        for switch_name in  ['s1', 's2', 's3']:
            switch_int = int(net.getNodeByName(switch_name).dpid)
            res = requests.get("http://0.0.0.0:8080/stats/port/{}".format(switch_int)).json()
            switches_data[switch_name] = res[str(switch_int)]
        
        with open("{}/switches_data.json".format(data_dir), "w") as f:
            json.dump(switches_data, f, indent=4)

        links_utilization = {}
        links_utilization['h1s1'] = self.compute_utilization(switches_data['s1'], 1)
        links_utilization['h2s2'] = self.compute_utilization(switches_data['s2'], 1)
        links_utilization['h3s3'] = self.compute_utilization(switches_data['s3'], 1)
        links_utilization['h4s3'] = self.compute_utilization(switches_data['s3'], 2)
        links_utilization['s1s2'] = self.compute_utilization(switches_data['s1'], 2)
        links_utilization['s2s3'] = self.compute_utilization(switches_data['s2'], 3)

        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h3receiver.log -v > {}/h3receiver.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h4receiver.log -v > {}/h4receiver.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h1h3sender.log -v > {}/h1h3sender.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h1h4sender.log -v > {}/h1h4sender.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h2h3sender.log -v > {}/h2h3sender.txt".format(data_dir, data_dir))
        h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec {}/h2h4sender.log -v > {}/h2h4sender.txt".format(data_dir, data_dir))

        paths_info = {}
        paths_info['h1h3'] = self.compute_path_info("{}/h3receiver.txt".format(data_dir), 1)
        paths_info['h1h4'] = self.compute_path_info("{}/h4receiver.txt".format(data_dir), 1)
        paths_info['h2h3'] = self.compute_path_info("{}/h3receiver.txt".format(data_dir), 2)
        paths_info['h2h4'] = self.compute_path_info("{}/h4receiver.txt".format(data_dir), 2)
        paths_info['h_h3'] = self.compute_path_info("{}/h3receiver.txt".format(data_dir), -1)
        paths_info['h_h4'] = self.compute_path_info("{}/h4receiver.txt".format(data_dir), -1)

        data_to_plot = {
            'links_utilization' : links_utilization,
            'paths_info' : paths_info
        }
        with open("{}/data_to_plot.json".format(data_dir), "w") as f:
            json.dump(data_to_plot, f, indent=4)

        for f in os.listdir(data_dir):
            os.chmod("{}/{}".format(data_dir, f), mode=0o777)

        net.stop()
        return

    def compute_utilization(self, data, port):
        self.BW
        max_bytes = self.BW*125000
        for d in data:
            if d['port_no'] == port:
                used_bytes = d["rx_bytes"] + d["tx_bytes"]
                return min(100, (used_bytes/max_bytes)*100)
        return None

    def compute_path_info(self, filename, src):

        if src == -1:
            step = 0
        else:
            step = 1

        avg_delay = None
        pkt_drop_perc = None

        with open(filename, "r") as f:
            for line in f.readlines():
                words = line.split()
                if words == []:
                    continue
                if step == 0 and words[0] == '****************':
                    step = 2
                    continue
                if step == 1 and words[0] == 'From' and int(words[1].split('.')[-1].split(':')[0]) == src:
                    step = 2
                    continue
                if step == 2 and words[0] == 'Average' and words[1] == 'delay':
                    step = 3
                    avg_delay = float(words[3])
                    continue
                if step == 3 and words[0] == 'Packets':
                    step = 4
                    pkt_drop_perc = float(words[4][1:])
                    continue
            d = {
                'avg_delay' : avg_delay,
                'pkt_drop_perc' : pkt_drop_perc
            }
            return d


if __name__=='__main__':
    
    try:
        rate_pkts_s = int(sys.argv[1])
        setLogLevel( 'info' )
        print()
        print()
        print("testing topology1 with lambda {}".format(rate_pkts_s))
        net = Mininet(topo=Network_Topology(), controller=None, link=TCLink)
        c0 = RemoteController('c0', 'localhost', 6633)
        net.addController(c0)
        net.topo.run(rate_pkts_s)
    except IndexError:
        print("usage: ./topologies/topology1.py <lambda-rate>")