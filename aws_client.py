import boto3
from boto3.session import Session
import os
import warnings


SWITCH_MESSAGE_FORMAT = 'Switch to {: <14} of {}'


def init_origin_credentials():
    oc = {}
    oc['AccessKeyId']     = os.environ['AWS_ACCESS_KEY_ID']
    oc['SecretAccessKey'] = os.environ['AWS_SECRET_ACCESS_KEY']
    oc['SessionToken']    = os.environ['AWS_SESSION_TOKEN']

    return oc


def prepare_client(origin_credentials, region, service):
    warnings.filterwarnings("ignore", category=ResourceWarning)
    print(SWITCH_MESSAGE_FORMAT.format(region, 'origin'))

    credentials = origin_credentials
    client = boto3.client(
        service,
        aws_access_key_id =     credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token =     credentials['SessionToken'],
        region_name = region
    )
    return client


def switch_role(origin_credentials, account, role, region, service):
    warnings.filterwarnings("ignore", category=ResourceWarning)
    print(SWITCH_MESSAGE_FORMAT.format(region, account))

    session = Session(
        aws_access_key_id =     origin_credentials['AccessKeyId'],
        aws_secret_access_key = origin_credentials['SecretAccessKey'],
        aws_session_token =     origin_credentials['SessionToken']
        )

    sts = session.client('sts')
    roleArn = 'arn:aws:iam::' + account + ':role/' + role
    result = sts.assume_role(RoleArn=roleArn, RoleSessionName='testtet')
    credentials = result['Credentials']

    client = boto3.client(
        service,
        aws_access_key_id =     credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token =     credentials['SessionToken'],
        region_name = region
    )
    return client
