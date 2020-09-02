# UDP-based host discovery on target network
# Identify all potential targets
# Use known os behaviour for active hosts at an ip address

# windows allows sniffing of all packet types but linux requires us to specify if sniffing ICMP

# Promiscuous mode allows us to sniff all packets seen by the NIC regardless if we are the destination

import socket
import os

# target ip
host = "192.168.0.1"

# if os is windows
if os.name == "nt":
    sockProtocol = socket.IPPROTO_IP
else:
    sockProtocol = socket.IPPROTO_ICMP

# raw socket so reading packets is easier
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, sockProtocol)
sniffer.bind(host, 0)

# set socket option to socket.IP_HDRINCL to declare we want view the IP headers
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# if windows then need to send IOCTL to set promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

print(sniffer.recvfrom(65565))

# disable promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)