import json
import boto3
import datetime
from ec2.ec2_service import ec2_service
from rds.rds_service import rds_service

def run(event, context):
    datetime_now = datetime.datetime.utcnow()
    ec2_serv = ec2_service(datetime_now)
    rds_serv = rds_service(datetime_now)
    rds_serv.start_stop_instances()
    ec2_serv.start_instances()
    ec2_serv.stop_instances()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


    