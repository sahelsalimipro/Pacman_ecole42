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
MAIN = testing.py
CONFIGFILE = config.json
PACKAGE_NAME = pacman

# Member whose next task to show: make next WHO=A  (empty = everyone)
WHO ?=


.PHONY: install run debug clean lint lint-strict build next

run:
	$(PYTHON) $(SRC)/$(MAIN) "$(CONFIGFILE)"

debug:
	$(PYTHON) -m pdb $(SRC)/$(MAIN) "$(CONFIGFILE)"

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
clean:
	ifeq ($(OS),Windows_NT)
		$(error 'make $@' is not supported on Windows because it relies on Unix find. Run it from WSL instead)
	else
		find . -type d -name "$(VENV)" -prune -o -type d -name "__pycache__" -prune -exec rm -rf {} +
		find . -type d -name "$(VENV)" -prune -o -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
		find . -type d -name "$(VENV)" -prune -o -type d \( -name ".mypy_cache" -o -name ".pytest_cache" -o -name ".ruff_cache" -o -name ".ipynb_checkpoints" \) -prune -exec rm -rf {} +
		find . -type d -name "$(VENV)" -prune -o -type d -name "*.egg-info" -prune -exec rm -rf {} +
		rm -rf .tox .nox .coverage htmlcov build dist .hypothesis
	endif

lint:
	ifeq ($(OS),Windows_NT)
		$(error 'make $@' is not supported on Windows because it relies on Unix find. Run it from WSL instead)
	else
		-$(VENV)/bin/flake8 . --exclude=$(VENV)
		$(VENV)/bin/mypy . --exclude '$(VENV)/' --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	ifeq ($(OS),Windows_NT)
		$(error 'make $@' is not supported on Windows because it relies on Unix find. Run it from WSL instead)
	else
		-$(VENV)/bin/flake8 . --exclude=$(VENV)
		$(VENV)/bin/mypy . --exclude '$(VENV)/' --strict

build:
	$(PIP) install --upgrade build
	$(PYTHON) -m build
	cp dist/$(PACKAGE_NAME)-*.whl .
