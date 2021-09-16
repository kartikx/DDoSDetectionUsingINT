import argparse
from datetime import datetime
from os import path, times

class ArgumentValues:
    # Interface to Sniff packets on.
    iface = ""
    # Source Switch name.
    source = ""
    # Sink Switch name.
    sink = ""
    # TimeDelta between Sink and Source startup times. (Sink > Source).
    sourceSinkTimeDelta = ""

# Returns the Time at which the switch was started.
def getStartupTime(switch):
    # Switch log path name.
    switchLogPath = path.join("log", switch+".log")

    # print(f"Filename: {switchLogPath}")

    with open(switchLogPath) as f:
        _ = f.readline()
        secondLine = f.readline()
        timeStamp = secondLine.split()[0][1:-1]
        print(f"Switch {switch} started at {timeStamp}")

    fmt = "%H:%M:%S.%f"
    return datetime.strptime(timeStamp, fmt)

def setTimeDifference(source, sink):
    sourceStartTime = getStartupTime(source)
    sinkStartTime = getStartupTime(sink)
    
    ArgumentValues.sourceSinkTimeDelta = sinkStartTime - sourceStartTime

def parseCommandLine():
    parser = argparse.ArgumentParser()

    # Add arguments to the Parser.
    parser.add_argument("-i", "--interface",
                        help="Interface to sniff packets on", required="true")
    parser.add_argument("--source", help="Source Switch name", required="true")
    parser.add_argument("--sink", help="Sink Switch name", required="true")

    # Parse actual args from the CLI
    args = parser.parse_args()

    ArgumentValues.iface = args.interface
    ArgumentValues.source = args.source
    ArgumentValues.sink = args.sink
