SERVICE_NAME = 'cloudwatch-sns-to-slack'

GENERIC_ERROR_MESSAGE = '*URGENT*: Error generating Slack message body from sns_message. ' \
    f'Check {SERVICE_NAME} logs for details. Something is going wrong but we don\'t know what'

BASE_CLOUDWATCH_ALARM_LINK = "https://sa-east-1.console.aws.amazon.com/cloudwatch/home?region=sa-east-1#alarmsV2:alarm/"

HEADERS = {
    'Content-Type': 'application/json',
}

# # Slack channel IDs
# PLATFORM_ALERTS_CHANNEL_ID = 'C0135LF58BH'
# TEST_CHANNEL_ID = 'C01A6H83NKA'

POST_TO_SLACK_WEBHOOK = 'https://hooks.slack.com/services/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'

DEV_SNS_ARN = 'arn:aws:sns:sa-east-1:123456789012:test-topic'

# Add a new channel via Slack here: https://api.slack.com/apps/A01VD8YBR28/incoming-webhooks
# CHANNEL_TO_WEBHOOKS_MAP = {
#     'platform-alerts': 'https://hooks.slack.com/services/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',
#     'test_channel': 'https://hooks.slack.com/services/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',
#     'area-51-aws': 'https://hooks.slack.com/services/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'
# }
