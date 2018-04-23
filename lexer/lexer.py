#!/usr/bin/python3

import sys
import re


class Lexeme:
    def __init__(self, line, start_index, end_index):
        self.line = line
        self.start_index = start_index
        self.end_index = end_index

    def __str__(self):
        return '{}:{}:{}'.format(self.line, self.start_index, self.end_index)


class Keyword(Lexeme):
    def __init__(self, line, start_index, end_index, keyword):
        super(Keyword, self).__init__(line, start_index, end_index)
        self.keyword = keyword

    def __str__(self):
        return 'Keyword({}, {})'.format(self.keyword, super(Keyword, self).__str__())


class Number(Lexeme):
    def __init__(self, line, start_index, end_index, number):
        super(Number, self).__init__(line, start_index, end_index)
        self.number = number

    def __str__(self):
        return 'Number({}, {})'.format(self.number, super(Number, self).__str__())


class Boolean(Lexeme):
    def __init__(self, line, start_index, end_index, value):
        super(Boolean, self).__init__(line, start_index, end_index)
        self.value = value

    def __str__(self):
        return 'Boolean({}, {})'.format(self.value, super(Boolean, self).__str__())


class Operator(Lexeme):
    def __init__(self, line, start_index, end_index, value):
        super(Operator, self).__init__(line, start_index, end_index)
        self.value = value

    def __str__(self):
        return 'Operator({}, {})'.format(self.value, super(Operator, self).__str__())


class Separator(Lexeme):
    def __init__(self, line, start_index, end_index, value):
        super(Separator, self).__init__(line, start_index, end_index)
        self.value = value

    def __str__(self):
        return 'Separator({}, {})'.format(self.value, super(Separator, self).__str__())


class Identifier(Lexeme):
    def __init__(self, line, start_index, end_index, value):
        super(Identifier, self).__init__(line, start_index, end_index)
        self.value = value

    def __str__(self):
        return 'Identifier(\'{}\', {})'.format(self.value, super(Identifier, self).__str__())


def split_by_many(s, seps):
    res = [s]
    for sep in seps:
        res = [subs.split(sep) for subs in res]
        res = [item for sublist in res for item in sublist]
    return res


def lex(filename, file):
    content = split_by_many(file, ['\r\n', '\n', '\r'])

    lexemes = []

    SPACE_CHARS = ' \t\f'
    ALPHA_CHARS = 'abcdefghijklmnopqrstuvwxyz'
    DIGIT_CHARS = '0123456789'
    OPERATOR_CHARS = '+-*/%=!><&|'
    SEPARATOR_CHARS = '();,'
    OTHER_CHARS = '_.'

    IDENTIFIER_CHARS = ALPHA_CHARS + DIGIT_CHARS + '_'
    ALLOWED_CHARACTERS = SPACE_CHARS + ALPHA_CHARS + DIGIT_CHARS +\
                         OPERATOR_CHARS + SEPARATOR_CHARS + OTHER_CHARS

    KEYWORDS = 'if then else while do read write'.split()
    BOOLEANS = 'true false'.split()

    OPERATORS_ONE_SYMBOL = '+ - * / % > <'.split()
    OPERATORS_TWO_SYMBOLS = '== != >= <= && ||'.split()

    MATCH_NUMBER = re.compile('^[-+]? *[0-9]+\.?[0-9]*(?:[Ee] *-? *[0-9]+)?')

    for i, line in enumerate(content):
        cur = 0
        for j, char in enumerate(line):
            if j < cur:
                continue
            if char.isspace():
                continue
            if char not in ALLOWED_CHARACTERS:
                print('{}:{}:{}:{}: unrecognized character: {}'.
                      format(filename, i, j, j, line[j]))
                return lexemes
            if char.isdigit() or char in '-+' and len(line) > j + 1 and line[j + 1].isdigit()\
                    and not (len(lexemes) > 0 and isinstance(lexemes[-1], Number)):
                # parse number greedy
                match = re.search(MATCH_NUMBER, line[j:])[0]
                cur = j + len(match)
                lexemes.append(Number(i, j, cur - 1, float(match)))
            elif char in OPERATOR_CHARS:
                # parse operator greedy
                if len(line) > j + 1 and line[j:j + 2] in OPERATORS_TWO_SYMBOLS:
                    lexemes.append(Operator(i, j, j + 1, line[j:j + 2]))
                    cur = j + 2
                elif line[j] in OPERATORS_ONE_SYMBOL:
                    lexemes.append(Operator(i, j, j, line[j]))
                else:
                    print('{}:{}:{}:{}: unexpected character: {}'.
                          format(filename, i, j, j, line[j]))
                    return lexemes

            elif char in SEPARATOR_CHARS:
                lexemes.append(Separator(i, j, j, line[j]))
            elif char in IDENTIFIER_CHARS:
                # parse identifier, keyword, or boolean literal greedy
                end = j + 1
                while len(line) < end and line[end] in IDENTIFIER_CHARS:
                    end += 1
                if line[j:end] in KEYWORDS:
                    lexeme = Keyword(i, j, end - 1, line[j:end])
                elif line[j:end] in BOOLEANS:
                    lexeme = Boolean(i, j, end - 1, line[j:end])
                else:
                    lexeme = Identifier(i, j, end - 1, line[j:end])
                lexemes.append(lexeme)
                cur = end
            else:
                print('{}:{}:{}:{}: unexpected character: {}'.
                      format(filename, i, j, j, line[j]))
                return lexemes

    return lexemes


def tests():
    good = ['', '1 + 2', '1+2', '1+-2', '-', '+', '&&', '123 abc', '123abc', 'abc123', 'abc 123', '+.004e5+4', 'read\nwrite', 'true+123', 'if+123'
             'read x; if y + 1 == x then write y else write x']
    bad = ['.', '..1', 'read A', '&', '& ', '!', '=', '= ']
    tests = good.copy()
    tests.extend(bad)

    for i, test in enumerate(tests):
        filename = 'test' + str(i)
        print(filename + ':' + test)
        lexemes = lex(filename, test)
        if lexemes:
            print([str(l) for l in lexemes])
        else:
            print(None)


def main():
    filename = sys.argv[1]
    with open(filename) as f:
        file = f.read()
    lex(filename, file)


if __name__ == '__main__':
    # tests()
    main()
