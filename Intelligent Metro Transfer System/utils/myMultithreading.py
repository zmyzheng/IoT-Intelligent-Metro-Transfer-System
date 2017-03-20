#!/usr/bin/python

import boto
import boto.dynamodb2
from boto.dynamodb2.table import Table

import threading
import time



TIME_INTERVAL_ADD = 3
TIME_INTERVAL_CLEAN = 6


def thread_add_data():
    print "add data thread start"
    i = 0
    while True:
        # TODO: add data here

        print "I have added data for {0} times".format(i)
        time.sleep(TIME_INTERVAL_ADD)
        i += 1


def thread_clear_data():
    print "clear data thread start"
    i = 0
    while True:
        # TODO: clean data here

        print "I have cleaned data for {0} times".format(i)
        time.sleep(TIME_INTERVAL_CLEAN)
        i += 1

if __name__ == '__main__':
    # TODO: error handle
    ACCOUNT_ID = '547629754253'
    IDENTITY_POOL_ID = 'us-east-1:46234eb7-5e0a-48ae-b309-7e1f364f7c68'
    ROLE_ARN ='arn:aws:iam::547629754253:role/Cognito_EdisonAppUnauth_Role'
    # Use cognito to get an identity.
    cognito = boto.connect_cognito_identity()
    cognito_id = cognito.get_id(ACCOUNT_ID, IDENTITY_POOL_ID)
    oidc = cognito.get_open_id_token(cognito_id['IdentityId'])
     
    # Further setup your STS using the code below
    sts = boto.connect_sts()
    assumedRoleObject = sts.assume_role_with_web_identity(ROLE_ARN, "XX", oidc['Token'])

    DYNAMODB_TABLE_NAME = 'mtaData'
    # Prepare DynamoDB client
    client_dynamo = boto.dynamodb2.connect_to_region(
        'us-east-1',
        aws_access_key_id=assumedRoleObject.credentials.access_key,
        aws_secret_access_key=assumedRoleObject.credentials.secret_key,
        security_token=assumedRoleObject.credentials.session_token)

    table_dynamo = Table(DYNAMODB_TABLE_NAME, connection=client_dynamo)

    # start threads
    t_add = threading.Thread(target=thread_add_data)
    t_clean = threading.Thread(target=thread_clear_data)
    t_add.setDaemon(True)
    t_clean.setDaemon(True)
    t_add.start()
    t_clean.start()

    while True:
        time.sleep(5)
