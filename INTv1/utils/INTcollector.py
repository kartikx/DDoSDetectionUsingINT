from scapy.all import sniff, Packet
from scapy.fields import (
    ShortField,
    ByteField,
    PacketListField,
    BitField,
)

"""
Represents each INT Data.

! This will require changes every time you modify headers.p4
"""


class INTData(Packet):
    name = "INT Data"
    fields_desc = [
        BitField("switchId", 0, 4),
        BitField("padding", 0, 4),
        ByteField("queueDepth", 0),
        ShortField("queueTime", 0),
    ]

    # Since there exist multiple INTData packets in sequence, this is
    # Required to prevent downstream data from being treated as payload.
    def extract_padding(self, s):
        return "", s


"""
Represents the INT Metadata Header along with the variable length
INT data.

! This class will need changes every time headers.p4 changes. 
"""


class INTLayer(Packet):
    name = "INT Header"
    fields_desc = [
        ShortField("countHeaders", 0),
        PacketListField(
            "intData", None, INTData, count_from=lambda pkt: pkt.countHeaders
        ),
    ]


"""
Extracts INT data from the bytes sniffed on the wire.
"""


def parse_INT_packet(pkt):
    print("Received a packet")
    # print(str(pkt));

    pkt.show2()

    # On the wire, INT is stored as an embedded IP Option.
    INTLayerBytes = pkt["IP"]["IP Option"].getfieldval("value")

    # print(INTLayerBytes)

    # Convert the Raw IP Option into an INT Layer.
    INTPkt = INTLayer(INTLayerBytes)

    INTPkt.show()

    # Store each INT Data packet in the layer in the Database.
    for INTData in INTPkt.getfieldval("intData"):
        INTDataPkt = INTData(INTData)
        print(
            INTDataPkt.getfieldval("switchId"),
            INTDataPkt.getfieldval("queueDepth"),
            INTDataPkt.getfieldval("queueTime"),
        )
        # TODO store in DB.

def init_database():
    pass

def add_INT_data():
    pass

def main():
    # Sniff packets on CPU Port of Sink Switch.
    iface = "s3-eth3"
    print(f"Sniffing packets on: {iface}")

    sniff(iface=iface, prn=lambda x: parse_INT_packet(x))


if __name__ == "__main__":
    main()
