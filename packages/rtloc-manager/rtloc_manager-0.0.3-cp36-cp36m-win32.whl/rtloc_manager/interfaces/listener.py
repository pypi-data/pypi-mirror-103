"""
    RTLOC - Manager Lib

    rtloc_manager/interfaces/listener.py

    (c) 2020 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import socket

from rtloc_manager.core.packets import Header, CXDWPacket, TYPE_DW, MESSAGE_TYPE_RANGING
from rtloc_manager.manager_api import ManagerInterface, DistanceReport

class Listener:
    def __init__(self):
        self.fragmentation_buf = bytearray()
        self.ip_addr = None

    def bind_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Broadcast
        self.client.bind(("", 11901))

    def close_socket(self):
        try:
            self.ip_addr = None
            self.client.close()
        except AttributeError:
            # socket has not been binded
            # do nothing
            pass

    def read_from_socket(self):
        # this socket call is blocking
        # TODO optimize buffer size
        recv_data, addr = self.client.recvfrom(4096)

        if self.ip_addr != addr and self.ip_addr is not None:
            return []

        # UDP data can contain multiple cx packets
        multiple_cx_packets = True

        # fix for packet fragmentation
        # TODO: check whether this can be fixed using sockets lib
        recv_data = self.fragmentation_buf + recv_data
        self.fragmentation_buf = bytearray()

        packets = []

        while(multiple_cx_packets):
            try:
                header = Header(recv_data[:9])
            except UnicodeDecodeError:
                # can happen that the data is not of the expected format
                # print("[unexpected header data] clearing buffers and continuing")
                print("Decode Error")
                multiple_cx_packets = False
                self.fragmentation_buf = bytearray()
                continue
            except AssertionError:
                # TODO possibly the header is split, can we detect this?
                print("Assertion Error")
                multiple_cx_packets = False
                self.fragmentation_buf = bytearray()
                continue

            if len(recv_data) > header.packet_len:
                data = recv_data[:header.packet_len]
                recv_data = recv_data[header.packet_len:]
            else:
                data = recv_data
                multiple_cx_packets = False

            if len(data) != header.packet_len:
                self.fragmentation_buf = data
                continue

            assert len(data) == header.packet_len

            if header.type == TYPE_DW:
                packets.append(CXDWPacket(header, data))
                self.ip_addr = addr

        return packets


class ListenerInterface(ManagerInterface):
    def __init__(self):
        self.listener = Listener()
        self.listener.bind_socket()

    def read_data(self):
        """ Get distance data from an abstract interface.
        This function is assumed to be implemented as a blocking
        function call, until new data becomes available.

        Only returning new data will create some room for
        apps to act on the data and not putting too much
        pressure on the CPU.

        Returns:
            list: distance report list
        """
        packets = self.listener.read_from_socket()

        distance_reports = []

        for packet in packets:
            distances_dict = {}
            
            if packet.message_type != MESSAGE_TYPE_RANGING:
                continue

            for report in packet.reports:
                distances_dict[report.addr] = report.dist
    
            distance_reports.append(DistanceReport(packet.addr, distances_dict))

        return distance_reports

    def stop(self):
        """ Properly stop the interface
        """
        self.listener.close_socket()

    def is_symmetrical(self):
        """ This interface is symmetrical.
        """
        return True
