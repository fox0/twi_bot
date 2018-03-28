.PHONY: clean all

all:
	yacc doc/pattern.grammar.y

clean:
	find . -name '*.pyc' -exec rm --force {} +
