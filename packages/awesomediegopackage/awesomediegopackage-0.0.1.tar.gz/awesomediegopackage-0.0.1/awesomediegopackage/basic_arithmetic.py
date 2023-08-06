def somma(*numbers):
    if len(numbers) == 0:
        return 0
    else:
        return sum(*numbers)


def prodotto(*numbers):
    if len(numbers) == 0:
        return 1
    else:
        result = 1
        for element in numbers[0]:
            result *= element
        return result


if __name__ == '__main__':
    test_numbers = [1, 2, 3, 4]
    print(somma(test_numbers))
    print(prodotto(test_numbers))
