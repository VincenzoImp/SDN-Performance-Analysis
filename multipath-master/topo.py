#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', dpid='0000000000000001', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', dpid='0000000000000002', protocols='OpenFlow13')
    s3 = net.addSwitch('s3', dpid='0000000000000003', protocols='OpenFlow13')


    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)


    info( '*** Add links\n')
    net.addLink(h1, s1, delay='75ms', bw=30, loss=0)
    net.addLink(h2, s2, delay='75ms', bw=30, loss=0)
    net.addLink(h3, s3, delay='75ms', bw=30, loss=0)
    net.addLink(h4, s3, delay='75ms', bw=30, loss=0)

    net.addLink(s1, s2, delay='75ms', bw=30, loss=0)
    net.addLink(s2, s3, delay='75ms', bw=30, loss=0)
    #aggiungere la riga seguente se si vuole eseguire la seconda topologia
    net.addLink(s1, s3, delay='75ms', bw=30, loss=0)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])

    info( '*** Post configure switches and hosts\n')


    net.pingAll()

    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    h3 = net.getNodeByName('h3')
    h4 = net.getNodeByName('h4')

    #tutti questi parametri nel ping sono un po' inutili, occorre capire quali lasciare o aggiungere
    h1.cmd('ping', '-aAbBdDfLnOqrRUv -c 1000', h3.IP(), '1> ./tmp/h1h3.out 2>/tmp/h1h3.err &')
    h1.cmd('ping', '-aAbBdDfLnOqrRUv -c 1000', h4.IP(), '1> ./tmp/h1h4.out 2>/tmp/h1h4.err &')
    h2.cmd('ping', '-aAbBdDfLnOqrRUv -c 1000', h3.IP(), '1> ./tmp/h2h3.out 2>/tmp/h2h3.err &')
    h2.cmd('ping', '-aAbBdDfLnOqrRUv -c 1000', h4.IP(), '1> ./tmp/h2h4.out 2>/tmp/h2h4.err &')



    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

