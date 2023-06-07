CURRENT_VERSION := $(shell poetry version -s)
DOCKER_NAME := boavizta/boaviztapi:${CURRENT_VERSION}
SEMVERS := major minor patch

clean:
		find . -name "*.pyc" -exec rm -rf {} \;
		rm -rf dist *.egg-info __pycache__

install: install_pip

install_pip:
		poetry install --with dev

test:
		poetry run pytest

run:
		poetry run uvicorn boaviztapi.main:app

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

