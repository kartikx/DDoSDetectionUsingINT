from scapy.all import sniff, Packet
from scapy.fields import (
    ShortField,
    IntField,
    FieldListField,
    ByteField,
    PacketListField,
    BitField,
)


class INTData(Packet):
    name = "INT Data"
    fields_desc = [
        BitField("switchId", 0, 4),
        BitField("padding", 0, 4),
        ByteField("queueDepth", 0),
        ShortField("queueTime", 0),
    ]

    # Required to prevent downstream data from being treated as payload.
    def extract_padding(self, s):
        return '', s

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


def parseINTPacket(pkt):
    print("Received a packet")
    # print(str(pkt));

    pkt.show2()

    # INT is stored as an embedded IP Option.
    intBytes = pkt["IP"]["IP Option"].getfieldval("value")

    print(intBytes)

    # Convert the Raw IP Option into an INT object.
    intPkt = INTLayer(intBytes)

    intPkt.show()

    for data in intPkt.getfieldval("intData"):
        dataPkt = INTData(data)
        print(dataPkt.getfieldval("switchId"), dataPkt.getfieldval("queueDepth"), dataPkt.getfieldval("queueTime"))

    # TODO store in DB.


def main():
    # Sniff packets on CPU Port of Sink Switch.
    iface = "s3-eth3"
    print(f"Sniffing packets on: {iface}")

    sniff(iface=iface, prn=lambda x: parseINTPacket(x))


if __name__ == "__main__":
    main()
