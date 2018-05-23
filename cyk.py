#!/usr/bin/python3

def in_language(input):
    n = len(input)
    if n == 0:
        return True

    # base = {
    #     'S': '0123456789',
    #     'E': '0123456789',
    #     'I': '-',
    #     'U': '*'
    # }
    #
    # step = {
    #     'S': ['EX', 'EY'],
    #     'E': ['EX', 'EY'],
    #     'X': ['IE'],
    #     'Y': ['UE']
    # }

    base = {
        'S': '0123456789',
        'H': '0123456789',
        'L': '0123456789',
        'D': '0123456789',
        'I': '-',
        'U': '*'
    }

    step = {
        'S': ['LA', 'HB'],
        'L': ['LA', 'HB'],
        'A': ['IH'],
        'H': ['HB'],
        'B': ['UD']
    }

    nt_set = set(list(base.keys()) + list(step.keys()))

    dp = dict()
    for nt in nt_set:
        dp[nt] = [[False] * n for _ in range(n)]

    for nt in base.keys():
        for t in base[nt]:
            for i, c in enumerate(input):
                if c == t:
                    dp[nt][i][i] = True

    for _ in range(n + 3):
        for A in step.keys():
            for i in range(n):
                for j in range(i + 1, n):
                    for rule in step[A]:
                        B, C = rule
                        for k in range(i, j):
                            dp[A][i][j] |= dp[B][i][k] and dp[C][k + 1][j]

    for nt in dp:
        print(nt)
        for lst in dp[nt]:
            print([1 if i else 0 for i in lst])
        print()
    return dp['S'][0][n - 1]


def test():
    assert in_language('')
    assert in_language('0')
    assert in_language('0*1')
    assert in_language('0*1-2-3*4*5')
    assert in_language('0-1')

    assert not in_language('1-')
    assert not in_language('1*')
    assert not in_language('11')
    assert not in_language('1*1-')
    assert not in_language('1*1-11')
    assert not in_language('1*1-11-')
    assert not in_language('1*1--1')


if __name__ == '__main__':
    # test()

    good = '0-1-2*3'
    print('Is {} in L?\n'.format(good))
    assert in_language(good)
    print(good, 'is in L')
    print('Tree: ')
    tree = """0-1-2*3
LIHIHUD
 --  --
 A   B
--- ---
L   H
   ----
   A
-------
S
    """
    print(tree)

    print('------------------------------\n')

    bad = '0-1-23*4'
    print('Is {} in L?\n'.format(bad))
    assert not in_language(bad)
    print(bad, 'is not in L')












