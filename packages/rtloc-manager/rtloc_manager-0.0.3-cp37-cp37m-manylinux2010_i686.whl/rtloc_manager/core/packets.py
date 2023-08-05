import cx_packets

TYPE_DW = cx_packets.TYPE_DW
TYPE_HB = cx_packets.TYPE_HB

MESSAGE_TYPE_RANGING = cx_packets.CXDWPacket._MESSAGE_TYPE_RANGING

class Header:
    def __init__(self, bytes):
        """[summary]

        Args:
            bytes ([type]): [description]
        """
        self.__header = cx_packets.Header(bytes)

    @property
    def packet_len(self):
        return self.__header.packet_len

    @property
    def type(self):
        return self.__header.type

class CXDWPacket:
    def __init__(self, header, bytes, callback=None):
        """[summary]

        Args:
            header ([type]): [description]
            bytes ([type]): [description]
            callback ([type], optional): [description]. Defaults to None.
        """
        self.__cx_dw_packet = cx_packets.CXDWPacket(header, bytes,
                                                    callback=callback)

    @property
    def addr(self):
        return self.__cx_dw_packet.addr

    @property
    def reports(self):
        return self.__cx_dw_packet.reports

    @property
    def message_type(self):
        return self.__cx_dw_packet.message_type

    def callback(self):
        self.__cx_dw_packet.callback()
