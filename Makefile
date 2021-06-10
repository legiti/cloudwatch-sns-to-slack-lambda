#### Base

project_name = cloudwatch_sns_to_slack
docker_run_tests = docker run -it $(project_name)
docker_run_tests_python = docker run -it $(project_name) python -m

docker-build-test-image:
	export DOCKER_BUILDKIT=1; docker build  \
		--build-arg PROJECT_NAME=$(project_name) \
		--build-arg PYPI_USER=${PYPI_USER} \
		--build-arg PYPI_PASSWORD=${PYPI_PASSWORD} \
		-t $(project_name) \
		-f Dockerfile.test \
		.

#### Lint

.SILENT lint: docker-build-test-image
	echo ">>> LINTING FILES (with flake8)..."
	$(docker_run_tests)  bash -c "find . -name '*.py' |  grep -v 'node_modules' | xargs flake8 || exit 1" || exit 1

	echo ">>> LINTING SRC FILES (with pylint)..."
	$(docker_run_tests) bash -c \
		"find ./$(project_name) -name '*.py' |  grep -v 'test' |  xargs pylint --rcfile .pylintrc || exit 1" || \
		exit 1

	echo ">>> LINTING TEST FILES (with pylint)..."
	$(docker_run_tests) bash -c \
		"find ./tests -name '*.py' |  xargs pylint --rcfile /$(project_name)/tests/.pylintrc || exit 1" || \
		exit 1

	echo "Yay! Your code is squeaky clean :)"

#### Tests

unit-test: docker-build-test-image
	$(docker_run_tests_python) pytest -s --cov-report term-missing --cov=cloudwatch_sns_to_slack tests/unit/

integration-test: docker-build-test-image
	$(docker_run_tests_python) pytest -s --cov-report term-missing --cov=cloudwatch_sns_to_slack tests/integration/

test: unit-test integration-test

#### Local development

run-dev:
	yarn dev:watch

sns-publish:
	python resources/sns_publish.py
