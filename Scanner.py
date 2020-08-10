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

host = "192.168.0.1"

subnet = "192.168.0.0/24"

# string check ICMP responses for
checkICMP = "JAVAISTHEBEST"


def udp_sender(sender, checkICMP):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for ip in IPNetwork(subnet):
        try:
            # sends udp datagrams ar each ip in subnet
            sender.sendto(checkICMP, ("%s" % ip, 65212))
        except TimeoutError:
            pass


class IP(Structure):
    # maps the first 20 bytes of recieved buffer into an IP header
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
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except IndexError:
            self.protocol = str(self.protocol_num)


# Same as in original sniffer
if os.name == "nt":
    sockProtocol = socket.IPPROTO_IP
else:
    sockProtocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, sockProtocol)

sniffer.bind(host, 0)
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

t = threading.Thread(target=udp_sender, args=(subnet, checkICMP))
t.start()

try:
    # when loop finished, have got an ICMP packet
    while True:
        raw_buffer = sniffer.recvfrom(65565)[0]

        ip_header = IP(raw_buffer[0:20])

        print("Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))

        if ip_header.protocol == "ICMP":
            # get head of ICMP packet
            # ihl says number of 32-bit words in the ip header so 4 * ihl is size of header
            # where this ends we know ICMP starts
            offset = ip_header.ihl * 4

            buf = raw_buffer[offset:offset + sizeof(ICMPStruct)]

            icmp_header = ICMPStruct(buf)

            print("ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code))

            if icmp_header.code == 3 and icmp_header.type == 3:
                if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                    if raw_buffer[len(raw_buffer) - len(checkICMP):] == checkICMP:
                        print("Host Up: %s" % ip_header.src_address)



except KeyboardInterrupt:
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
