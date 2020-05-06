# AWS Start stop lambda

AWS Start stop lambda is tags based automation tool which starts&stops services. Thanks for this you can cut costs by stopping services during non business hours.
Services supported:
  - EC2
  - RDS
### Tech
* Python 3.8
* boto3
* croniter
* serverless

### AWS Installation
* install and conrifure [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
* install [Serverless framework](https://www.serverless.com/framework/docs/getting-started/)
* Run in src folder
```sh
$ serverless deploy
```
### Configuration
* You can configure tags names which will be used in each service. To do it please edit rds_service.py START_RDS_TAG & STOP_RDS_TAG or ec2_service.py START_EC2_TAG & STOP_EC2_TAG.
* CHECK_TIME_SEC is set to 600 seconds by default. It's twice as much as current lambda cron.
* Cron in EC2 tags is in standard format
* Cron in RDS tags is more complicated because it doesn't allows few standard cron characters. Our software has to do some replacement to get proper cron. In tags please use:
'_' instad of '*', '+' instad of '?', '.' instead of ',' in example 45 16 _ _ _

### Todos
* Cron based instances resize

License
----

MIT
