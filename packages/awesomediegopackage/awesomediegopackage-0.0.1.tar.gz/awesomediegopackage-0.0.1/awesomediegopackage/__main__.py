from awesomediegopackage.basic_arithmetic import somma, prodotto
from awesomediegopackage.advanced_arithmetic import potenza, radice

if __name__ == '__main__':
    print("This is the first package written and published by Diego Stucchi.")
    print("You can only perform trivial arithmetic operations")

    numbers = [1, 2, 3, 4, 5]
    exponent = 2
    print(f"The sum of the numbers in {numbers} is {somma(numbers)}")
    print(f"The product of the numbers in {numbers} is {prodotto(numbers)}")
    print(f"The square of the numbers in {numbers} is {potenza(numbers, exponent)}")
    print(f"The square root of the numbers in {numbers} is {radice(numbers, exponent)}")
