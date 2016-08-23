#!/usr/bin/env python

'''
    This script makes AMIs of each instance marked with specific (selector) tag.
    All AMIs creates in a moment without rebooting so you can easily use this
    for backuping your instances. When script creates new AMIs it removes old AMIs. 

    If you have the AWS CLI installed, then you can use it to 
    configure your credentials file:

	># aws configure

	Alternatively, you can create the credential file yourself. 
	By default, its location is at ~/.aws/credentials:

	[default]
	aws_access_key_id = YOUR_ACCESS_KEY
	aws_secret_access_key = YOUR_SECRET_KEY

	Here is your start point if all of this is something new for you:
	http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html
'''

import boto3
import pprint
import json
	
selector_key 	= 'env'
selector_val	= 'prod'
iId 			= '' #instance id
iName 			= ''
keyword			= '. Created by backup script' #This keyword we append to our new Image Name. We use it in cleanOldAMI() as well
clean_all_backups_on_run #Parameter for cleanOldAMI()

client 			= boto3.client('ec2')
response 		= client.describe_instances(Filters=[{'Name':'tag:'+selector_key, 'Values': [selector_val]}])
ownerId			= response['Reservations'][0]['OwnerId']
#ToDo: set ownerId for each instance separately

def getInstancesList(ec2_client):
	'''
		Querying describe_instances with filter by tag and form easy-to-use list
	'''
	list = []
	descrInstResp 	= client.describe_instances(Filters=[{'Name':'tag:'+selector_key, 'Values': [selector_val]}])
	for insts in descrInstResp['Reservations']:
		for inst in insts['Instances']:
			list.append(inst)
	return list

	
def getInstanceName(tags):
	'''
		In case you have a few tags.
	'''
	for tag in tags:
		if tag['Key'] == 'Name':
			return tag['Value']
	return 'Unnamed'

	
def cleanOldAMI(ec2_client, name, ownerId, clean_all_backups_on_run):
	'''
		Delete AMI/AMIs we created last run.
		We don't know ImageID of our AMI so firstly get 
		the ID based on name+keyword pair or, if clean_all_backups_on_run
		is set we're deleteing all AMIs contains keywords in name.
	'''
	if clean_all_backups_on_run:
		name_values = name+keyword
	else:
		name_values = keyword

	all_images = ec2_client.describe_images(Owners=[ownerId], Filters=[{'Name':'name', 'Values':[name+keyword]}])
	for image in all_images['Images']:
		print('Deregistering '+image['ImageId'])
		deregister_result = ec2_client.deregister_image(ImageId=image['ImageId'])
		if (deregister_result['ResponseMetadata']['HTTPStatusCode'] == 200):
			print('Deregistered successfully')
		else:
			print('Something wrong with deregistering: ', deregister_result)
	return None


def createBackupImage(ec2_client, instId, iName):
	try:
		createImageResp = ec2_client.create_image(InstanceId=instId, Name=iName+keyword, NoReboot=True)
	except:
		print("Can't create backup image")
		return 1
	else:
		if(createImageResp['ResponseMetadata']['HTTPStatusCode'] == 200):
			print("Image created sucessfully.")
		else:
			print('Something wrong with creating backup: ', createImageResp)
		return 0


for i in getInstancesList(client):
	iId 	= i['InstanceId']
	iName	= getInstanceName(i['Tags'])
	print('{:<18}  {:>18}  {:>18}  {:>18}  {:>18}  {:>18}  {:>18}'.format( \
		iName, iId, i['InstanceType'], i['KeyName'], \
		i['NetworkInterfaces'][0]['PrivateIpAddress'], \
		i['NetworkInterfaces'][0]['Association']['PublicIp'], \
		i['NetworkInterfaces'][0]['MacAddress']))
	cleanOldAMI(client, iName, ownerId)
	createBackupImage(client, iId, iName)
