init:
	pip install -r requirements_dev.txt
	pip install -r requirements.txt

test:
	clear
	nosetests -v --nocapture --rednose

testw:
	clear
	nosetests -v --nocapture --rednose --with-watch

cov:
	nosetests --with-coverage \
		--cover-package=tidml \
		--cover-inclusive \
		--cover-branches \
		--cover-erase \
		--cover-html
	open cover/index.html

reqs:
	pipreqs . --force
