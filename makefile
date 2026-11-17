VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
SCRIPT = simulation.py

.PHONY: all install run clean

all: run

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install numpy matplotlib

run:
	$(PYTHON) $(SCRIPT)

clean:
	rm -rf $(VENV) __pycache__ *.pyc

