import ast
import json
import logging

import requests

from cloudwatch_sns_to_slack.constants import (
    BASE_CLOUDWATCH_ALARM_LINK,
    CHANNEL_TO_WEBHOOKS_MAP,
    GENERIC_ERROR_MESSAGE,
    SERVICE_NAME
)


logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.INFO)


def _get_slack_message_body(sns_message):
    try:
        sns_message_dict = ast.literal_eval(sns_message)
        alarm_name_line = f'*Alarm name:* {sns_message_dict["AlarmName"]}'
        alarm_description_line = f'*Alarm Description:* {sns_message_dict["AlarmDescription"]}'
        alarm_state_line = f'*State:* {sns_message_dict["NewStateValue"]}'
        alarm_state_reason_line = f'*State Reason:* {sns_message_dict["NewStateReason"]}'
        alarm_state_change_time_line = f'*State Change Time:* {sns_message_dict["StateChangeTime"]}'
        alarm_link_line = f'*Link*: {BASE_CLOUDWATCH_ALARM_LINK}{sns_message_dict["AlarmName"]}'
        slack_message_body = '\n'.join(
            [
                alarm_name_line,
                alarm_description_line,
                alarm_state_line,
                alarm_state_reason_line,
                alarm_state_change_time_line,
                alarm_link_line,
            ]
        )
        return slack_message_body
    except Exception as err:
        logger.error(err)
        return GENERIC_ERROR_MESSAGE


def _get_severity(sns_message):
    try:
        sns_message_dict = ast.literal_eval(sns_message)
        alarm_state = sns_message_dict['NewStateValue']
        return 'danger' if alarm_state == 'ALARM' else 'good'
    except Exception as err:
        logger.error(err)
        return 'danger'


def _post(channel, headers, data):
    response = requests.post(
        CHANNEL_TO_WEBHOOKS_MAP[channel],
        headers=headers,
        data=json.dumps(data),
    )
    if not response.ok:
        logger.error('Unable to post to Slack...')


def _post_message_to_slack(channel, record):
    try:
        subject = record['Sns']['Subject']
        logger.info(f'{subject=}')
        sns_message = record['Sns']['Message']
        logger.info(f'{sns_message=}')

        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'text': '*' + subject + '*',
            'username': 'AWS Notification Bot',
            'icon_emoji': ':gratidão:',
            'attachments': [
                {
                    'text': _get_slack_message_body(sns_message),
                    'color': _get_severity(sns_message)
                }
            ]
        }
        _post(channel, headers, data)

    except Exception as err:
        logger.error(err)
        data = {
            'text': '*' + 'ERROR: unable to post SNS record as Slack message' + '*',
            'username': 'AWS Notification Bot',
            'icon_emoji': ':gratidão:',
            'attachments': [
                {
                    'text': GENERIC_ERROR_MESSAGE,
                    'color': 'danger'
                }
            ]
        }
        _post(channel, headers, data)


def get_channel(sns_topic_arn):
    return 'test_channel'


def handler(event, _):
    logger.info(f'{event=}')
    try:
        for record in event['Records']:
            sns_topic_arn = event["Records"][0]["Sns"]["TopicArn"]
            logger.info(f'SNS message received on SNS topic {sns_topic_arn}')

            # TODO figure out channel
            channel = get_channel(sns_topic_arn)

            _post_message_to_slack(channel, record)
    except Exception:
        # _post_message_to_slack('platform-alerts', record)
        _post_message_to_slack('test_channel', record)
