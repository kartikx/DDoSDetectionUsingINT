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
from constants import Options, flowTableIntervalTime
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
    def __init__(self, flowEntry, INTPkt, pkt):
        # This is the first entry.
        if flowEntry is None:
            # TODO Use pkt for this.
            self.protocol = 6

            # Stores the timestamp of the first packet of this flow.
            # Finally, when the flow gets over, we can compute the time difference.
            self.duration = datetime.now()

            # hopL, fowL and qO store the current aggregated respective values for this flow.
            # Since this packet is the first occurence of this flow, initialize all to 0.
            self.hopLatency = 0
            self.flowLatency = timedelta(seconds=0)
            self.queueOccupancy = 0

            # Number of total packets that this flow aggregates over.
            self.numPackets = 1

        # There exists a previous entry on this flow. Current packet should be aggregated in existing flow.
        else:
            self.protocol = flowEntry.protocol

            # Timestamp of Flow initialization is copied over from existing flow.
            self.duration = flowEntry.duration

            # Initialize hopL, flowL and queueO to avg * numPackets.
            # These will be used to compute the new average.
            self.hopLatency = flowEntry.hopLatency * flowEntry.numPackets
            self.flowLatency = flowEntry.flowLatency * flowEntry.numPackets
            self.queueOccupancy = flowEntry.queueOccupancy * flowEntry.numPackets

            # Increase the number of packets this flow aggregates over.
            self.numPackets = flowEntry.numPackets + 1

        # Stores the timestamp of the most recent entry.
        # Used to check staleness of flow entry.
        self.lastEntry = datetime.now()

        INTDataArray = INTPkt.getfieldval("intData")
        length = len(INTDataArray)
        # print(length)

        # Extract sink and source Ingress Time for the INT_MD Header.
        sinkTime = str(INTPkt.getfieldval("sinkIngressTime"))
        sourceTime = str(INTPkt.getfieldval("sourceIngressTime"))

        # Flow Latency is computed as the Time Difference from Source to Sink.
        flowLatency = (
            timedelta(seconds=int(sinkTime[:-6]),
                      microseconds=int(sinkTime[-6:]))
            + Options.sourceSinkTimeDelta
            - timedelta(seconds=int(sourceTime[:-6]),
                        microseconds=int(sourceTime[-6:]))
        )

        # Values for this current packet, will be aggregated into existing flow (if exists).
        hopLatency, queueOccupancy = 0, 0

        for i in range(0, length):
            INTDataPkt = INTData(INTDataArray[i])
            hopLatency += int(INTDataPkt.getfieldval("queueTime"))
            queueOccupancy += int(INTDataPkt.getfieldval("queueDepth"))

        # Aggregate into Existing flow.
        # If this is the first packet of the flow, the previous values would be 0.
        # Otherwise the previous values would be the previous sum (avg * numPackets).
        # TODO How can I write tests for this?
        self.hopLatency = (self.hopLatency + hopLatency /
                           length) / self.numPackets
        self.queueOccupancy = (
            self.queueOccupancy + queueOccupancy / length
        ) / self.numPackets
        self.flowLatency = (self.flowLatency + flowLatency) / self.numPackets

    def __str__(self):
        return (
            str(self.__class__)
            + "\n"
            + "\n".join(
                ("{} = {}".format(item, self.__dict__[
                 item]) for item in self.__dict__)
            )
        )


# Returns the Flow Table index key for this packet.
# TODO Currently only using IP, since not sending TCP level packets.


def getFlowKey(pkt):
    return pkt["IP"].getfieldval("src") + ":" + pkt["IP"].getfieldval("dst")


"""
Extracts INT data from the bytes sniffed on the wire.
"""


def parse_INT_packet(pkt):
    print("Received a packet")
    # print(str(pkt));

    # pkt.show2()

    flowTableKey = getFlowKey(pkt)

    # On the wire, INT is stored as an embedded IP Option.
    INTLayerBytes = pkt["IP"]["IP Option"].getfieldval("value")

    # print(INTLayerBytes)

    # Convert the Raw IP Option into an INT Layer.
    INTPkt = INTLayer(INTLayerBytes)

    INTPkt.show()

    global flowTable

    flowEntry = flowTable.get(flowTableKey)

    if flowEntry:
        print(f"Existing entry with timestamp {flowEntry.lastEntry}")
        currTime = datetime.now()

        if (currTime - flowEntry.lastEntry).seconds > flowTableIntervalTime:
            print("Stale entry")

            # Insert Stale Entry into Database.
            addFlowEntryDatabase(flowEntry)

            # This packet now serves as the first packet of a new flow.
            entry = FlowTableEntry(None, INTPkt, pkt)
        else:
            print("Fresh entry")

            # Packet gets aggregated into existing flow.
            entry = FlowTableEntry(flowEntry, INTPkt, pkt)
    else:
        print("Adding new entry")

        # First packet of a new flow.
        entry = FlowTableEntry(None, INTPkt, pkt)

    flowTable[flowTableKey] = entry
    # print(entry)


def printINTPacket(INTPkt):
    print(len(INTPkt.getfieldval("intData")))
    # Store each INT Data packet in the layer in the Database.
    for data in INTPkt.getfieldval("intData"):
        INTDataPkt = INTData(data)
        print(
            INTDataPkt.getfieldval("switchId"),
            INTDataPkt.getfieldval("queueDepth"),
            INTDataPkt.getfieldval("queueTime"),
        )


def init_database():
    pass


def addFlowEntryDatabase(flowEntry):
    print("--Adding to Database----")
    print(flowEntry)


def sniffPackets():
    print(f"Sniffing packets on: {Options.iface}")
    sniff(iface=Options.iface, prn=lambda x: parse_INT_packet(x))
