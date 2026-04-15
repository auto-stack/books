def print_banner(text):
    border = "=" * (len(text) + 4)
    print(border)
    print(f"= {text} =")
    print(border)


def main():
    # Before encapsulation: repeated code
    print("=========")
    print("= Hello =")
    print("=========")
    print()
    print("===========")
    print("= Welcome =")
    print("===========")
    print()
    print("========")
    print("= Bye =")
    print("========")

    print()

    # After encapsulation: call a function
    print_banner("Hello")
    print()
    print_banner("Welcome")
    print()
    print_banner("Bye")


if __name__ == "__main__":
    main()
