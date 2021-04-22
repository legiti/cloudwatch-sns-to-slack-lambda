import logging

from cloudwatch_sns_to_slack.constants import SERVICE_NAME

logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.INFO)

def handler(event, _):
    logger.info('SNS message received')
    logger.info(f'SNS message contents: {event["Records"][0]["Sns"]["Message"]}')
    return True
