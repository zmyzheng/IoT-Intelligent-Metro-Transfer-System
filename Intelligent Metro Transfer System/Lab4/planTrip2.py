import sys
sys.path.append('../utils')
from aws import getResource
from Synthesis import Synthesis
from boto3.dynamodb.conditions import Key,Attr


def planTrip2():
    DYNAMODB_TABLE_NAME = 'mtaData'
    dynamodb = getResource('dynamodb', 'us-east-1')
    table_dynamo = dynamodb.Table(DYNAMODB_TABLE_NAME)


    #step 8
    print 'step 8'
    
    tripId=raw_input('Please type in tripid\n')
    direction=tripId[-1]
    
    if direction=='S':
        
        localTrains =[]
        search = table_dynamo.scan(FilterExpression=Attr('routeId').eq('1') & Attr('direction').eq('S'))
        trainsDict = search['Items']
        for trainDict in trainsDict:
            train = Synthesis()
            train.constructFromDyDict(trainDict)
            #       120S => 96st
            if tripId in train.futureStops and u'120S' in train.futureStops:
                localTrains.append(train)
        print 'there are {0} local train to 96st'.format(len(localTrains))
        
        if len(localTrains) == 0:
            print 'no local train stop at:' + tripId
            return 'no local train stop at:' + tripId
    
        expressTrains = []
        search = table_dynamo.scan(FilterExpression=(Attr('routeId').eq('2') | Attr('routeId').eq('3')) & Attr('direction').eq('S'))
        trainsDict = search['Items']
        for trainDict in trainsDict:
            train = Synthesis()
            train.constructFromDyDict(trainDict)
            if u'120S' in train.futureStops:
                expressTrains.append(train)
        print 'there are {0} express train to 96st'.format(len(expressTrains))
        if len(expressTrains) == 0:
            print 'no express train stop at: 96st, you can only take local train'
            return 'no express train stop at 96st, you can only take local train' 

        nearestTrain_local = None
        nearestTime_local = None
        arrivalTimes_local = [(train.futureStops[u'120S'][0], train) for train in localTrains]
        
        nearestTime_local, nearestTrain_local = min(arrivalTimes_local)
        print 'The eariset local train to 96st arrive at {0}'.format(nearestTime_local)
    
        
        
        nearestTrain_express = None
        nearestTime_express = None
        arrivalTimes_express = [(train.futureStops[u'120S'][0], train) for train in expressTrains if train.futureStops[u'120S'][0] > nearestTime_local]
        
        nearestTime_express, nearestTrain_express = min(arrivalTimes_express)
        print 'The eariset express train to 96st arrive at {0}'.format(nearestTime_express)
    
        
        
        arrival_at_stop42_local = nearestTrain_local.futureStops[u'127S'][0]
        arrival_at_stop42_express = nearestTrain_express.futureStops[u'127S'][0]
        startTime = nearestTrain_local.futureStops[u'117S'][0]
        print 'time taken to reach 42nd by local train is {0}'.format(arrival_at_stop42_local - startTime)
        print 'time taken to reach 42nd by express train is {0}'.format(arrival_at_stop42_express - startTime)
        
        
        if arrival_at_stop42_local - startTime > arrival_at_stop42_express - startTime:
            print 'Switch to Express Train'
            return 'Switch to Express Train'
        else:
            print 'Stay on in the Local Train'
            return 'Stay on in the Local Train'
                
    if direction=='N':
        localTrains1 =[]
        search1= table_dynamo.scan(FilterExpression=Attr('routeId').eq('1') & Attr('direction').eq('N'))
        trainsDict1 = search1['Items']
        for trainDict in trainsDict1:
            train1 = Synthesis()
            train1.constructFromDyDict(trainDict)
            if u'127N' in train1.futureStops:
                localTrains1.append(train1)
        print 'there are {0} local train to 42st'.format(len(localTrains1))
        
        if len(localTrains1) == 0:
            print 'no local train stop at: 42st'
            return 'no local train stop at: 42st'
        
        
        expressTrains2 = []
        search2 = table_dynamo.scan(FilterExpression=(Attr('routeId').eq('2') | Attr('routeId').eq('3')) & Attr('direction').eq('N'))
        trainsDict2 = search2['Items']
        for trainDict in trainsDict2:
            train2 = Synthesis()
            train2.constructFromDyDict(trainDict)
            if u'127N' in train2.futureStops:
                expressTrains2.append(train2)
        print 'there are {0} express train to 42st'.format(len(expressTrains2))
        if len(expressTrains2) == 0:
            print 'no express train stop at: 42st, you can only take local train'
            return 'no express train stop at 42st, you can only take local train' 

        
        
        nearestTrain_local1 = None
        nearestTime_local1= None
        arrivalTimes_local1 = [(train_1.futureStops[u'120N'][0], train_1) for train_1 in localTrains1]
        if len(arrivalTimes_local1) > 0:
            nearestTime_local1, nearestTrain_local1 = min(arrivalTimes_local1)
        print 'The eariset local train to 96st arrive at {0}'.format(nearestTime_local1)
    
        nearestTrain_express2 = None
        nearestTime_express2 = None
        arrivalTimes_express2= [(train_2.futureStops[u'120N'][0], train_2) for train_2 in expressTrains2]
        if len(arrivalTimes_express2) > 0:
            nearestTime_express2, nearestTrain_express2 = min(arrivalTimes_express2)
        print 'The eariset express train to 96st arrive at {0}'.format(nearestTime_express2)
    
        
        if nearestTime_local1 > nearestTime_express2:
            print 'get on the express at 42nd Street'
            return 'get on the express at 42nd Street'
        else:
            print 'get on the local at 42nd Street'
            return 'get on the local at 42nd Street'

            




