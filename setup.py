# REPO_SETUP: you may remove this file in case your repo is not for a Python package

import os
import sys

import git
import requests
import setuptools
from packaging.version import Version

REQUIREMENTS = [
    # REPO_SETUP: add your requirements here
]

PYPI_USER = os.getenv('PYPI_USER')
PYPI_PASSWORD = os.getenv('PYPI_PASSWORD')

# REPO_SETUP: fill out YOUR_PACKAGE_NAME_HERE in the line below. You should change the `src` directory's name to that
# as well
PACKAGE_NAME = 'YOUR_PACKAGE_NAME_HERE'

dev = False

if '--dev' in sys.argv:
    dev = True
    sys.argv.remove('--dev')


def get_latest_git_tag(repo):
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)

    if tags:
        latest_tag = str(tags[-1])
    else:
        latest_tag = '0.0.0'

    return latest_tag


def get_latest_pypi_tag():
    response = requests.get(url=f'https://{PYPI_USER}:{PYPI_PASSWORD}@pypi.lgtcdn.net/simple/{PACKAGE_NAME}/json/')
    if response.status_code == 404:
        return '0.0.0'
    tag = response.json()['urls'][0]['filename'].split(f'{PACKAGE_NAME}-')[1].split('-')[0].split('.tar')[0]
    return tag


def write_version_to_init(version):
    with open(f'{PACKAGE_NAME}/__init__.py', 'w') as init_file:
        init_file.write(f'__version__ = "{version}"\n')


def check_for_local_repo_changes(repo):
    if repo.is_dirty(untracked_files=True):
        raise Exception('Aborting publication - please remove local uncommitted changes or commit them and try again.')


def push_tag_to_repo(repo, version):
    repo.config_writer().set_value("user", "name", "Publishing").release()
    repo.config_writer().set_value("user", "email", "publishing@legiti.com").release()
    tag = repo.create_tag(version, message=f'Automatic tag "{version}"')
    print(f'Pushing tag for {version}')
    repo.remotes.origin.push(tag)


def get_version():
    repo = git.Repo(search_parent_directories=True)
    check_for_local_repo_changes(repo)

    latest_pypi_version = get_latest_pypi_tag()
    upgraded_pypi_version = '.'.join(latest_pypi_version.split('.')[:-1] + [str(int(latest_pypi_version.split('.')[-1]) + 1)])
    latest_git_tag = get_latest_git_tag(repo)

    version = latest_git_tag if Version(latest_git_tag) > Version(latest_pypi_version) else upgraded_pypi_version

    if dev:
        sha = repo.head.object.hexsha
        short_sha = repo.git.rev_parse(sha, short=7)
        short_sha_as_integers = ''.join([str(ord(char)) for char in short_sha])

        version_pieces = version.split('.')
        patch_version = version_pieces[-1]
        version_without_patch = '.'.join(version_pieces[:-1])

        version = version_without_patch + '.dev' + patch_version + short_sha_as_integers
    elif version != latest_git_tag:
        push_tag_to_repo(repo, version)

    print(f'New version tag is {version}')
    write_version_to_init(version)

    return version


version = get_version()
setuptools.setup(
    name=PACKAGE_NAME,
    version=version,
    packages=setuptools.find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
)
print(version)
