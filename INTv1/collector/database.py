"""
Responsible for Flow Entry Database operations
"""

from influxdb import InfluxDBClient
from datetime import datetime
from constants import DatabaseConstants

def strfDelta(tdelta):
    return str(tdelta.seconds) + "." + str(tdelta.microseconds)

def initDatabase():

    DatabaseConstants.client = InfluxDBClient(host='localhost', port=8086)

    databaseObject = {'name': DatabaseConstants.databaseName}
    # If Database does not already exist, create database.
    if databaseObject not in DatabaseConstants.client.get_list_database():
        DatabaseConstants.client.create_database(DatabaseConstants.databaseName)

    # Make client operate on this database.
    DatabaseConstants.client.switch_database(DatabaseConstants.databaseName)

def addFlowEntry(flowEntry):
    now = datetime.now()

    # print(flowEntry)
    # Convert flowEntry to JSON Format to be inserted.
    tableEntry = [
        {
            "measurement": DatabaseConstants.tableName,
            "tags": {
                "flowKey": flowEntry.flowTableKey
            },
            "time": now,
            "fields": {
                "protocol": flowEntry.protocol,
                "hopLatency": flowEntry.hopLatency,
                "flowLatency": strfDelta(flowEntry.flowLatency),
                "queueOccupancy": flowEntry.queueOccupancy,
                "duration": strfDelta(flowEntry.lastEntry - flowEntry.firstEntry),
                "numPackets": flowEntry.numPackets
            }
        }
    ]

    DatabaseConstants.client.write_points(tableEntry)
    # print("Written point")