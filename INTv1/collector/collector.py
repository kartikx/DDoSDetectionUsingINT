from sniff import sniffPackets
from parser import parseCommandLine, setTimeDifference

# Sniff packets on CPU Port of Sink Switch.
def main():
    parseCommandLine()
    setTimeDifference("s1", "s3")
    sniffPackets()

if __name__ == "__main__":
    main()
