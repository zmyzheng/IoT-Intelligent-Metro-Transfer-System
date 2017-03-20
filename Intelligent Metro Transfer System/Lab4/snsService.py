#!/usr/bin/python
import json
import time
import sys
from collections import OrderedDict
from threading import Thread
import boto3


sys.path.append('../utils')




### YOUR CODE HERE ####


from aws import getResource
from aws import getClient
import time

def subsrcibeSnsService(phone):
    # TODO: error handle
    client = getClient('sns', 'us-east-1')
    response = client.create_topic(Name='hw4Topic')
    topicArn = response['TopicArn']
 #    response = client.subscribe(
	#     TopicArn=topicArn,
	#     Protocol='email',
	#     Endpoint='zhengzmy@gmail.com'
	# )

    response = client.subscribe(TopicArn=topicArn,Protocol='sms',Endpoint=phone)
    

    client.publish(TopicArn=topicArn,
	    
	    Message='you have subscribed',
	    Subject='Subscribe to message feed',

    )


def publishSMS(message):
    client = getClient('sns', 'us-east-1')
    response = client.create_topic(Name='hw4Topic')
    topicArn = response['TopicArn']
    client.publish(TopicArn=topicArn,
        
        Message=message,
        Subject='Subscribe to message feed',

    )
