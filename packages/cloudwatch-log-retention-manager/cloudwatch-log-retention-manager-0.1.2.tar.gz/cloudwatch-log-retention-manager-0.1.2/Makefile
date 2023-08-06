clean:
	tox -e clean

build:
	tox -e build  # to build your package distribution

publish: clean build
	tox -e publish  # to test your project uploads correctly in test.pypi.org

publish-live: clean build
	tox -e publish -- --repository pypi  # to release your package to PyPI

tasks:
	tox -av  # to list all the tasks available

