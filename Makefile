#### Base

project_name = cloudwatch-sns-to-slack-lambda
docker_run = docker run -it $(project_name)
docker_run_python = docker run -it $(project_name) python -m

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
	$(docker_run_python) pytest -s --cov-report term-missing --cov=cloudwatch_sns_to_slack tests/unit/

integration-test: docker-build
	$(docker_run_python) pytest -s --cov-report term-missing --cov=cloudwatch_sns_to_slack tests/integration/

test: unit-test integration-test

#### Local development

run-dev:
	# REPO_SETUP: add this

#### Dev helpers
