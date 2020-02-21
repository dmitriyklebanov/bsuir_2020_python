all: upload

test:
	pytest

build: clean test
	python setup.py sdist bdist_wheel

upload: build
	twine upload --repository testpypi dist/*

clean:
	git clean -fdX
