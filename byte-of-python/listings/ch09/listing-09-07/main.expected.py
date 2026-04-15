def main():
    name = "Swaroop"

    if name.startswith("Swa"):
        print("Yes, the string starts with 'Swa'")

    if "war" in name:
        print("Yes, it contains the string 'war'")

    if "xyz" in name:
        print("Yes, it contains the string 'xyz'")
    else:
        print("No, it does not contain 'xyz'")

    delim = "-*-"
    mylist = ["Brazil", "Russia", "India", "China"]
    print(delim.join(mylist))

    print(name.replace("oo", "aa"))

    print("This is a sentence".split())


if __name__ == "__main__":
    main()
