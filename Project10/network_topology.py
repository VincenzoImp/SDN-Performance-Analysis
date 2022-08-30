from hmac import trans_36
from http.server import HTTPServer
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
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
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s3)

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        #aggiungere la riga seguente se si vuole eseguire la seconda topologia
        self.addLink(s1, s3)

        return


def run():
    #la funzione crea la rete ed esegue i quattro stream stabiliti

    c0 = RemoteController('c0', 'localhost', 6633)
    net = Mininet(topo=Network_Topology(), controller=None)
    net.addController(c0)
    net.start()
    net.pingAll()
    """
    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    h3 = net.getNodeByName('h3')
    h4 = net.getNodeByName('h4')

    #tutti questi parametri nel ping sono un po' inutili, occorre capire quali lasciare o aggiungere
    h1.cmd('ping', '-aAbBdDfLnOqrRUv -c 100', h3.IP(), '1> ./tmp/h1h3.out 2>/tmp/h1h3.err &')
    h1.cmd('ping', '-aAbBdDfLnOqrRUv -c 100', h4.IP(), '1> ./tmp/h1h4.out 2>/tmp/h1h4.err &')
    h2.cmd('ping', '-aAbBdDfLnOqrRUv -c 100', h3.IP(), '1> ./tmp/h2h3.out 2>/tmp/h2h3.err &')
    h2.cmd('ping', '-aAbBdDfLnOqrRUv -c 100', h4.IP(), '1> ./tmp/h2h4.out 2>/tmp/h2h4.err &')
    """
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
