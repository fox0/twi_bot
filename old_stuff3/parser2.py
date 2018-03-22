# coding: utf-8
from twi_bot.tokenizer import tokenizer, ParseError


def main():
    with open('patterns/example1.conf') as f:
        text = f.read()

    def e_s():
        tokid, tokval = next(s)
        if tokid in ('COMMENT1', 'NEWLINE'):
            return
        elif tokid == 'ID':
            if tokval == 'function':
                raise NotImplementedError
            elif tokval == 'bot':
                e_act()
            else:
                e_id(tokval)
        else:
            raise NotImplementedError(tokid)

    def e_id(name_id):
        tokid, tokval = next(s)
        if tokid == '=':
            raise NotImplementedError(tokid)
        raise NotImplementedError(tokid)

    def e_act():
        tokid, tokval = next(s)
        if tokid != 'ID' or tokval != 'bot':
            raise ParseError('Ожидалось %s, найдено: %s' % ('bot', tokval))
        raise NotImplementedError(tokid)

    s = tokenizer(text)
    result = []
    tabs = 0
    try:
        while True:
            e_s()
    except StopIteration:
        print(result)


if __name__ == '__main__':
    main()
