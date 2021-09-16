from sniff import sniffPackets
from utils import parseCommandLine, setTimeDifference
from constants import Options

# Sniff packets on CPU Port of Sink Switch.
def main():
    parseCommandLine()
    setTimeDifference(Options.source, Options.sink)
    sniffPackets()

if __name__ == "__main__":
    main()
