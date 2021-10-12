from influxdb import InfluxDBClient
import numpy as np
import pandas as pd
import pickle

# IP with which abnormal flows start.
abnormalIP = "69"


class Constants:
    NormalID = 0
    AbnormalID = 1
    ArrayLen = 5


class Parameters:
    HopLatencyScale = 1000
    QueueOccupancyScale = 10
    TrainSplit = 0.9
    AbnormalFlowLimit = 200

# Notes
# ! Why do I have a 1.977 duration Abnormal Flow.


def collectData():
    client = InfluxDBClient(host='localhost', port=8086)

    # First get Normal Flows
    result = client.query(
        f"SELECT * from flowTable WHERE flowKey !~ /{abnormalIP}.*/", database="flowDatabase")
    normalPoints = list(result.get_points(measurement="flowTable"))

    # Format : <Normal, Duration, flowL, hopL, numPackets, queueO>
    normalFlows = np.empty((0, Constants.ArrayLen))

    # ? Implement Scaling, check using different values.
    for point in normalPoints:
        normalFlows = np.append(normalFlows, [[float(point["duration"]), float(
            point["flowLatency"]), point["hopLatency"]/Parameters.HopLatencyScale, point["numPackets"], point["queueOccupancy"]/Parameters.QueueOccupancyScale]], axis=0)

    # print(len(normalFlows), normalFlows[0])

    # ? Convert to DataFrame to get statistics about flow.
    # df = pd.DataFrame(normalFlows, columns=["Type", "Duration", "FlowL", "HopL", "NumPackets", "QueueO"])
    # print(df)
    # print(df["QueueO"].max(), df["QueueO"].min())

    result = client.query(
        f"SELECT * from flowTable WHERE flowKey =~ /{abnormalIP}.*/", database="flowDatabase")
    abnormalPoints = list(result.get_points(measurement="flowTable"))

    # Format : <Normal, Duration, flowL, hopL, numPackets, queueO>
    abnormalFlows = np.empty((0, Constants.ArrayLen))

    # ? Implement Scaling, check using different values.
    for point in abnormalPoints:
        abnormalFlows = np.append(abnormalFlows, [[float(point["duration"]), float(
            point["flowLatency"]), point["hopLatency"]/Parameters.HopLatencyScale, point["numPackets"], point["queueOccupancy"]/Parameters.QueueOccupancyScale]], axis=0)

    # print(len(abnormalFlows), abnormalFlows[0])

    # df = pd.DataFrame(abnormalFlows, columns=["Type", "Duration", "FlowL", "HopL", "NumPackets", "QueueO"])
    # print(df)
    # print(df["Duration"].max(), df["Duration"].min())

    # Arrays are currently sorted by time, shuffle it.
    # np.random.shuffle(normalFlows)
    # np.random.shuffle(abnormalFlows)

    # ? Scale size of Normal and Abnormal Flows.
    # ? Currently Abnormal Flows are way greater.
    # ! I could also do this in the Query?
    abnormalFlows = abnormalFlows[:Parameters.AbnormalFlowLimit]

    # print(len(normalFlows), len(abnormalFlows))
    # Return the x_train, x_test.
    splitNormal, splitAbnormal = int(len(
        normalFlows)*Parameters.TrainSplit), int(len(abnormalFlows)*Parameters.TrainSplit)

    # print(normalFlows[:splitNormal])
    # print(abnormalFlows[:splitAbnormal])

    x_train = normalFlows[:splitNormal]
    y_train = np.zeros(len(x_train))
    x_train = np.append(x_train, abnormalFlows[:splitAbnormal], axis=0)
    y_train = np.append(y_train, np.ones(splitAbnormal))

    x_test = normalFlows[splitNormal:]
    y_test = np.zeros(len(x_test))
    x_test = np.append(x_test, abnormalFlows[splitAbnormal:], axis=0)
    y_test = np.append(y_test, np.ones(len(abnormalFlows)-splitAbnormal))

    # Shuffle before returning.
    # np.random.shuffle(x_train)
    # np.random.shuffle(x_test)

    print(len(x_train), len(y_train), len(x_test), len(y_test))

    # To check if we labelled correctly.
    # Include label in the array before doing this.
    # for i in range(len(y_train)):
    #     print(y_train[i], x_train[i])

    return (x_train, y_train), (x_test, y_test)


def main():
    (x_train, y_train), (x_test, y_test) = collectData()

    train_shuffler = np.random.permutation(len(x_train))
    x_train = x_train[train_shuffler]
    y_train = y_train[train_shuffler]

    test_shuffler = np.random.permutation(len(x_test))
    x_test = x_test[test_shuffler]
    y_test = y_test[test_shuffler]

    # Check if shuffled output is correct.
    # for i in range(len(y_test)):
    #     if y_test[i] != x_test[i][0]:
    #         print("oops")

    with open("x_train_data", "wb") as f:
        pickle.dump(x_train, f)

    with open("y_train_data", "wb") as f:
        pickle.dump(y_train, f)

    with open("x_test_data", "wb") as f:
        pickle.dump(x_test, f)

    with open("y_test_data", "wb") as f:
        pickle.dump(y_test, f)

if __name__ == '__main__':
    main()
