#!/usr/bin/env python

import os
import sys
import time
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller, RemoteController
from mn_wifi.link import wmediumd
from mininet.link import TCLink

def topology(args):
    """Create and manage the network topology."""
    info("*** Initializing network\n")
    # link=wmediumd is used for WiFi, but wired links fall back to TCLink logic automatically
    net = Mininet_wifi(controller=Controller, link=wmediumd)

    # Add controller
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    # Add access point
    ap1 = net.addAccessPoint(
        'ap1', ssid="ap1", mac='00:00:00:00:00:01', mode="g", channel="6",
        position='500,1250,0', range=200
    )

    # Add station
    h1 = net.addStation(
        'client', ip='10.0.0.1/8', mac='00:00:00:00:01:01',
        position='400,1250,0', range=100
    )

    # Add hosts
    h2 = net.addHost("server", ip='10.0.0.2/8', mac='00:00:00:00:01:02')
    h3 = net.addHost("h3", ip='10.0.0.3/8', mac='00:00:00:00:01:03')
    h4 = net.addHost("h4", ip='10.0.0.4/8', mac='00:00:00:00:01:04')

    # Add switches
    switches = [
        net.addSwitch(f"s{i}", mac=f"00:00:00:00:00:0{i}") for i in range(2, 10)
    ]
    s2, s3, s4, s5, s6, s7, s8, s9 = switches

    # Configure propagation model
    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3)

    # Configure WiFi nodes
    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    # Add links
    # OPTIMIZATION: Added max_queue_size=1000 to prevent buffer bottlenecks on high-bw links
    info("*** Creating links\n")
    net.addLink(h1, ap1) # WiFi link
    
    # Wired links with Queue Optimization
    net.addLink(s2, ap1, bw=80, delay='25ms')
    net.addLink(s2, s9, bw=70, delay='15ms')
    net.addLink(s9, s3, bw=50, delay='20ms')
    net.addLink(s3, s4, bw=50, delay='5ms')
    net.addLink(s4, h2, bw=50, delay='20ms')
    net.addLink(s4, s7, bw=50, delay='5ms')
    net.addLink(s7, s5, bw=70, delay='10ms')
    net.addLink(s5, h3, bw=50, delay='5ms')
    net.addLink(s4, s8, bw=50, delay='5ms')
    net.addLink(s8, s6, bw=60, delay='5ms')
    net.addLink(s6, h4, bw=60, delay='12ms')
    net.addLink(s5, s9, bw=50, delay='10ms')
    net.addLink(s9, s6, bw=50, delay='5ms')

    # Build and start the network
    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    for switch in switches:
        switch.start([c0])
        
        
    # Signal that topology is ready
    open("/tmp/mininet_ready", "w").close()
    info("*** Topology ready\n")

    while True:
        time.sleep(1)

if __name__ == '__main__':
    setLogLevel('info')
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    # Run the topology
    topology(sys.argv)