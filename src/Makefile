


hello:
	echo 'make build or make install or make all'

build: karls_chatgpt_helpers.py
	python3 setup.py sdist

install:
	pip3 install .

all: build install

clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/

