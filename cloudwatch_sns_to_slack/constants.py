SERVICE_NAME = 'cloudwatch-sns-to-slack'

GENERIC_ERROR_MESSAGE = '*URGENT*: Error generating Slack message body from sns_message. ' \
    f'Check {SERVICE_NAME} logs for details. Something is going wrong but we don\'t know what'

BASE_CLOUDWATCH_ALARM_LINK = "https://sa-east-1.console.aws.amazon.com/cloudwatch/home?region=sa-east-1#alarmsV2:alarm/"

HEADERS = {
    'Content-Type': 'application/json',
}

DEV_SNS_ARN = 'arn:aws:sns:sa-east-1:123456789012:test-topic'

S3_BUCKET_NAME = 'com.legiti.cloudwatch-slack-alerts'  # hardcoded in serverless.yml too
