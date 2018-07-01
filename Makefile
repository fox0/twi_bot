.PHONY: install clean

install:
	virtualenv --system-site-packages --python=python2 venv
	# . env/bin/activate;\
	# pip install -r requirements.txt

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.o' -exec rm --force {} +
	find . -name '*.so' -exec rm --force {} +
