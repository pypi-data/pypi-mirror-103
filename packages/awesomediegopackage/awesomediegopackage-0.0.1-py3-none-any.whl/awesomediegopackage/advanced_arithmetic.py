def potenza(base, exp):
    if type(base) == list:
        return [element ** exp for element in base]
    else:
        return base ** exp


def radice(base, exp):
    if type(base) == list:
        return [element ** (1/exp) for element in base]
    else:
        return base ** (1/exp)


if __name__ == '__main__':
    test_numbers = [1, 2, 3]
    test_exp = 3

    print(potenza(test_numbers, test_exp))
    print(radice(test_numbers, test_exp))
