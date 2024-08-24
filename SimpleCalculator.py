def addition(number1, number2):
    return number1 + number2
def subtraction(number1, number2):
    return number1 - number2

def multiplication(number1, number2):
    result = round(number1 * number2, 8)
    return f"{result:.8f}"

def division(number1, number2):
    result = round(number1 / number2, 8)
    return f"{result:.8f}"

def percentage(number):
    result = round(number / 100, 8)
    return f"{result:.8f}"

def sign_inversion(number):
    return number * -1

