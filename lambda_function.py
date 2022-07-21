import os
import json
import boto3
print('Loading function')
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    target_bucket = os.environ.get('destination_s3')
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    key = key.replace("+", " ")
    copy_source = {'Bucket':source_bucket, 'Key':key}
    prefix = os.environ.get('destination_prefix')
    keydest = prefix + (key[key.rfind("/")+1:]).replace(" ", "_")
    print ('Key:',key)
    print (keydest)
    sts_client = boto3.client('sts')
    assumedRoleObject=sts_client.assume_role (
        RoleArn="arn:aws:iam::007712106137:role/crossaccount-autoreplication-lambda-assume-role",
        RoleSessionName="AssumeRoleSession1"
        )
    credentials=assumedRoleObject['Credentials']
    s3 = boto3.client(
        's3',
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken'],
        )
    
    
    print ("Copying %s from bucket %s to bucket %s …" % (keydest, source_bucket, target_bucket))    
    s3.copy(Bucket=target_bucket, Key=keydest, CopySource=copy_source)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from s3 crossaccreplication Lambda!')
    }
