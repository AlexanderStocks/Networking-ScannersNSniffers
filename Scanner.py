import socket
import os
import struct
from ctypes import *
from ICMPStruct import ICMPStruct
import threading
import time

# netaddr makes it easy to work with subnets and addressing
# can make iterators through each packet in a network and send
from netaddr import IPNetwork, IPAddress

hostIP = "192.168.0.1"

subnetIP = "192.168.0.0/24"

# string check ICMP responses for
checkICMP = "JAVAISTHEBEST"


def sendUDP(senderSock, checkICMP):
    time.sleep(5)
    senderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for ip in IPNetwork(subnetIP):
        try:
            # sends udp datagrams ar each ip in subnetIP
            senderSock.sendto(checkICMP, ("%s" % ip, 65212))
        except TimeoutError:
            pass


class IPStruct(Structure):
    # maps the first 20 bytes of received buffer into an IP header
    _fields_ = [
        ("ihl", c_ubyte, 4),  # specifies field is 4 bits wide
        ("version", c_ubyte, 4),  # specifies field is 4 bits wide
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_ulong),
        ("dst", c_ulong)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # sets up the output to be readable
        self.protocolMap = {1: "ICMP", 6: "TCP", 17: "UDP"}

        self.srcAddress = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dstAddress = socket.inet_ntoa(struct.pack("<L", self.dst))

        try:
            self.protocol = self.protocolMap[self.protocol_num]
        except IndexError:
            self.protocol = str(self.protocol_num)


# Same as in original sniffer
if os.name == "nt":
    protocolSock = socket.IPPROTO_IP
else:
    protocolSock = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocolSock)

sniffer.bind(hostIP, 0)
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

thread = threading.Thread(target=sendUDP, args=(subnetIP, checkICMP))
thread.start()

try:
    # when loop finished, have got an ICMP packet
    while True:
        rawBuffer = sniffer.recvfrom(65565)[0]

        ipHeader = IPStruct(rawBuffer[0:20])

        print("Protocol: %s %s -> %s" % (ipHeader.protocol, ipHeader.srcAddress, ipHeader.dstAddress))

        if ipHeader.protocol == "ICMP":
            # get head of ICMP packet
            # ihl says number of 32-bit words in the ip header so 4 * ihl is size of header
            # where this ends we know ICMP starts
            offset = ipHeader.ihl * 4

            buffer = rawBuffer[offset:offset + sizeof(ICMPStruct)]

            icmpHeader = ICMPStruct(buffer)

            print("ICMP -> Type: %d Code: %d" % (icmpHeader.type, icmpHeader.code))

            if icmpHeader.code == 3 and icmpHeader.type == 3:
                if IPAddress(ipHeader.srcAddress) in IPNetwork(subnetIP):
                    if rawBuffer[len(rawBuffer) - len(checkICMP):] == checkICMP:
                        print("hostIP Up: %s" % ipHeader.srcAddress)
except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)