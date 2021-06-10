# Cloudwatch SNS to Slack Lambda

This Lambda is used to send CloudWatch notifications to Slack. Which channel the message is sent to is determined based on the name of the SNS topic. At the time of writing, SNS topics exist for:
- test_channel
- platform-alerts
- area-51-aws
- data-quality-alerts

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

To get the Lambda running for the first time, run `yarn` in the project root to install the necessary dependencies. Then, simply run:
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

## Checklist before going to prod

You should keep this in the README before going to prod. Once all boxes are ticked here, and the service is deployed into prod, feel free to remove it.

- docs:
    - [x] repo README
    - [ ] [firefighting helper docs](https://coda.io/d/Firefighting-Resources_dPln74ERCm_/Service-Specific-Tips_suMxX#_lup6E)
- CI:
    - [x] setup the Circle CI project for the repo (through Circle's interface)
        - Should you need any additional Circle environment variables, you should prioritize putting them in our [context](https://app.circleci.com/settings/organization/github/legiti/contexts/4cc59443-f597-4168-94ea-463f79f4bdd3), so that they are shared in our organization, rather than being set per repository
    - [x] lint, unit and integration tests in all branches except for develop and master (more info on test suites structure [here](https://coda.io/d/Legiti-Backend-and-Data-Science-Development_dZcBe-sb1eb/Test-Suites-Structure_sueoo#_lugDX))
    - [-] staging deploy + staging end to end tests in develop
    - [x] prod deploy + prod end to end tests in master
    - [x] branch protection rules (*)
- prod maintainability:
    - [ ] alarms
    - [ ] Logs Insights queries
    - [-] add service(s) to [Legiti's architecture diagram](https://coda.io/d/Legiti-Backend-and-Data-Science-Development_dZcBe-sb1eb/Architecture-Diagram_su738#_lubNj)
    - [ ] add service(s) to [Legiti's services overview](https://coda.io/d/Legiti-Backend-and-Data-Science-Development_dZcBe-sb1eb/Services-Overview_sux72#_luqpi)
- [-] repo should be added to Tech Opportunities Coda doc's GH Sync so that repo's issues get tracked as tech opportunities (feel free to reach out to the doc's maintainer to get help with that)
- [x] set up dependabot (**)

(*) Branch protection rules that should be set:
    - for `develop` (if your repo won't have a `develop` branch, these should be applied to `master`):
        - check `Require pull request reviews before merging`
            - below that, check `Dismiss stale pull request approvals when new commits are pushed`
        - check `Require status checks to pass before merging`
            - below that, check `Require branches to be up to date before merging`
            - below that, check `check-branch-name`
            - below that, check `lint-unit-test-integration-test`, or however you've named your Circle workflow that runs those things
        - check `Require linear history`
        - check `Include administrators`
    - for `master`:
        - check `Require status checks to pass before merging`
            - below that, check `staging-deploy` and `staging-e2e`, or however you've named your staging deploy and E2E tests Circle workflows
        - check `Include administrators`

(**) Note that, at the time of writing this, if your service uses packages from our private PyPI repository, you need to use Dependabot's legacy setup. If you need help on this, you can check how our other repos have set up Dependabot.
