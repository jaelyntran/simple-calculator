import SimpleCalculator


def main():
    user_input = input('Enter an equation: ')
    while user_input != '':
        try:
            #==============RUN SimpleCalculator.py==============
            #===================================================
            # Parse user input into a list
            # of equation elements
            expression = SimpleCalculator.parse_equation(user_input)

            # Process expression by precedence (PEMDAS)
            result = SimpleCalculator.calculate_expression(expression)

            # Print result
            if result.is_integer():
                print(f'= {int(result)}')
            else:
                print(f'= {result}')

            # Reprompt for new input
            # or enter to quit
            user_input = input('Enter a new equation or '
                               'press enter to quit: ')

        except ZeroDivisionError as e:
            print(f'Error: {e}.')
            user_input = input('Please enter a new equation '
                               'or press enter to quit: ')
        except ValueError as e:
            print(f'Invalid input: {e} in expression: {user_input}.')
            print('Only numerical values and the following operators:'
                  ' +, -, *, /, % are allowed.')
            user_input = input('Please enter a new equation '
                               'or press enter to quit: ')


if __name__ == '__main__':
    main()
