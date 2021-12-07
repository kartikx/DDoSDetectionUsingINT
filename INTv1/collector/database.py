"""
Responsible for Flow Entry Database operations
"""

from influxdb import InfluxDBClient
from datetime import datetime
from constants import DatabaseConstants, Options
from predictor import predictFlow

def strfDelta(tdelta):
    return str(tdelta.seconds) + "." + str(tdelta.microseconds)


def initDatabase():

    DatabaseConstants.client = InfluxDBClient(host='localhost', port=8086)

    databaseObject = {'name': DatabaseConstants.databaseName}
    # If Database does not already exist, create database.
    if databaseObject not in DatabaseConstants.client.get_list_database():
        print("Didn't find existing database, creating a new one")
        DatabaseConstants.client.create_database(
            DatabaseConstants.databaseName)

    # Make client operate on this database.
    DatabaseConstants.client.switch_database(DatabaseConstants.databaseName)


def addFlowEntry(flowEntry):
    # Not operating in Data Gathering mode.
    # Make the prediction and return.
    if Options.predict:
        if Options.verbose:
            print("Calling prediction")
        return predictFlow(flowEntry)

    now = datetime.now()

    if Options.useNewDatabase:
        tableName = DatabaseConstants.tableName + \
            str(now.day) + str(now.month) + \
            str(now.hour) + str(now.minute)
    else:
        tableName = DatabaseConstants.tableName

    if Options.verbose:
        print("Table Name: ", tableName)

    # print(flowEntry)
    # Convert flowEntry to JSON Format to be inserted.
    tableEntry = [
        {
            "measurement": tableName,
            "tags": {
                "flowKey": flowEntry.flowTableKey
            },
            "time": now,
            "fields": {
                "protocol": flowEntry.protocol,
                "hopLatency": flowEntry.hopLatency,
                "flowLatency": float(strfDelta(flowEntry.flowLatency)),
                "queueOccupancy": flowEntry.queueOccupancy,
                "duration": float(strfDelta(flowEntry.lastEntry - flowEntry.firstEntry)),
                "numPackets": flowEntry.numPackets
            }
        }
    ]

    DatabaseConstants.client.write_points(tableEntry)
    # print("Written point")
