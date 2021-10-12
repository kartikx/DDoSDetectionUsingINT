from sniff import sniffPackets, flushFlows
from utils import parseCommandLine, setTimeDifference
from constants import Options
from database import initDatabase
import signal

def handler(signum, frame):
    print("Flushing leftover flows to Database")
    flushFlows()
    print("Flushed leftover flows to Database")

signal.signal(signal.SIGTSTP, handler)

def initCollector():
    # Each router reports timestamps relative to the time at which they
    # were started. Record the time difference between the Source and
    # Sink, to correctly compute flow latency.

    setTimeDifference(Options.source, Options.sink)

    # Initialize the database to be written to.
    initDatabase()

# Sniff packets on CPU Port of Sink Switch.
def main():
    parseCommandLine()

    initCollector()

    print("Sniffing Packets, Press Ctrl+Z to flush flows and Ctrl+C to stop")
    sniffPackets()

if __name__ == "__main__":
    main()
