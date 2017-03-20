# *********************************************************************************************
# Usage python mta.py

import json,time,csv,sys

import boto3
from boto3.dynamodb.conditions import Key,Attr

sys.path.append('../utils')
import aws
import snsService
import planTrip


DYNAMODB_TABLE_NAME = "mtaData"

# prompt
def prompt():
    print "please input command: "
    print ">Available Commands are : "
    print "1. plan trip"
    print "2. subscribe to messages"
    print "3. exit"

def main():
    prompt()
    menu = input()


    while menu != 3:
        if menu == 1:
            message = planTrip.planTrip()
            snsService.publishSMS(message)


        elif menu == 2:
            phone = raw_input("input your phone number:")
            print "your phone is "+ phone
            snsService.subsrcibeSnsService(phone)

        prompt()
        menu = input()

if __name__ == "__main__":
    main()


