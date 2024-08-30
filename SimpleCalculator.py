import re
import sys


def parse_equation(user_input):
    # Define a pattern of number
    # or operators
    pattern = r'\d+\.?\d*|[-+*/%]'

    matches = re.findall(pattern, user_input)

    # Convert numbers to floats
    matches = [float(x) if re.match(r'\d+\.?\d*', x)
               else x for x in matches]

    return matches


def calculate_expression(expression):
    # Process division, subtraction, and percentage first
    while any(operation in expression for operation in ['*', '/', '%']):
        for idx, val in enumerate(expression[:-1]):
            if val in ['*', '/', '%']:
                num1 = expression[idx - 1]
                num2 = None
                result = None
                if val != '%':
                    num2 = expression[idx + 1]

                if val == '*':
                    result = multiply(num1, num2)
                elif val == '/':
                    result = divide(num1, num2)
                elif val == '%':
                    result = percentage_of(num1)

                expression[idx - 1] = float(result)
                del expression[idx:idx + 2]
                break

    # Process addition and subtraction
    while len(expression) > 1:
        num1 = expression[0]
        num2 = expression[2]
        result = None

        if expression[1] == '+':
            result = add(num1, num2)
        elif expression[1] == '-':
            result = subtract(num1, num2)

        equation = [float(result)] + expression[3:]

    return expression[0]


def add(num1, num2):
    return num1 + num2


def subtract(num1, num2):
    return num1 - num2


def multiply(num1, num2):
    result = round(num1 * num2, 8)
    return f"{result:.8f}"


def divide(num1, num2):
    if num2 == 0:
        print("Error: Cannot divide by zero.")
        sys.exit(1)
    result = round(num1 / num2, 8)
    return f"{result:.8f}"


def percentage_of(num):
    result = round(num / 100, 8)
    return f"{result:.8f}"


def sign_inversion(number):
    return number * -1
