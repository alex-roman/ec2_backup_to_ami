# ec2_backup_to_ami
Backup your AWS EC2 instances to AMI based on tags.

This is python script that utilize boto3 to create AMI of your instances. 
Set tag-value pair to select instances and run script in cron. 
It creates images without reboot so you production and night dreams will not be affected.
Also it deletes old AMI before creating a new ones.

If you have the AWS CLI installed, then you can use it to
configure your credentials file:

    ># aws configure

Alternatively, you can create the credential file yourself.
By default, its location is at ~/.aws/credentials:

    [default]
    aws_access_key_id = YOUR_ACCESS_KEY
    aws_secret_access_key = YOUR_SECRET_KEY

Here is your start point if all this is something new for you:
http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html
