from sniff import sniffPackets, flushFlows
from utils import parseCommandLine, setTimeDifference
from constants import Options, TestingConstants
from database import initDatabase
from predictor import initModel
import signal

# Clean this up?
def sigTSTPhandler(signum, frame):
    print("Flushing leftover flows to Database")
    flushFlows()
    print("Flushed leftover flows to Database")

original_sigint_handler = signal.getsignal(signal.SIGINT)

def sigINThandler(signum, frame):
    if Options.testing:
        print(f"Test Accuracy: {(float(TestingConstants.correctPredictionsCount) / float(TestingConstants.totalPredictionsCount))*100} %") 
    return original_sigint_handler(signum, frame)

signal.signal(signal.SIGTSTP, sigTSTPhandler)
signal.signal(signal.SIGINT, sigINThandler)


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

    if Options.predict:
        initModel()

    print("Sniffing Packets, Press Ctrl+Z to flush flows and Ctrl+C to stop")
    sniffPackets()

if __name__ == "__main__":
    main()
