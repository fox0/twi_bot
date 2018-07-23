installenv:
	virtualenv --never-download --python=python2 venv;\
	. venv/bin/activate;\
	pip install -U -r requirements.txt

cleanvenv:
	rm -rf venv

clean:
	rm -rf twi_bot2/cache/*
	touch twi_bot2/cache/__init__.py
	find . -name '*.pyc' -exec rm --force {} +
