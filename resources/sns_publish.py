import json
import os

import boto3

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_TOPIC_ARN = 'arn:aws:sns:sa-east-1:123456789012:test-topic'
CLOUDWATCH_ALARM_MESSAGE_TEMPLATE = ''
# see https://stackoverflow.com/a/52380239/7560692 for more on SNS Cloudwatch message format
with open(f'{SCRIPT_DIR}/example_cloudwatch_sns_message.json') as json_file:
    CLOUDWATCH_ALARM_MESSAGE_TEMPLATE = json.load(json_file)

sns = boto3.client('sns', endpoint_url='http://127.0.0.1:4002')

sns.publish(TopicArn=DEFAULT_TOPIC_ARN,
            Message=json.dumps(CLOUDWATCH_ALARM_MESSAGE_TEMPLATE),
            Subject='ALARM: "Example alarm name" in South America (Sao Paulo)')
