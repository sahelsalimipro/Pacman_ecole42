VENV = venv
ifeq ($(OS),Windows_NT)
	SYS_PYTHON = python
	PYTHON = $(VENV)\Scripts\python.exe
else
	SYS_PYTHON = python3
	PYTHON = $(VENV)/bin/python
endif

PIP = $(PYTHON) -m pip

SRC = src
MAIN = pac-man.py
CONFIGFILE = config.json
PACKAGE_NAME = pacman

# Member whose next task to show: make next WHO=A  (empty = everyone)
WHO ?=


.PHONY: install run debug clean lint lint-strict build next

run:
	$(PYTHON) $(MAIN) "$(CONFIGFILE)"

debug:
	$(PYTHON) -m pdb $(MAIN) "$(CONFIGFILE)"

# Real file target (NOT phony): make only creates the venv if it is missing
$(VENV)/pyvenv.cfg:
	@echo No virtual environment found, creating $(VENV)...
	$(SYS_PYTHON) -m venv $(VENV)

install: $(VENV)/pyvenv.cfg
	$(PIP) install --upgrade pip
	$(PIP) install mazegenerator/mazegenerator-2.1.0-py3-none-any.whl
	$(PIP) install -r requirements.txt

# Next unfinished task from PLANNING.md (stdlib only, no venv needed)
next:
	@$(SYS_PYTHON) dev/next_task.py $(WHO)

# WARNING: 'clean' relies on Unix 'find' and does NOT work on Windows
# (cmd.exe / PowerShell). Use WSL or a Linux machine for this rule.
# Note: OS=Windows_NT is also set inside Git Bash, so it is blocked there too.

ifeq ($(OS),Windows_NT)
clean lint lint-strict:
	$(error 'make $@' is not supported on Windows, use WSL)
else
clean:
	find . -type d -name "$(VENV)" -prune -o -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name "$(VENV)" -prune -o -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
	find . -type d -name "$(VENV)" -prune -o -type d \( -name ".mypy_cache" -o -name ".pytest_cache" -o -name ".ruff_cache" -o -name ".ipynb_checkpoints" \) -prune -exec rm -rf {} +
	find . -type d -name "$(VENV)" -prune -o -type d -name "*.egg-info" -prune -exec rm -rf {} +
	rm -rf .tox .nox .coverage htmlcov build dist .hypothesis
lint:
	$(VENV)/bin/flake8 . --exclude=$(VENV)
	$(VENV)/bin/mypy . --exclude '$(VENV)/' --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VENV)/bin/flake8 . --exclude=$(VENV)
	$(VENV)/bin/mypy . --exclude '$(VENV)/' --strict
endif

build:
	$(PIP) install --upgrade build
	$(PYTHON) -m build
	cp dist/$(PACKAGE_NAME)-*.whl .
