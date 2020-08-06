# -*- coding: utf-8 -*-

# lambda func : RequestSpotInstance
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.request_spot_instances
# Python version 3.6 ~
# boto version 1.14.x ~

import boto3

# SpotFleet、インスタンスタイプetc設定
spot_price = "0.02"
request_type = "persistent"
# ここではAmazon Linux2 Latest
image_id = "ami-0cc75a8978fbbc969"
# 配列で設定するので複数付与することもできる
security_groups = ["sg-xxxxxxxxxxxxxx"]
incetance_type = "t2.medium"
availability_zone = "ap-northeast-1a"
subnet_id = "subnet-xxxxxxxxx"
key_name = "hoge-key"

client = boto3.client('ec2')


def lambda_handler(event, context):

    # SpotFleetリクエスト
    response = client.request_spot_instances(
        SpotPrice=spot_price,
        InstanceCount=1,
        Type=request_type,
        LaunchSpecification={
            "ImageId": image_id,
            "SecurityGroupIds": security_groups,
            "InstanceType": incetance_type,
            "Placement": {
                "AvailabilityZone": availability_zone
            },
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {
                        # 単位 GB
                        "VolumeSize": 30,
                        # 汎用SSD
                        "VolumeType": "gp2",
                        # インスタンス終了時にEBSも削除する
                        "DeleteOnTermination": True
                    }
                }
            ],
            "SubnetId": subnet_id,
            "KeyName": key_name
        },
        TagSpecifications=[
            {
                "ResourceType": "spot-instances-request",
                # ここに個々人の名前が入るように設定するとか
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'kento-test'
                    },
                ]
            },
        ],
        # 入札金額を下回った場合、停止にする(補足：terminate にすると終了)
        InstanceInterruptionBehavior="stop"
    )

    # ここではリクエストIDだけ撮っているが、レスポンスにはインスタンスIDが含まれるのでインスタンスIDで絞り込んでEIP付与、タグ付与とか色々できる
    # インスタンス作成後の運用はlambdaでタグがついたインスタンスの起動、停止ロジックでOK
    request = {
        "requestId": response['SpotInstanceRequests'][0]["SpotInstanceRequestId"]
    }
    # スポットリクエストID
    # 戻り値例：{"requestId": "sir-bbbbbbb"}
    return request


#print(lambda_handler("ddd", "aaa"))
# next -> 60秒まつ -> GetBiddingResult
