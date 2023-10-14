.DEFAULT_GOAL := lint
sources = samuelcolvin_aicli.py

.PHONY: install
install:
	pip install -r requirements/linting.txt
	pre-commit install

.PHONY: format
format:
	black $(sources)
	ruff --fix-only $(sources)

.PHONY: lint
lint:
	ruff $(sources)
	black $(sources) --check --diff
