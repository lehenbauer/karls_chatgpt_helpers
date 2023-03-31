

PROJ=karls_chatgpt_helpers
DIR=$(PROJ)

hello:
	echo 'make build or make install or make all'

build: $(DIR)/helpers.py $(DIR)/chatgpt/__main__.py $(DIR)/gptshell/__main__.py
	python3 -m build

devinstall:
	pip3 install --editable .

install: build
	pip3 install .

upload: build
	python3 -m twine upload dist/*

deinstall:
	pip3 uninstall $(PROJ)

all: build install

clean:
	rm -rf build/ dist/ *.egg-info/

