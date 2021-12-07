import tensorflow as tf
import numpy as np
from datetime import datetime
from constants import ModelConstants, TestingConstants, Options
from os import path

model = ""


def strfDelta(tdelta):
    return str(tdelta.seconds) + "." + str(tdelta.microseconds)


def initModel():
    global model
    print("Initializing model")
    model = tf.keras.models.load_model("savedModel/model1")


"""
Takes the flowEntry and uses the trained model to predict whether
the flow is Anomalous or not.
"""


def predictFlow(flowEntry):
    entry = np.array([[float(strfDelta(flowEntry.lastEntry - flowEntry.firstEntry)), float(
        strfDelta(flowEntry.flowLatency)), float(flowEntry.hopLatency), float(flowEntry.queueOccupancy)]])

    entry = entry.reshape(1, 1, 4)

    pred = model.predict(entry)

    predictAnomalous = (pred[0][1] > ModelConstants.AnomalyThreshold)

    # print(f"Flow <{flowEntry.flowTableKey}> Prediction: [NORMAL]")

    if Options.testing:
        prefixIP = flowEntry.flowTableKey.split(":")[0].split(".")[0]

        if Options.verbose:
            print("Prefix IP: ", prefixIP)

        if (prefixIP == ModelConstants.AnomalyIP and predictAnomalous) or (prefixIP != ModelConstants.AnomalyIP and not predictAnomalous):
            # Correct Prediction
            if Options.verbose:
                print("Correct Prediction")

            TestingConstants.correctPredictionsCount = TestingConstants.correctPredictionsCount + 1
            TestingConstants.totalPredictionsCount = TestingConstants.totalPredictionsCount + 1
        else:
            # Incorrect Prediction
            if Options.verbose:
                print("Incorrect Prediction")

            TestingConstants.totalPredictionsCount = TestingConstants.totalPredictionsCount + 1

        if Options.verbose:
            print(f"Flow <{flowEntry.flowTableKey}> Anomalous: {predictAnomalous}")

    # Should be in an else block actually
    else:
        print(f"Flow <{flowEntry.flowTableKey}> Anomalous: {predictAnomalous}")
