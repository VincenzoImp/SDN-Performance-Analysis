#!/usr/bin/python

'''
Evaluation topology for the controller
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI


class EvaluationTopo(Topo):

    def __init__(self, **opts):
        Topo.__init__(self, **opts)

        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Adding switches
        s1 = self.addSwitch('s1', dpid='0000000000000001', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', dpid='0000000000000002', protocols='OpenFlow13')
        s3 = self.addSwitch('s3', dpid='0000000000000003', protocols='OpenFlow13')

        # Add links
        self.addLink(h1, s1, delay='75ms', bw=30, loss=0)
        self.addLink(h2, s2, delay='75ms', bw=30, loss=0)
        self.addLink(h3, s3, delay='75ms', bw=30, loss=0)
        self.addLink(h4, s3, delay='75ms', bw=30, loss=0)

        self.addLink(s1, s2, delay='75ms', bw=30, loss=0)
        self.addLink(s2, s3, delay='75ms', bw=30, loss=0)
        #aggiungere la riga seguente se si vuole eseguire la seconda topologia
        self.addLink(s1, s3, delay='75ms', bw=30, loss=0)


topos = {'evaluation': (lambda: EvaluationTopo())}
