def main():
    ab = {"swaroop": 4098, "matz": 4139}
    print(f"ab is {ab}")

    ab["guido"] = 4127
    print(f"\nab is now {ab}")

    # delete a key-value pair
    # del ab["swaroop"]
    print(f"\nab is now {ab}")

    for name in ab.keys():
        print(f"Contact {name} at {ab[name]}")

    if "guido" in ab:
        addr = ab["guido"]
        print(f"\nguido's address is {addr}")


if __name__ == "__main__":
    main()
