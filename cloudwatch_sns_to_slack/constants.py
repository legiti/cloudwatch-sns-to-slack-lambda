SERVICE_NAME = 'cloudwatch_sns_to_slack'

GENERIC_ERROR_MESSAGE = '*URGENT*: Error generating Slack message body from sns_message. ' \
    f'Check {SERVICE_NAME} logs for details. Something is going wrong but we don\'t know what'

BASE_CLOUDWATCH_ALARM_LINK = "https://sa-east-1.console.aws.amazon.com/cloudwatch/home?region=sa-east-1#alarmsV2:alarm/"

# # Slack channel IDs
# PLATFORM_ALERTS_CHANNEL_ID = 'C0135LF58BH'
# TEST_CHANNEL_ID = 'C01A6H83NKA'

# Add a new channel via Slack here: https://api.slack.com/apps/A01VD8YBR28/incoming-webhooks
CHANNEL_TO_WEBHOOKS_MAP = {
    'platform-alerts': 'https://hooks.slack.com/services/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',
    'test_channel': 'https://hooks.slack.com/services/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',
    'area-51-aws': 'https://hooks.slack.com/services/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'
}
