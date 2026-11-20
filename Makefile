VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
SRC = src
MAIN = testing.py
CONFIGFILE = config.json


.PHONY: install run debug clean lint lint-strict build

run:
	$(PYTHON) $(SRC)/$(MAIN) "$(CONFIGFILE)"

debug:
	$(PYTHON) -m pdb $(SRC)/$(MAIN) "$(CONFIGFILE)"

install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "No virtual environment found, creating '$(VENV)'..."; \
		python3 -m venv $(VENV); \
	else \
		echo "Virtual environment '$(VENV)' found."; \
	fi
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

clean:
	find . -type d -name "$(VENV)" -prune -o -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name "$(VENV)" -prune -o -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
	find . -type d -name "$(VENV)" -prune -o -type d \( -name ".mypy_cache" -o -name ".pytest_cache" -o -name ".ruff_cache" -o -name ".ipynb_checkpoints" \) -prune -exec rm -rf {} +
	find . -type d -name "$(VENV)" -prune -o -type d -name "*.egg-info" -prune -exec rm -rf {} +
	rm -rf .tox .nox .coverage htmlcov build dist .hypothesis

lint:
	-$(VENV)/bin/flake8 . --exclude=$(VENV)
	$(VENV)/bin/mypy . --exclude '$(VENV)/' --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	-$(VENV)/bin/flake8 . --exclude=$(VENV)
	$(VENV)/bin/mypy . --exclude '$(VENV)/' --strict

build:
	$(PIP) install --upgrade build
	$(PYTHON) -m build
	cp dist/mazegen-*.whl .
