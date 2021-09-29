"""
Stores the variables shared among files.
"""

# Stores contents of Parsed CLI variables.
class Options:
    # Interface to Sniff packets on.
    iface = ""
    # Source Switch name.
    source = ""
    # Sink Switch name.
    sink = ""
    # TimeDelta between Sink and Source startup times. (Sink > Source).
    sourceSinkTimeDelta = ""

class TimeConstants:
    # Additional Safety Time (in uS) to prevent Negative Flow Latency.
    safetyTimeDelta = 5000

class FlowConstants:
    # Interval after which a Flow Table Entry is considered to be Stale.
    flowTableIntervalTime = 2

class DatabaseConstants:
    # Stores the InfluxDB client connection.
    client = ""

    databaseName = "flowDatabase"

    tableName = "flowTable"