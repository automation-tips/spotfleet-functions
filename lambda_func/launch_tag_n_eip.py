# -*- coding: utf-8 -*-

# lambda func : LaunchTagAndEIP
# Python version 3.6 ~
# boto version 1.14.x ~

import boto3

client = boto3.client('ec2')


def lambda_handler(event, context):
    # event => {"LaunchedInstance": "id-xxxxxxxxxxs"}
    instance_id = event["LaunchedInstance"]

    # 対象インスタンスにタグを付与
    resp = client.create_tags(
        Resources=[instance_id],
        Tags=[
            {'Key': 'Name', 'Value': 'kento-test'}
        ]
    )

    # 対象のEIP取得
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_addresses
    eip = client.describe_addresses(
        Filters=[
            {
                'Name': 'tag-key',
                'Values': ['Name']
            },
            {
                'Name': 'tag-value',
                'Values': ['kento-test']
            }
        ]
    )

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.associate_address
    client.associate_address(InstanceId=instance_id,
                             AllocationId=eip["Addresses"][0]["AllocationId"])

    return eip


# print(lambda_handler({"LaunchedInstance": "i-xxxxxxxxxxxxxxxx"}, "aaa")) -> END
