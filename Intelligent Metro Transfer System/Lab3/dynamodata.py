#!/usr/bin/python
import json
import time
import sys
from collections import OrderedDict
from threading import Thread
import boto3
from boto3.dynamodb.conditions import Key,Attr

sys.path.append('../utils')
import tripupdate
import mtaUpdates
import datetime



### YOUR CODE HERE ####
import boto
import boto.dynamodb2
from boto.dynamodb2.table import Table

import threading
import time

from aws import getResource
from aws import getClient

TIME_INTERVAL_ADD = 30
TIME_INTERVAL_CLEAN = 60
DYNAMODB_TABLE_NAME = 'mtaData'

def thread_add_data():
    
    
    # TODO: add data here
    dynamodb = getResource('dynamodb', 'us-east-1')
    table_dynamo = dynamodb.Table(DYNAMODB_TABLE_NAME)

    
    print "add data thread start"
    i = 0
    while True:
    # TODO: add data here
        newmat = mtaUpdates.mtaUpdates('49366f59360e776881a0172d90ed32ee')
        tripUpdates = newmat.getTripUpdates()
        j = 0
        for update in tripUpdates:
            #if table_dynamo.get_item(tripId = str(update.tripId)) == None:
            table_dynamo.put_item(Item={
                'tripId': str(update.tripId),
                'routeId': str(update.routeId),
                'startDate': str(update.startDate),
                'direction': str(update.direction),
                'futureStops' : str(update.futureStops),
                'timestamp' : update.timeStamp,
                'currentStopId' : str(update.currentStopId),
                'currentStopStatus' : str(update.currentStopStatus),
                'vehicleTimeStamp' : str(update.vehicleTimeStamp),
            })
            j = j + 1
            #print j

        

        print "I have added data for {0} times".format(i)
        time.sleep(TIME_INTERVAL_ADD)
        i += 1


def thread_clear_data():
    
    
    # TODO: clean data here
    dynamodb = getResource('dynamodb', 'us-east-1')
    table_dynamo = dynamodb.Table(DYNAMODB_TABLE_NAME)

    print "delete data thread start"
    i = 0
    while True:
        # TODO: add data here
        diff=int(time.time()-120)
        search=table_dynamo.scan(FilterExpression=Attr('timestamp').lt(diff))
        items=search['Items']
        #print items


        # newmat = mtaUpdates.mtaUpdates('49366f59360e776881a0172d90ed32ee')
        # tripUpdates = newmat.getTripUpdates()
        # usefuldata=table_dynamo.scan()
        for update in items:
            #print 1
        #     print(json.dumps(update, cls=DecimalEncoder))
            
            table_dynamo.delete_item(
                Key={'tripId':update['tripId']})

        print "I have cleaned data for {0} times".format(i)
        time.sleep(TIME_INTERVAL_CLEAN)
        i += 1

if __name__ == '__main__':
    # TODO: error handle
    client = getClient('dynamodb', 'us-east-1')
    dynamodb = getResource('dynamodb', 'us-east-1')
    table_dynamo = dynamodb.Table(DYNAMODB_TABLE_NAME)

    response = client.list_tables()
    tablelist = response['TableNames']
    if DYNAMODB_TABLE_NAME in tablelist:
        response = client.delete_table(TableName=DYNAMODB_TABLE_NAME)
        #table_dynamo.delete()
        table_dynamo.wait_until_not_exists()

    dynamodb.create_table(
        TableName=DYNAMODB_TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'tripId',
                'KeyType': 'HASH'  #Partition key
            },
            
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'tripId',
                'AttributeType': 'S'
            },
            

        ],
        ProvisionedThroughput=
            {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
  
    )

    table_dynamo.wait_until_exists()
    # start threads
    t_add = threading.Thread(target=thread_add_data)
    t_clean = threading.Thread(target=thread_clear_data)
    t_add.setDaemon(True)
    t_clean.setDaemon(True)
    t_add.start()
    t_clean.start()

    while True:
        time.sleep(5)
