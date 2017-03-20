# Creating aws machine learning model
# This program uploads the finalData.csv file to S3, and used it as a data source to train a binary 
# classification model
import time,sys,random

import boto3

import S3

sys.path.append('../utils')
import aws

TIMESTAMP  =  time.strftime('%Y-%m-%d-%H-%M-%S')
S3_BUCKET_NAME = 'mtaedisondatagzsl'
S3_FILE_NAME = 'finalData.csv'
S3_URI = "s3://{0}/{1}".format(S3_BUCKET_NAME, S3_FILE_NAME)
DATA_SCHEMA = "aml.csv.schema"


#client.upload_file('finalData.csv', S3_BUCKET_NAME, S3_FILE_NAME)
s3Class = S3.S3(S3_FILE_NAME)
s3Class.uploadData()

client = aws.getClient('machinelearning', 'us-east-1')
dataSource = client.create_data_source_from_s3(
        DataSourceId='dataSource3',
        DataSpec={
                'DataLocationS3': S3_URI,
                'DataSchema': open(DATA_SCHEMA).read()
                
                },
        ComputeStatistics=True

        )

mlModel = client.create_ml_model(
    MLModelId='mlModel3',
    MLModelType='BINARY',
    TrainingDataSourceId = dataSource['DataSourceId'],
)










