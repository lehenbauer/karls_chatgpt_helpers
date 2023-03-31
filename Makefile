


hello:
	echo 'make build or make install or make all'

build: karls_chatgpt_helpers/helpers.py karls_chatgpt_helpers/chatgpt/__main__.py karls_chatgpt_helpers/gptshell/__main__.py
	python3 -m build

install:
	pip3 install --editable .

all: build install

clean:
	rm -rf build/ dist/ *.egg-info/

