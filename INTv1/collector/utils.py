from constants import Options
import argparse
from datetime import datetime
from os import path

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
    
    Options.sourceSinkTimeDelta = sinkStartTime - sourceStartTime

def parseCommandLine():
    parser = argparse.ArgumentParser()

    # Add arguments to the Parser.
    parser.add_argument("-i", "--interface",
                        help="Interface to sniff packets on", required="true")
    parser.add_argument("-s", "--source", help="Source Switch name", required="true")
    parser.add_argument("-S", "--sink", help="Sink Switch name", required="true")

    # Parse actual args from the CLI
    args = parser.parse_args()

    # Set the passed parameter values, to be used throughout the program.
    Options.iface = args.interface
    Options.source = args.source
    Options.sink = args.sink
