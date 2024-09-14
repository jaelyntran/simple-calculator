import re


def parse_equation(user_input):
    number_pattern = r'-?\d+\.?\d*'
    operator_pattern = r'[-+*/]'

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

    # Update patterns
    number_pattern = r'\d+\.?\d*'
    operator_pattern = r'[-+*/%]'
    pattern = f'{number_pattern}|{operator_pattern}'
    matches = re.findall(pattern, user_input)

    parsed_expression = []
    # Initialize a flag to check the previous character
    prev_was_operator = False
    neg_first_val = False
    for i, match in enumerate(matches):
        if re.match(operator_pattern, match):
            if prev_was_operator:
                if not (re.match(number_pattern, matches[i + 1])
                        and match == '-'):
                    msg = ('Invalid characters or format in input: \n'
                            + user_input + '\n'
                            + 'Only numerical values '
                              'and the following operators: \n'
                              '+, -, *, /, % are allowed\n'
                            + 'Please enter a new equation')
                    raise ValueError(msg)
                continue
            else:
                if i == 0 and re.match(number_pattern, matches[i + 1]):
                    neg_first_val = True
                    continue
                elif i + 1 < len(matches) and re.match(operator_pattern, matches[i + 1]):
                    prev_was_operator = True
                parsed_expression.append(match)
        elif re.match(number_pattern, match):
            if neg_first_val:
                parsed_expression.append(float(match) * -1)
                neg_first_val = False
            elif prev_was_operator:
                parsed_expression.append(float(match) * -1)
                prev_was_operator = False
            else:
                parsed_expression.append(float(match))

    print("Parsed Expression:", parsed_expression)  # Debugging line
    return parsed_expression


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
            expression = expression[:idx - 2] + [result] + expression[idx + 2:]
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

            # Update the expression list
            expression = expression[:idx - 1] + [result] + expression[idx + 1:]
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
