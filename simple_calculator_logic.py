import re


def parse_equation(user_input):
    number_pattern = r'-?\d+\.?\d*'
    operator_pattern = r'[-+*/]'
    percentage = r'%'

    # Define a pattern to match the entire input
    # 1. Number with optional percentage sign
    # 2. Operator with optional spaces around
    # 3. Zero or more sequences of operators,
    # followed by numbers with optional % signs.
    valid_pattern = r'^' + number_pattern + r'%?' \
                    + r'(?:\s*' + operator_pattern + r'\s*' \
                    + number_pattern + r'%?' + r')*$'

    if not re.fullmatch(valid_pattern, user_input):
        msg = ('Invalid characters or format in input: \n'
               + user_input + '\n'
               + 'Only numerical values '
                 'and the following operators: \n'
                 '+, -, *, /, % are allowed\n'
               + 'Please enter a new equation')
        raise ValueError(msg)

    # Define a pattern of number
    # or operators
    pattern = f'{number_pattern}|{operator_pattern}|{percentage}'
    matches = re.findall(pattern, user_input)

    # Convert numbers to floats
    matches = [float(x) if re.match(number_pattern, x)
               else x for x in matches]

    return matches


def calculate_expression(expression):
    # Process percentage
    expression = percentage_conversion(expression)

    # Process division and multiplication
    idx = 0
    while idx < len(expression):
        val = expression[idx]
        if val in ['*', '/']:
            num1 = expression[idx - 1]
            num2 = expression[idx + 1]
            result = None

            if val == '*':
                result = multiply(num1, num2)
            elif val == '/':
                result = divide(num1, num2)

            # Update the expression list
            del expression[idx:idx + 2]  # Remove the operator and the number after it
            expression[idx - 1] = float(result)
            idx = max(0, idx - 1)  # Reset index to recheck current position
        else:
            idx += 1

    # Process addition and subtraction
    while len(expression) > 1:
        num1 = expression[0]
        num2 = expression[2]
        result = None

        if expression[1] == '+':
            result = add(num1, num2)
        elif expression[1] == '-':
            result = subtract(num1, num2)

        expression = [float(result)] + expression[3:]

    return expression[0]


def percentage_conversion(expression):
    idx = 0
    while idx < len(expression):
        val = expression[idx]
        if val in ['%']:
            num = expression[idx - 1]
            result = round(num / 100, 8)
            expression.pop(idx)

            # Update the expression list
            expression[idx - 1] = float(result)
            idx = max(0, idx - 1)  # Reset index to recheck current position
        else:
            idx += 1
    return expression


def add(num1, num2):
    return float(num1 + num2)


def subtract(num1, num2):
    return float(num1 - num2)


def multiply(num1, num2):
    return round(float(num1 * num2), 8)


def divide(num1, num2):
    if num2 == 0:
        msg = ('Cannot divide by zero\n'
               + 'Please enter a new equation')
        raise ZeroDivisionError(msg)
    return round(float(num1 / num2), 8)
