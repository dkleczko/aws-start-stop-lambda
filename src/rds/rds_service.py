import boto3
from modules.croniter import croniter
import datetime
from extensions.date_extension import date_extension

class rds_service(object):
    START_RDS_TAG = 'Start'
    STOP_RDS_TAG = 'Stop'
    CHECK_TIME_SEC = 600
    rds = boto3.client('rds')

    def __init__(self, datetime_now):
        self.NOW = datetime_now

    def start_stop_instances(self):
        for db in self.rds.describe_db_instances()['DBInstances']:
            status = db['DBInstanceStatus']
            if(status == 'stopped'):
                self.__make_action_on_instance_by_cron(db, self.START_RDS_TAG, self.__start_instance)
            if(status == 'available'):
                self.__make_action_on_instance_by_cron(db, self.STOP_RDS_TAG, self.__stop_instance)


    def __make_action_on_instance_by_cron(self, db, tag_key, action):
        db_tags = self.__get_tags_for_db(db['DBInstanceArn'])
        tag = next(iter(filter(lambda tag: tag['Key'] == tag_key, db_tags)), None)
        if(tag is not None):
            cron = self.__make_replacement_in_cron(tag['Value'])
            itr = croniter(cron, self.NOW)
            seconds_diff = date_extension.diff_dates_seconds(itr.get_prev(datetime.datetime), self.NOW)
            if(seconds_diff >= 0 and seconds_diff <= self.CHECK_TIME_SEC):
                action(db['DBInstanceIdentifier'])

    def __get_tags_for_db(self, instance_arn):
        instance_tags = self.rds.list_tags_for_resource(ResourceName=instance_arn)
        return instance_tags['TagList']
    
    def __make_replacement_in_cron(self, cron):
        cron = cron.replace('_', '*')
        cron = cron.replace('+', '?')
        cron = cron.replace('.', ',')
        print(cron)
        return cron

    def __start_instance(self, instance_identifier):
        try:
            self.rds.start_db_instance(DBInstanceIdentifier=instance_identifier)
            print(f'Instance stared: {instance_identifier}')
        except Exception as e:
            print(e)
            pass
    def __stop_instance(self, instance_identifier):
        try:
            self.rds.stop_db_instance(DBInstanceIdentifier=instance_identifier)
            print(f'Instance stopped: {instance_identifier}')
        except Exception as e:
            print(e)
            pass
            
