CURRENT_VERSION := $(shell poetry version -s || sed -n '3s/.*version = "\(.*\)"/\1/p' pyproject.toml)
TIMESTAMP := $(shell date "+%m-%d-%y")
DOCKER_NAME := boavizta/boaviztapi:${CURRENT_VERSION}
SEMVERS := major minor patch

.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help message
		@echo "Available commands:"
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: ## Remove Python bytecode files and build artifacts
		find . -name "*.pyc" -exec rm -rf {} \;
		rm -rf dist *.egg-info __pycache__

install: install_pip ## Install project dependencies

install_pip: ## Install dependencies using Poetry
		poetry install --with dev

check-csv: ## Validate CSV data files
		poetry run python3 validate_csv.py

test: ## Run unit tests
		poetry run pytest

test-e2e: ## Run end-to-end tests
		poetry run pytest --rune2e

lint: ## Run linting checks with ruff
		poetry run ruff check

lint-fix: ## Run linting checks and auto-fix issues
		poetry run ruff check --fix

format: ## Format code with ruff
		poetry run ruff format

format-check: ## Check code formatting without making changes
		poetry run ruff format --check

pre-commit-install: ## Install pre-commit hooks
		poetry run pre-commit install

pre-commit: ## Run pre-commit hooks on all files
		poetry run pre-commit run --all-files

run: ## Run API server with uvicorn on port 5000
		poetry run uvicorn boaviztapi.main:app --port 5000

run-py: ## Run API server with Python
		python boaviztapi/main.py

run-doc: ## Run documentation server
		cd docs && poetry run mkdocs serve

$(SEMVERS): ## Bump version (use: make major|minor|patch)
		poetry version $@
		$(MAKE) npm_version
		$(MAKE) tag_version

npm_version: ## Update package.json version to match Poetry version
		npm version --no-git-tag-version ${CURRENT_VERSION}

tag_version: ## Create git tag for current version
		git commit -m "release: bump to ${CURRENT_VERSION}" pyproject.toml package.json package-lock.json
		git tag ${CURRENT_VERSION}

build: ## Build Python package with Poetry
		poetry build

distribute: ## Publish package to PyPI
		poetry config pypi-token.pypi ${API_TOKEN}
		poetry publish --build

docker-build: ## Build Docker image with version tag
		docker build -t $(DOCKER_NAME) .

docker-build-development: ## Build Docker image with timestamp tag
		docker build -t boavizta/boaviztapi:${TIMESTAMP} .

docker-run-development: ## Run development Docker container
		docker run -p 5000:5000 boavizta/boaviztapi:${TIMESTAMP}

compose-build: ## Build Docker Compose services
		docker compose build

compose-up: ## Build and start Docker Compose services
		docker compose up --build
