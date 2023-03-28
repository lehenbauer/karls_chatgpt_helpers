


hello:
	echo 'make build or make install or make all'

build: src/karls_chatgpt_helpers.py
	python3 -m build

install:
	pip3 install --editable .

all: build install

clean:
	rm -rf build/ dist/ *.egg-info/

