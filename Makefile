.PHONY: clean build install-test upload-test upload-prod
	
clean:
	rm -rf dist
	rm -rf build
	rm -rf cyclic_pattern.egg-info
build:
	python setup.py sdist bdist_wheel
install-test:
	pip install -e .
upload-test:
	twine upload --repository testpypi dist/*
upload-prod:
	twine upload --repository pypi dist/*
