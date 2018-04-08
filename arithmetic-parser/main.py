def tokenize(s):
    arithm = '+-*/^()'
    tokens = []
    reading_number = False
    for c in s:
        if c.isspace():
            reading_number = False
        elif c.isdigit():
            if reading_number:
                tokens[-1].append(c)
            else:
                tokens.append(c)
                reading_number = True
        elif c in arithm:
            tokens.append(c)
            reading_number = False
        else:
            raise Exception('Unknown symbol: ' + c)


def main():
    pass


if __name__ == '__main__':
    main()
