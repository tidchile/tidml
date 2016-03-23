VERSION=`cat VERSION`

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	rm -rf tidml.egg-info/
	rm -rf cover/
	rm -f .coverage

install: clean
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	clear
	python setup.py nosetests  --verbosity=2 --nocapture --rednose

test-watch:
	clear
	nosetests -v --nocapture --rednose --with-watch

coverage:
	python setup.py nosetests --with-coverage \
		--cover-package=tidml \
		--cover-inclusive \
		--cover-erase \
		--cover-html
	open cover/index.html

reqs:
	pipreqs . --force

register: clean
	python setup.py sdist bdist_wheel
	twine register dist/*

upload: clean
	python setup.py sdist bdist_wheel
	twine upload dist/*

tag:
	git tag $(VERSION) -m "Add tag for setup download_url"
