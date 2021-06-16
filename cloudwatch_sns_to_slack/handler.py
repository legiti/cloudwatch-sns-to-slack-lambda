import json
import logging

import requests

from cloudwatch_sns_to_slack.constants import (
    BASE_CLOUDWATCH_ALARM_LINK,
    DEV_SNS_ARN,
    GENERIC_ERROR_MESSAGE,
    HEADERS,
    POST_TO_SLACK_WEBHOOK,
    SERVICE_NAME
)


logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.INFO)

def _safe_get_sns_message_as_json(sns_message):
    return json.loads(sns_message.replace("'", "\"").replace('None', 'null'))


def _get_slack_message_body(sns_message):
    try:
        sns_message_dict = _safe_get_sns_message_as_json(sns_message)
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
        sns_message_dict = _safe_get_sns_message_as_json(sns_message)
        alarm_state = sns_message_dict['NewStateValue']
        return 'danger' if alarm_state == 'ALARM' else 'good'
    except Exception as err:
        logger.error(err)
        return 'danger'


def _post(data):
    response = requests.post(
        POST_TO_SLACK_WEBHOOK,
        headers=HEADERS,
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

        data = {
            'text': '*' + subject + '*',
            'channel': channel,
            'username': 'AWS Notification Bot',
            'icon_emoji': ':gratidão:',
            'attachments': [
                {
                    'text': _get_slack_message_body(sns_message),
                    'color': _get_severity(sns_message)
                }
            ]
        }
        _post(data)

    except Exception as err:
        logger.error(err)
        data = {
            'text': '*' + 'ERROR: unable to post SNS record as Slack message' + '*',
            'channel': '#platform-alerts',
            'username': 'AWS Notification Bot',
            'icon_emoji': ':gratidão:',
            'attachments': [
                {
                    'text': GENERIC_ERROR_MESSAGE,
                    'color': 'danger'
                }
            ]
        }
        _post(data)


def _get_channel(sns_topic_arn):
    if sns_topic_arn == DEV_SNS_ARN:
        logger.info('Message received on dev SNS topic. Will send to #test_channel...')
        return '#test_channel'

    slack_topic_prefix = 'slack-'
    topic_name = sns_topic_arn.split(':')[-1]

    if topic_name[:6] != slack_topic_prefix:
        logger.warning(f'Slack messaging behavior not defined for SNS topic {sns_topic_arn}.')
        logger.info('Will send to #platform-alerts...')
        return '#platform-alerts'

    channel_name = '#' + topic_name.split(slack_topic_prefix)[-1]
    logger.info(f'Will send message to channel {channel_name}')
    return channel_name


def handler(event, _):
    logger.info(f'{event=}')
    for record in event['Records']:
        try:
            sns_topic_arn = record['Sns']['TopicArn']
            logger.info(f'SNS message received on SNS topic {sns_topic_arn}')

            channel = _get_channel(sns_topic_arn)

            _post_message_to_slack(channel, record)
        except Exception:
            # uncomment when developing and comment the last line to spare your friends :)
            # _post_message_to_slack('#test_channel', record)
            _post_message_to_slack('#platform-alerts', record)
