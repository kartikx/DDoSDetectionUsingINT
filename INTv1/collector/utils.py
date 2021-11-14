from constants import Options, TimeConstants
import argparse
from datetime import datetime, timedelta
from os import path

# Returns the Time at which the switch was started.


def getStartupTime(switch):
    # Switch log path name.
    switchLogPath = path.join("log", switch + ".log")

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

    # ? Adding an extra second for safety.
    Options.sourceSinkTimeDelta = sinkStartTime - sourceStartTime + \
        timedelta(microseconds=TimeConstants.safetyTimeDelta)


def parseCommandLine():
    parser = argparse.ArgumentParser()

    # Add arguments to the Parser.
    parser.add_argument(
        "-i", "--interface", help="Interface to sniff packets on", required="true"
    )
    parser.add_argument(
        "-s", "--source", help="Source Switch name", required="true")
    parser.add_argument(
        "-S", "--sink", help="Sink Switch name", required="true")
    # parser.add_argument("-t", "--time", help="Sink Source Time Delta", required="true")
    parser.add_argument("--new", help="Use new Database", action="store_true")
    parser.add_argument("-v", "--verbose", help="Print useful output for each event", action="store_true")

    # Parse actual args from the CLI
    args = parser.parse_args()

    # Set the passed parameter values, to be used throughout the program.
    Options.iface = args.interface
    Options.source = args.source
    Options.sink = args.sink
    Options.useNewDatabase = args.new
    Options.verbose=args.verbose
    # Assuming delta passed in as egress format.
    # Options.sourceSinkTimeDelta = args.time

    # print("Timedelta: ", args.time)
