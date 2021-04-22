#### Base

# REPO_SETUP: set your project name below
project_name = YOUR_PROJECT_NAME_HERE
docker_run = docker run -it $(project_name)
docker_run_python = docker run -it $(project_name) python -m

# REPO_SETUP: you might want to use docker-compose instead, feel free to change it to docker compose, you'll just need
# to pass those same build-args to your docker-compose services.
docker-build:
	export DOCKER_BUILDKIT=1; docker build  \
		--build-arg PROJECT_NAME=$(project_name) \
		--build-arg PYPI_USER=${PYPI_USER} \
		--build-arg PYPI_PASSWORD=${PYPI_PASSWORD} \
		-t $(project_name) \
		-f Dockerfile \
		.

#### Lint

.SILENT lint: docker-build
	echo ">>> LINTING FILES (with flake8)..."
	$(docker_run)  bash -c "flake8 . || exit 1" || exit 1

	echo ">>> LINTING SRC FILES (with pylint)..."
	$(docker_run) bash -c \
		"find /$(project_name) -name '*.py' |  grep -v 'test' |  xargs pylint --rcfile /$(project_name)/.pylintrc || exit 1" || \
		exit 1

	echo ">>> LINTING TEST FILES (with pylint)..."
	$(docker_run) bash -c \
		"find /$(project_name)/tests -name '*.py' |  xargs pylint --rcfile /$(project_name)/tests/.pylintrc || exit 1" || \
		exit 1

	echo "Yay! Your code is squeaky clean :)"

#### Tests

unit-test: docker-build
	# REPO_SETUP: if your repo is a package and you change the name of the `src` directory, you must update it here as
	# well, after --cov
	$(docker_run_python) pytest -s --cov-report term-missing --cov=src tests/unit/

integration-test: docker-build
	# REPO_SETUP: if your repo is a package and you change the name of the `src` directory, you must update it here as
	# well, after --cov
	$(docker_run_python) pytest -s --cov-report term-missing --cov=src tests/integration/

test: unit-test integration-test

#### Local development

run-dev:
	# REPO_SETUP: add this

#### Dev helpers

# REPO_SETUP: if you have any commands that can be helpful for devving, you may add them here

#### Package publishing

# REPO_SETUP: you may remove this entire section in case your repo is not for a Python package

package-clean:
	rm -rf build
	rm -rf dist
	rm -rf area_51.egg-info

build-package: package-clean
	python setup.py sdist bdist_wheel

dev-build-package: package-clean
	python setup.py sdist bdist_wheel --dev

publish:
	python -m twine upload -u $(PYPI_USER) -p $(PYPI_PASSWORD) --repository-url https://pypi.lgtcdn.net dist/*
