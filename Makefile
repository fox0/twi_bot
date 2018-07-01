.PHONY: installenv cleanenv clean

installenv:
	virtualenv --never-download --python=python2 venv;\
	. venv/bin/activate;\
	pip install -U -r requirements.txt

cleanvenv:
	rm -rf venv

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.o' -exec rm --force {} +
	find . -name '*.so' -exec rm --force {} +

runjupyter:
	jupyter-notebook --no-browser
