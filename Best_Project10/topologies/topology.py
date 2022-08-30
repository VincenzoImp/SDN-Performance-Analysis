from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from time import sleep

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
        #aggiungere la riga seguente se si vuole eseguire la seconda topologia
        self.addLink(s1, s3, bw=10, delay='20ms', max_queue_size=100)

        return


def run():
    #la funzione crea la rete ed esegue i quattro stream stabiliti

    
    net = Mininet(topo=Network_Topology(), controller=None, link=TCLink)

    c0 = RemoteController('c0', 'localhost', 6633)
    net.addController(c0)

    net.start()

	
    net.pingAll()
    
    
    time_ms = 15000
    rate_pkts_s = 100
    pkt_size_bytes = 512
    ttl = 64

    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    h3 = net.getNodeByName('h3')
    h4 = net.getNodeByName('h4')

    h3.cmd("./D-ITG-2.8.1-r1023/bin/ITGRecv -l ./tmp/h3receiver.log &")
    h4.cmd("./D-ITG-2.8.1-r1023/bin/ITGRecv -l ./tmp/h4receiver.log &")

    h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -C {} -t {} -f {} -l ./tmp/h1h3sender.log &".format(h3.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl))
    h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -C {} -t {} -f {} -l ./tmp/h1h4sender.log &".format(h4.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl))
    h2.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -C {} -t {} -f {} -l ./tmp/h2h3sender.log &".format(h3.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl))
    h2.cmd("./D-ITG-2.8.1-r1023/bin/ITGSend -T UDP -a {} -c {} -C {} -t {} -f {} -l ./tmp/h2h4sender.log &".format(h4.IP(), pkt_size_bytes, rate_pkts_s, time_ms, ttl))
    
    sleep(time_ms/1000)

    h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec ./tmp/h3receiver.log > ./tmp/h3receiver.txt")
    h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec ./tmp/h4receiver.log > ./tmp/h4receiver.txt")
    h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec ./tmp/h1h3sender.log > ./tmp/h1h3sender.txt")
    h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec ./tmp/h1h4sender.log > ./tmp/h1h4sender.txt")
    h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec ./tmp/h2h3sender.log > ./tmp/h2h3sender.txt")
    h1.cmd("./D-ITG-2.8.1-r1023/bin/ITGDec ./tmp/h2h4sender.log > ./tmp/h2h4sender.txt")


    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
