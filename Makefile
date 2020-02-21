all: test build upload

test:
	pytest

build:
	python setup.py sdist bdist_wheel

upload:
	twine upload --repository testpypi dist/*

