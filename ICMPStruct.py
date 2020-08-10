from ctypes import *


class ICMPStruct(Structure):
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
    ]

    def __new__(cls, socketBuffer):
        return cls.from_buffer_copy(socketBuffer)

    def __init__(self, socketBuffer):
        pass
