from unittest.mock import patch, Mock, call

from cloudwatch_sns_to_slack import handler, constants


SNS_ARN_PREFIX = 'arn:aws:sns:sa-east-1:123456789012:'


def test_get_slack_message_body_error_handling():
    assert handler._get_slack_message_body('this is not a cloudwatch message') == constants.GENERIC_ERROR_MESSAGE


def test_get_severity_error_handling():
    assert handler._get_severity('this is not a cloudwatch message') == 'danger'


def test_post_to_slack_with_exception_constructing_body():
    with patch('cloudwatch_sns_to_slack.handler._get_slack_message_body', Mock(side_effect=Exception)), \
         patch('cloudwatch_sns_to_slack.handler._post', Mock()) as post_mock:
        handler._post_message_to_slack(channel='some_channel', record='this is not a cloudwatch message')
    assert post_mock.assert_called_once


def test_get_channel_for_non_conforming_sns_topicl():
    assert handler._get_channel(f'{SNS_ARN_PREFIX}foo') == '#sre-alerts'


def test_get_channel_for_sns_channel():
    assert handler._get_channel(f'{SNS_ARN_PREFIX}slack-foo') == '#foo'


def test_post_message_for_each_record_in_event():
    mock_cloudwatch_event_1 = {
        'Sns': {
            'TopicArn': 'some arn',
            'Subject': 'Hurgadurga',
            'Message': 'See subject'
        }
    }
    mock_cloudwatch_event_2 = {
        'Sns': {
            'TopicArn': 'some arn',
            'Subject': 'Hurgadurga2',
            'Message': 'See subject'
        }
    }
    mock_cloudwatch_sns_event = {'Records': [mock_cloudwatch_event_1, mock_cloudwatch_event_2]}

    with patch('cloudwatch_sns_to_slack.handler._post_message_to_slack', Mock()) as post_message_to_slack_mock, \
         patch('cloudwatch_sns_to_slack.handler._upload_to_s3', Mock()):
        handler.handler(mock_cloudwatch_sns_event, None)

    post_message_to_slack_mock.assert_has_calls([
        call('#sre-alerts', mock_cloudwatch_event_1),
        call('#sre-alerts', mock_cloudwatch_event_2)
    ])
