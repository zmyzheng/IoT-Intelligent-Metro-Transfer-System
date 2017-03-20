#!/usr/bin/python
import json
import time
import sys
from collections import OrderedDict
from threading import Thread
import boto3
import mraa
import math

sys.path.append('../utils')




### YOUR CODE HERE ####


from aws import getResource
from aws import getClient

if __name__ == '__main__':
    tempSensor = mraa.Aio(1)
    B=4275
    R = (1023.0/tempSensor.read()-1.0) * 100000
    temperature=1.0/(math.log(R/100000.0)/B+1/298.15)-273.15
    client = getClient('sns', 'us-east-1')
    client.publish(TopicArn='arn:aws:sns:us-east-1:547629754253:Demo_Topic',
	    
	    Message='the temperature is'+str(temperature),
	    Subject='temperature',

    )
