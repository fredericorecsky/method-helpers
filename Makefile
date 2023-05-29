APP=method-helper-gitsync

VERSION =? $(shell git branch | sed -n -e 's/^\* \(.*\)/\1/p')
PYTHON ?= $(shell which python3.10)

setup:
	touch requirements.txt \
	&& [ ! -d venv ] && $(PYTHON) -m venv venv  && source venv/bin/activate && python -m pip install -U pip && pip install --no-cache-dir -r requirements.txt
	@echo -------------------------
	@echo To start your python environement use:
	@echo  . /venv/bin/activate 
	@echo -------------------------