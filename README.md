# Legiti Python Template

This template repo is meant to be used for helping to set up new repositories, by already setting some things that we end up setting in all our repositories, but also, to provide a checklist of things that should be done before considering a service as being ready to go into production. By having this boilerplate setup we hope to make it easier and quicker for new services to be setup, while also helping maintaining some Legiti repo style, and the checklist should make it clearer and safer to add new services to production.

When creating new repos, you should click the `Use this template` button on this repo's main page in GitHub, and then you only really need to change the places that are marked with the comment `REPO_SETUP:` (ctrl+shift+f will be your friend here). You can remove those comments after setting it up. You should do that in a follow-up PR, so that it's clear what came from the template and what was modified specifically in your new repo.

The structure here should match the general guidelines described in our [development structure doc](https://coda.io/d/Legiti-Backend-and-Data-Science-Development_dZcBe-sb1eb/Development-Structure_surl0#_luyWP). Changes there should be replicated here and vice-versa. Also, any changes to this general structure that starts happening in our repo are encouraged to be brought into this template repository, so that it's always as complete as possible.

There might be exceptions, of course, and not all of this might apply to all services, so not following some of the set up here is up to developers' and PR reviewers' discretion.

## Checklist before going to prod

You should keep this in the README before going to prod. Once all boxes are ticked here, and the service is deployed into prod, feel free to remove it.

- docs:
    - [ ] repo README
    - [ ] [firefighting helper docs](https://coda.io/d/Firefighting-Resources_dPln74ERCm_/Service-Specific-Tips_suMxX#_lup6E)
- CI:
    - [ ] setup the Circle CI project for the repo (through Circle's interface)
        - Should you need any additional Circle environment variables, you should prioritize putting them in our [context](https://app.circleci.com/settings/organization/github/legiti/contexts/4cc59443-f597-4168-94ea-463f79f4bdd3), so that they are shared in our organization, rather than being set per repository
    - [ ] lint, unit and integration tests in all branches except for develop and master (more info on test suites structure [here](https://coda.io/d/Legiti-Backend-and-Data-Science-Development_dZcBe-sb1eb/Test-Suites-Structure_sueoo#_lugDX))
    - [ ] staging deploy + staging end to end tests in develop
    - [ ] prod deploy + prod end to end tests in master
    - [ ] branch protection rules (*)
- prod maintainability:
    - [ ] alarms
    - [ ] Logs Insights queries
    - [ ] add service(s) to [Legiti's architecture diagram](https://coda.io/d/Legiti-Backend-and-Data-Science-Development_dZcBe-sb1eb/Architecture-Diagram_su738#_lubNj)
    - [ ] add service(s) to [Legiti's services overview](https://coda.io/d/Legiti-Backend-and-Data-Science-Development_dZcBe-sb1eb/Services-Overview_sux72#_luqpi)
- [ ] repo should be added to Tech Opportunities Coda doc's GH Sync so that repo's issues get tracked as tech opportunities (feel free to reach out to the doc's maintainer to get help with that)
- [ ] set up dependabot (**)

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
