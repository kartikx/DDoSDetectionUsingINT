"""
Responsible for Sniffing Packets on the Interface.
"""

from scapy.all import sniff, Packet
from scapy.fields import (
    ShortField,
    IntField,
    PacketListField,
    BitField,
)
from constants import Options
from datetime import datetime, timedelta

flowTable = {}

"""
Represents each INT Data.

! This will require changes every time you modify int_data changes
"""


class INTData(Packet):
    name = "INT Data"
    fields_desc = [
        BitField("switchId", 0, 4),
        BitField("queueDepth", 0, 12),
        ShortField("queueTime", 0),
    ]

    # Since there exist multiple INTData packets in sequence, this is
    # Required to prevent downstream data from being treated as payload.
    def extract_padding(self, s):
        return "", s


"""
Represents the INT Metadata Header along with the variable length
INT data.

! This class will need changes every time int_md changes. 
"""


class INTLayer(Packet):
    name = "INT Header"
    fields_desc = [
        ShortField("countHeaders", 0),
        IntField("sourceIngressTime", 0),
        IntField("sinkIngressTime", 0),
        PacketListField(
            "intData", None, INTData, count_from=lambda pkt: pkt.countHeaders
        ),
    ]


class FlowTableEntry:
    # INTPkt represents the first occurence of this flow.
    # def __init__(self, INTPkt, pkt):
    #     # TODO Use pkt for this.
    #     self.protocol = 6;

    #     # Stores the timestamp of the first packet of this flow.
    #     # Finally, when the flow gets over, we can compute the time difference.
    #     self.duration = datetime.now();
    #     self.hopLatency = 0;
    #     self.flowLatency = 0;
    #     self.queueOccupancy = 0;

    #     # Number of packets that this flow aggregates over.
    #     self.numPackets = 1;

    #     INTDataArray = INTPkt.getfieldval("intData");
    #     length = len(INTDataArray)
    #     print(length)

    #     sourceTime=0, lastTransitTime=0;

    #     for i in range(0, length):
    #         INTDataPkt = INTData(INTDataArray[i])
    #         self.hopLatency += int(INTDataPkt.getfieldval("queueTime"))
    #         self.queueOccupancy += int(INTDataPkt.getfieldval("queueDepth"))

    #         if i == 0 :
    #             sourceTime = str(INTDataPkt.getfieldval("ingressTime"))
    #         elif i == length - 1:
    #             lastTransitTime = str(INTDataPkt.getfieldval("ingressTime"))

    #     self.hopLatency /= length;
    #     self.queueOccupancy /= length;

    #     self.flowLatency = timedelta(seconds=int(lastTransitTime[:-6]), microseconds=int(lastTransitTime[-6:])) + Options.sourceSinkTimeDelta - timedelta(seconds=int(sourceTime[:-6]), microseconds=int(sourceTime[-6:]))

    def __init__(self, flowEntry, INTPkt, pkt):
        # This is the first entry.
        if flowEntry is None:
            # TODO Use pkt for this.
            self.protocol = 6

            # Stores the timestamp of the first packet of this flow.
            # Finally, when the flow gets over, we can compute the time difference.
            self.duration = datetime.now()
            self.hopLatency = 0
            self.flowLatency = timedelta(seconds=0)
            self.queueOccupancy = 0
            # Number of packets that this flow aggregates over.
            self.numPackets = 1

        # There exists a previous entry on this flow. Current packet should be aggregated in existing flow.
        else:
            self.protocol = flowEntry.protocol

            self.duration = flowEntry.duration

            # Initialize hopLatency to prevAvg * prevCount;
            self.hopLatency = flowEntry.hopLatency * flowEntry.numPackets
            self.flowLatency = flowEntry.flowLatency * flowEntry.numPackets
            self.queueOccupancy = flowEntry.queueOccupancy * flowEntry.numPackets
            self.numPackets = flowEntry.numPackets + 1

        # Used to check staleness of flow entry.
        self.lastEntry = datetime.now()

        INTDataArray = INTPkt.getfieldval("intData")
        length = len(INTDataArray)
        print(length)

        sinkTime = str(INTPkt.getfieldval("sinkIngressTime"))
        sourceTime = str(INTPkt.getfieldval("sourceIngressTime"))

        # Values for this current packet, will be aggregated into existing flow (if exists).
        hopLatency, queueOccupancy, flowLatency = 0, 0, 0

        for i in range(0, length):
            INTDataPkt = INTData(INTDataArray[i])
            hopLatency += int(INTDataPkt.getfieldval("queueTime"))
            queueOccupancy += int(INTDataPkt.getfieldval("queueDepth"))

        # Flow Latency is computed as the Time Difference from Source
        flowLatency = timedelta(seconds=int(sinkTime[:-6]), microseconds=int(
            sinkTime[-6:])) + Options.sourceSinkTimeDelta - timedelta(seconds=int(sourceTime[:-6]), microseconds=int(sourceTime[-6:]))

        # Aggregate into Existing flow.
        # If this is the first packet of the flow, the previous values would be 0.
        # Otherwise the previous values are to be aggregated to.
        self.hopLatency = (self.hopLatency + hopLatency/length)/self.numPackets
        self.queueOccupancy = (self.queueOccupancy +
                               queueOccupancy/length)/self.numPackets
        self.flowLatency = (self.flowLatency + flowLatency)/self.numPackets

    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

def getFlowKey(pkt):
    return pkt["IP"].getfieldval("src") + ":"+pkt["IP"].getfieldval("dst")


"""
Extracts INT data from the bytes sniffed on the wire.
"""


def parse_INT_packet(pkt):
    print("Received a packet")
    # print(str(pkt));

    pkt.show2()

    flowTableKey = getFlowKey(pkt)

    # On the wire, INT is stored as an embedded IP Option.
    INTLayerBytes = pkt["IP"]["IP Option"].getfieldval("value")

    # print(INTLayerBytes)

    # Convert the Raw IP Option into an INT Layer.
    INTPkt = INTLayer(INTLayerBytes)

    INTPkt.show()

    global flowTable;

    keyExists = flowTable.get(flowTableKey)

    if keyExists:
        print(f"Existing entry with timestamp {keyExists.lastEntry}")
        entry = FlowTableEntry(keyExists, INTPkt, pkt)
        flowTable[flowTableKey] = entry
        print(entry)
    else:
        print("Adding new entry")
        entry = FlowTableEntry(None, INTPkt, pkt)
        flowTable[flowTableKey] = entry
        print(entry)
    # print(len(INTPkt.getfieldval("intData")))
    # # Store each INT Data packet in the layer in the Database.
    # for data in INTPkt.getfieldval("intData"):
    #     INTDataPkt = INTData(data)
    #     print(
    #         INTDataPkt.getfieldval("switchId"),
    #         INTDataPkt.getfieldval("queueDepth"),
    #         INTDataPkt.getfieldval("queueTime"),
    #     )
    #     # TODO store in DB.


def init_database():
    pass


def add_INT_data():
    pass


def sniffPackets():
    print(f"Sniffing packets on: {Options.iface}")
    # sniff(iface=ArgumentValues.iface, prn=lambda x: parse_INT_packet(x))
    sniff(iface="s3-eth3", prn=lambda x: parse_INT_packet(x))
