.PHONY: install clean

install:
	virtualenv --system-site-packages --python=python2 env
	# . env/bin/activate;\
	# pip install -r requirements.txt

clean:
	find . -name '*.pyc' -exec rm --force {} +
