# coding: utf-8
import logging
from itertools import count

from pyparsing import alphas, alphanums, hexnums, cppStyleComment, delimitedList, dblQuotedString, \
    Suppress, Keyword, Word, Regex, Group, Optional, ZeroOrMore, ParseBaseException

log = logging.getLogger(__name__)

semi = Suppress(';')
token_lbra = Suppress('{')
token_rbra = Suppress('}')
token_type = Keyword('byte') | Keyword('word')
token_id = Word(alphas + '_', alphanums + '_')
token_integer = Regex(r'[+-]?\d+')
token_hex = Suppress('0x') + Word(hexnums)

const_array = Group(Suppress('[') + delimitedList(token_hex) + Suppress(']'))
const_value = token_integer | const_array

var = Group(token_type + delimitedList(Group(token_id + Optional('=' + const_value)))) + semi

call_func = Group(token_id + Suppress('()'))('call') + semi
set_register = Group(token_hex + '=' + const_value) + semi

body = ZeroOrMore(call_func | set_register | Group(dblQuotedString))

func = Group(Suppress('function') + token_id + Suppress('()') + token_lbra + Group(body) + token_rbra)('func')

const = Group(Suppress('const') + token_type +
              Group(delimitedList(
                  Group(token_id + '=' + const_value)
              )) + semi)('const')

program = ZeroOrMore(const | var | func)
program.ignore(cppStyleComment)


def main():
    text = '''\
    int a = 0;


    '''

    try:
        ast = program.parseString(text, parseAll=True)
    except ParseBaseException as e:
        log.error('\n'.join(('Parse error', e.line, ' ' * (e.column - 1) + '^', e.__str__())))
        return

    for i in ast:
        log.debug(i)

        Point = namedtuple('Point', ['x', 'y'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
