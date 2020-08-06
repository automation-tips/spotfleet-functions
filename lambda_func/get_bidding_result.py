# -*- coding: utf-8 -*-

# lambda func : GetBiddingResult

import boto3

ec2 = boto3.client('ec2')


def lambda_handler(event, context):

    # 例：{"requestId": "sir-xxxxx"}
    request_id = event['requestId']

    spot_response = ec2.describe_spot_instance_requests(
        SpotInstanceRequestIds=[request_id]
    )

    spot_request = spot_response["SpotInstanceRequests"][0]

    if "InstanceId" in spot_request:
        response = {"LaunchedInstance": spot_request["InstanceId"]}

    else:
        response = {"LaunchedInstance": "0"}

    return response


#event = {'requestId': "sir-xxxxx"}
#print(lambda_handler(event, "hoge"))
# next (return 0) -> オンデマンド起動のやつ
# next -> LaunchTagAndEIP
