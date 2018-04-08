import sys

class Tree:
    token = None
    left = None
    right = None

    def __init__(self, token, left, right):
        self.token = token
        self.left = left
        self.right = right

    def __str__(self):
        return '({}: {}, {})'.format(self.token, self.left, self.right)


def tokenize(s):
    arithm = '+-*/^()'
    tokens = []
    reading_number = False
    for c in s:
        if c.isspace():
            reading_number = False
        elif c.isdigit():
            if reading_number:
                tokens[-1] += c
            else:
                tokens.append(c)
                reading_number = True
        elif c in arithm:
            tokens.append(c)
            reading_number = False
        else:
            raise Exception('Unknown symbol: ' + c)
    return tokens


def find_first_symbol_outside_parenthesis(symbols, tokens, reverse_tokens=True):
    balance = 0
    ordered_tokens = reversed(list(enumerate(tokens))) if reverse_tokens else enumerate(tokens)
    for i, e in ordered_tokens:
        if e == '(':
            balance += 1
        elif e == ')':
            balance -= 1
        elif balance == 0 and e in symbols:
            return i
    return -1


def parse_lp(tokens):
    i = find_first_symbol_outside_parenthesis('+-', tokens)
    if i == -1:
        return parse_mp(tokens)
    return Tree(tokens[i], parse_lp(tokens[:i]), parse_mp(tokens[i + 1:]))


def parse_mp(tokens):
    i = find_first_symbol_outside_parenthesis('*/', tokens)
    if i == -1:
        return parse_hp(tokens)
    return Tree(tokens[i], parse_mp(tokens[:i]), parse_hp(tokens[i + 1:]))


def parse_hp(tokens):
    i = find_first_symbol_outside_parenthesis('^', tokens, reverse_tokens=False)
    if i == -1:
        return parse_op(tokens)
    return Tree(tokens[i], parse_op(tokens[:i]), parse_hp(tokens[i + 1:]))


def parse_op(tokens):
    if len(tokens) == 1:
        try:
            num = int(tokens[0])
            return Tree(num, None, None)
        except:
            print(tokens)
            raise Exception('Incorrect operand: ' + ' '.join(tokens))
    if len(tokens) < 3:
        raise Exception('Incorrect operand: ' + ' '.join(tokens))
    if tokens[0] != '(' or tokens[-1] != ')':
        raise Exception('Incorrect operand: ' + ' '.join(tokens))
    return parse_lp(tokens[1:-1])


def parse(s):
    return parse_lp(tokenize(s))


def test():
    parse('0 + 13 * 42 - 7 / 0')
    parse('(0 + 13) * ((42 - 7) / 0)')
    parse('1 - 2 - 3 - (5 - 6)')
    parse('13')
    parse('(((((13)))))')
    parse('42 ^ 24 - 156 * 123')
    parse('(42 ^ (24 - 156) * 123)')

    test_fails('-1')
    test_fails('((1)')
    test_fails('1^2^')

def test_fails(s):
    ok = False
    try:
        parse(s)
        ok = True
    except:
        pass
    if ok:
        raise Exception('Tests: Incorrect test has passed.')


def main():
    test()

    with open(sys.argv[1]) as f:
        s = f.readline()
        t = parse(s)
        print(t)


if __name__ == '__main__':
    main()
