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

class FlowConstants:
    # Interval after which a Flow Table Entry is considered to be Stale.
    flowTableIntervalTime = 4

class DatabaseConstants:
    # Stores the InfluxDB client connection.
    client = ""

    databaseName = "flowDatabase"

    tableName = "flowTable"