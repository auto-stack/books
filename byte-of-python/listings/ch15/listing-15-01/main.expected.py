def main():
    a = 5
    b = 8
    print(f"Before: a={a}, b={b}")

    # Swap using a temporary variable
    temp = a
    a = b
    b = temp
    print(f"After: a={a}, b={b}")

    # Tuple destructuring
    x, y = (10, 20)
    print(f"x={x}, y={y}")

    # Returning multiple values from a function
    error_num, error_msg = get_error_details()
    print(f"Error {error_num}: {error_msg}")


def get_error_details():
    return (2, "details")


if __name__ == "__main__":
    main()
