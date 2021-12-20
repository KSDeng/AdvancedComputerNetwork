from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.node import Controller, OVSSwitch, RemoteController
import subprocess
import os
from functools import partial

myDelay = '5ms'
myLossPercentage = 0
myQueueSize = 1000

class LineTopo(Topo):
	def build(self):
		print "*** Creating switches"
		s1 = self.addSwitch('S1');
		s2 = self.addSwitch('S2');
		s3 = self.addSwitch('S3');

		print "*** Creating hosts"
		h1 = self.addHost('h1', mac='00:00:00:00:00:01');
		h2 = self.addHost('h2', mac='00:00:00:00:00:02');
		h3 = self.addHost('h3', mac='00:00:00:00:00:03');
		h4 = self.addHost('h4', mac='00:00:00:00:00:04');
		h5 = self.addHost('h5', mac='00:00:00:00:00:05');
		h6 = self.addHost('h6', mac='00:00:00:00:00:06');

		print "*** Creating links"
		self.addLink(s1, h1, bw=7, delay=myDelay);
		self.addLink(s1, h2, bw=5, delay=myDelay);

		self.addLink(s2, h4, bw=4, delay=myDelay);
		self.addLink(s2, h5, bw=10, delay=myDelay);
		self.addLink(s2, h6, bw=2, delay=myDelay);

		self.addLink(s3, h3, bw=10, delay=myDelay);

		self.addLink(s1, s2, bw=5, delay=myDelay, 
			loss=myLossPercentage, max_queue_size=myQueueSize, use_htb=True);
		self.addLink(s1, s3, bw=10, delay=myDelay,
			loss=myLossPercentage, max_queue_size=myQueueSize, use_htb=True);
		self.addLink(s2, s3, bw=10, delay=myDelay,
			loss=myLossPercentage, max_queue_size=myQueueSize, use_htb=True);


def LineNet():
    topo = LineTopo()

    net = Mininet( topo=topo, host=CPULimitedHost, 
        link=TCLink, controller=None, switch=partial(OVSSwitch,protocols='OpenFlow13'))

    print "*** Adding controller. Make sure you run the controller at port 5229!!"
    net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=5229 )
    
    print "*** Starting network"
    net.start()

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    LineNet()






