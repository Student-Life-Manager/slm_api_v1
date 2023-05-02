# Build configuration
# -------------------

APP_NAME := `sed -n 's/^ *name.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
APP_VERSION := `sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
GIT_REVISION = `git rev-parse HEAD`

# Introspection targets
# ---------------------

.PHONY: help
help: header targets

.PHONY: header
header:
	@echo "\033[34mEnvironment\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@printf "\033[33m%-23s\033[0m" "APP_NAME"
	@printf "\033[35m%s\033[0m" $(APP_NAME)
	@echo ""
	@printf "\033[33m%-23s\033[0m" "APP_VERSION"
	@printf "\033[35m%s\033[0m" $(APP_VERSION)
	@echo ""
	@printf "\033[33m%-23s\033[0m" "GIT_REVISION"
	@printf "\033[35m%s\033[0m" $(GIT_REVISION)
	@echo "\n"

.PHONY: targets
targets:
	@echo "\033[34mDevelopment Targets\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

# Development targets
# -------------

.PHONY: shell
shell: ## Start poetry shell
	poetry shell

.PHONY: install
install: ## Install dependencies
	poetry install

.PHONY: run
run: start

.PHONY: start
start: ## Starts the server
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))
	poetry run uvicorn main:app --reload

.PHONY: infra-up
infra-up: ## Start infrastructure (db, redis etc)
	docker-compose up -d

.PHONY: infra-down
infra-down: ## Stop infrastructure (db, redis etc)
	docker-compose down

# Check, lint and format targets
# ------------------------------

.PHONY: check
check: check-format lint

.PHONY: check-format
check-format: ## Dry-run code formatter
	poetry run black ./ --check
	poetry run isort ./ --profile black --check

.PHONY: lint
lint: ## Run linter
	poetry run pylint app/api/

.PHONY: format
format: ## Run code formatter
	poetry run black ./
	poetry run isort ./ --profile black

.PHONY: test
test:
	$(eval include .env.test)
	$(eval export $(sh sed 's/=.*//' .env.test))
	poetry run alembic upgrade head
	poetry run pytest ./app/tests $(FLAGS) --disable-pytest-warnings

.PHONY: db-migrate
db-migrate: ## Run the migrations
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))
	poetry run alembic upgrade head

.PHONY: db-rollback
db-rollback: ## Rollback migrations one level
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))
	poetry run alembic downgrade -1

.PHONY: db-reset
db-reset: ## Rollback all migrations
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))
	poetry run alembic downgrade base

.PHONY: db-generate-migration
db-generate-migration: ## Auto generate migration
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))
	poetry run alembic revision --autogenerate -m "$(m)"

.PHONY: ci/check
ci/check: check-format lint