import SimpleCalculator


def main():
    user_input = input("Enter an equation: ")

    # Parse user input into a list
    # of equation elements
    expression = SimpleCalculator.parse_equation(user_input)

    # Process tuple by precedence
    result = SimpleCalculator.calculate_expression(expression)
    if result.is_integer():
        print(f"= {int(result)}")
    else:
        print(f"= {result}")


if __name__ == "__main__":
    main()
