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
    # Indicates whether to use a new database for this run (Test runs)
    useNewDatabase = ""
    # Indicates whether to print messages for events.
    verbose = ""
    # Indicates whether Collector is running in predict mode.
    predict = ""

class TimeConstants:
    # Additional Safety Time (in uS) to prevent Negative Flow Latency.
    safetyTimeDelta = 500000

class FlowConstants:
    # Interval after which a Flow Table Entry is considered to be Stale.
    flowTableIntervalTime = 2

class DatabaseConstants:
    # Stores the InfluxDB client connection.
    client = ""

    databaseName = "flowDatabase"

    tableName = "flowTable"

class ModelConstants:
    AnomalyThreshold = 0.8

    # First subaddress of Spoofed Anomalous IP, meant to check whether predicted
    # Anomaly is really an Anomaly.
    AnomalyIP = "69"

class TestingConstants:
    correctPredictionsCount = 0
    totalPredictionsCount = 0