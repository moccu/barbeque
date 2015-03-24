.PHONY: tests coverage coverage-html devinstall tox docs clean
APP=.
COV=barbeque
OPTS=

help:
	@echo "tests - run all tests"
	@echo "coverage - run all tests with coverage enabled"
	@echo "coverage-html - run all tests with coverage html export enabled"
	@echo "devinstall - install all packages required for development"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "clean - Clean build related files"

tests:
	py.test ${OPTS} ${APP}

coverage:
	py.test --cov=${COV} --cov-report=term-missing ${OPTS} ${APP}

coverage-html:
	py.test --cov=${COV} --cov-report=html ${OPTS} ${APP}

devinstall:
	pip install -e .
	pip install -e .[docs]
	pip install -e .[tests]

docs: clean
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr htmlcov/
	$(MAKE) -C docs clean
