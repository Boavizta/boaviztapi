CURRENT_VERSION := $(shell poetry version -s || sed -n '3s/.*version = "\(.*\)"/\1/p' pyproject.toml)
TIMESTAMP := $(shell date "+%m-%d-%y")
DOCKER_NAME := boavizta/boaviztapi:${CURRENT_VERSION}
SEMVERS := major minor patch

clean:
		find . -name "*.pyc" -exec rm -rf {} \;
		rm -rf dist *.egg-info __pycache__

install: install_pip

install_pip:
		poetry install --with dev

check-csv:
		poetry run python3 validate_csv.py

test:
		poetry run pytest

test-e2e:
		poetry run pytest --rune2e

lint:
		poetry run ruff check

lint-fix:
		poetry run ruff check --fix

format:
		poetry run ruff format

format-check:
		poetry run ruff format --check

pre-commit-install:
		poetry run pre-commit install

pre-commit:
		poetry run pre-commit run --all-files

run:
		poetry run uvicorn boaviztapi.main:app --port 5000

run-py:
		python boaviztapi/main.py

run-doc:
		cd docs && poetry run mkdocs serve

$(SEMVERS):
		poetry version $@
		$(MAKE) npm_version
		$(MAKE) tag_version

npm_version:
		npm version --no-git-tag-version ${CURRENT_VERSION}

tag_version:
		git commit -m "release: bump to ${CURRENT_VERSION}" pyproject.toml package.json package-lock.json
		git tag ${CURRENT_VERSION}

build:
		poetry build

distribute:
		poetry config pypi-token.pypi ${API_TOKEN}
		poetry publish --build

docker-build:
		docker build -t $(DOCKER_NAME) .

docker-build-development:
		docker build -t boavizta/boaviztapi:${TIMESTAMP} .

docker-run-development:
		docker run -p 5000:5000 boavizta/boaviztapi:${TIMESTAMP}

compose-build:
		docker compose build

compose-up:
		docker compose up --build
