def print_twice(string):
    print(string)
    print(string)


def cat_twice(part1, part2):
    # cat is a local variable
    cat = part1 + part2
    print_twice(cat)
    # cat is destroyed when this function ends


def main():
    line1 = "Always look on the "
    line2 = "bright side of life."
    cat_twice(line1, line2)

    # This would be an error -- cat is local to cat_twice:
    # print(cat)

    # These would also be errors -- parameters are local:
    # print(part1)
    # print(part2)


if __name__ == "__main__":
    main()
