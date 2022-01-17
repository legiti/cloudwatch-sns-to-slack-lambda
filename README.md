# Cloudwatch SNS to Slack Lambda

This Lambda is used to send CloudWatch notifications to Slack. Notifications are also persisted to S3 for future analysis. Which channel the message is sent to is determined based on the name of the SNS topic. At the time of writing, SNS topics exist for:
- test_channel
- apps-alerts
- integration-alerts
- mlplatform-alerts
- modelagem-alerts
- sre-alerts
- area-51-aws (deprecated)
- data-quality-alerts
- platform-alerts (deprecated)

If you want to add a new channel, you'll need to:
- Ensure the channel exists in Slack
- Create the corresponding SNS topic via Canaveral (add another module block [here](https://github.com/legiti/canaveral/blob/master/slack_sns_topics/main.tf#L6-L9))
- Update the serverless.yml of this service to listen to the new SNS channel

Any errors or unexpected processing in this Lambda will result in messages being sent to #platform-alerts in Slack.

### Development
Note: this project has been developed and tested with NodeJS 12.22.1

Generally, you'll want to do two things while developing:
- Get the Lambda running locally with a local SNS topic that you can publish events to
- Publish events to the SNS topic to trigger the Lambda

To get the Lambda running for the first time, run `yarn` in the project root to install the necessary dependencies. You'll also need to export a value for `SLACK_WEBHOOK_URL` to your local environment (if you want to actually post to Slack, you'll need to get this value from 1Password).

Then, simply run:
```
make run-dev
```

This will run the Lambda locally as well as create a local SNS topic that you can use to trigger the Lambda.

To publish to the SNS topic, you'll probably want to use the `resources/sns_publish.py` script (requirements in `requirements-dev.txt` in project root). Feel free to modify `resources/example_cloudwatch_sns_message.json` as you please (changes will be ignored), and then publish the message to the local SNS topic via
```
make sns-publish
```

This service does not have integration or E2E tests.

## CI
There is no Staging version (or `develop` branch) of this service. Merges to `main` are automatically deployed via CircleCI.
