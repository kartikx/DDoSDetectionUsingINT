class Options:
    # Interface to Sniff packets on.
    iface = ""
    # Source Switch name.
    source = ""
    # Sink Switch name.
    sink = ""
    # TimeDelta between Sink and Source startup times. (Sink > Source).
    sourceSinkTimeDelta = ""

# Interval after which a Flow Table Entry is considered to be Stale.
flowTableIntervalTime = 10
