def total(*numbers):
    print("a", numbers[0] if numbers else 5)

    # iterate through all the items in tuple
    for single_item in numbers[1:]:
        print("single_item", single_item)

    print("The sum is", sum(numbers))


def main():
    total(10, 1, 2, 3)
    print("---")
    total()
