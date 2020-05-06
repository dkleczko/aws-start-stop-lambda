import boto3
import datetime
from modules.croniter import croniter
from extensions.date_extension import date_extension


class ec2_service(object):
    START_EC2_TAG = 'Start'
    STOP_EC2_TAG = 'Stop'
    CHECK_TIME_SEC = 600
    ec2 = boto3.client('ec2')

    def __init__(self, datetime_now):
        self.NOW = datetime_now

    def start_instances(self):
        reservations = self.__get_instance_reservations(self.START_EC2_TAG, 'stopped')
        self.__make_action_on_instance_by_cron(reservations, self.START_EC2_TAG, self.__start_instance)


    def stop_instances(self):
        reservations = self.__get_instance_reservations(self.STOP_EC2_TAG, 'running')
        self.__make_action_on_instance_by_cron(reservations, self.STOP_EC2_TAG, self.__stop_instance)

    def __make_action_on_instance_by_cron(self,reservations, cron_tag, action):
        for reservation in reservations:
            for instance in reservation['Instances']:
                cron = self.__get_tag_value(instance['Tags'], cron_tag)
                instanceId = instance['InstanceId']
                itr = croniter(cron, self.NOW)
                seconds_diff = date_extension.diff_dates_seconds(itr.get_prev(datetime.datetime), self.NOW)
                if(seconds_diff >= 0 and seconds_diff <= self.CHECK_TIME_SEC):
                    action(instanceId)

    def __stop_instance(self, instanceId):
        try:
            self.ec2.stop_instances(
                    InstanceIds=[
                        instanceId
                    ])
            print(f'Instance stopped: {instanceId}')
        except Exception as e:
            print(e)
            pass

    def __get_instance_reservations(self,tag, state):
        filters = [{
            'Name': f'tag:{tag}',
            'Values': ['*']},
            {
            'Name': 'instance-state-name'  ,
            'Values': [state]  
            }]
        return self.ec2.describe_instances(Filters=filters)['Reservations']

    def __start_instance(self, instanceId):
        try:
            self.ec2.start_instances(
                    InstanceIds=[
                        instanceId
                    ])
            print(f'Instance stared: {instanceId}')
        except Exception as e:
            print(e)
            pass
            

    def __get_tag_value(self, tagList, tagName):
        for tag in tagList:
            if(tag['Key'] == tagName):
                return tag['Value']
        return ''
