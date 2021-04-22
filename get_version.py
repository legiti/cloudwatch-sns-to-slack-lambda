# REPO_SETUP: if your repo does not pubilsh a Docker image, you may remove this file

import os
from argparse import ArgumentParser

import boto3
import git
from packaging.version import Version, InvalidVersion

PARSER = ArgumentParser()
PARSER.add_argument("--prod", action='store_true', default=False)
ARGS = PARSER.parse_args()


def get_latest_git_tag(repo):
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)

    if tags:
        latest_tag = str(tags[-1])
    else:
        latest_tag = '0.0.0'

    return latest_tag


def get_all_ecr_tags(next_token, tags):
    if next_token is None:
        return tags

    params = {
        'registryId': '495260634483',
        # REPO_SETUP: fill out the placeholder in the line below
        'repositoryName': 'placeholder',
        'maxResults': 10,
        'filter': {
            'tagStatus': 'TAGGED'
        }
    }
    if next_token != '':
        params['nextToken'] = next_token

    client = boto3.client('ecr')
    response = client.list_images(**params)

    for image in response['imageIds']:
        tag = image['imageTag']
        if 'SNAPSHOT' not in tag:  # SNAPSHOT identifies non-prod tags
            try:
                tags.append(Version(tag))
            except InvalidVersion:
                pass

    return get_all_ecr_tags(response.get('nextToken'), tags)


def get_latest_ecr_tag():
    parsed_tags = get_all_ecr_tags(next_token='', tags=[])
    if parsed_tags:
        latest_tag = str(sorted(parsed_tags)[-1])
    else:
        latest_tag = '0.0.0'

    return latest_tag


def check_for_local_repo_changes(repo):
    if repo.is_dirty(untracked_files=True):
        raise Exception('Aborting publication - please remove local uncommitted changes or commit them and try again.')


def push_tag_to_repo(repo, version):
    repo.config_writer().set_value("user", "name", "Publishing").release()
    repo.config_writer().set_value("user", "email", "publishing@legiti.com").release()
    tag = repo.create_tag(version, message=f'Automatic tag "{version}"')
    print(f'Pushing tag for {version}')
    repo.remotes.origin.push(tag)


def set_version_environment_variable(version):
    bash_env_filename = os.getenv('BASH_ENV')

    with open(bash_env_filename, 'a') as bash_env_file:
        bash_env_file.write(f'export VERSION="{version}"')


def get_version():
    repo = git.Repo(search_parent_directories=True)

    check_for_local_repo_changes(repo)

    latest_docker_registry_version = get_latest_ecr_tag()
    upgraded_docker_registry_version = '.'.join(latest_docker_registry_version.split('.')[:-1] +
                                                [str(int(latest_docker_registry_version.split('.')[-1]) + 1)])
    latest_git_tag = get_latest_git_tag(repo)

    version = latest_git_tag if Version(latest_git_tag) > Version(latest_docker_registry_version) \
        else upgraded_docker_registry_version

    print(f'New version tag is {version}')
    set_version_environment_variable(version)

    if ARGS.prod and version != latest_git_tag:
        push_tag_to_repo(repo, version)
    return version


if __name__ == '__main__':
    get_version()
