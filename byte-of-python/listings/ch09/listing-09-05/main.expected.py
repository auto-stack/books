def main():
    bri = {"brazil", "russia", "india"}
    print(f"'india' in bri: {'india' in bri}")
    print(f"'usa' in bri: {'usa' in bri}")

    bric = bri.copy()
    bric.add("china")
    print(f"bric is {bric}")
    print(f"bric is superset of bri: {bric.issuperset(bri)}")

    bri.remove("russia")
    print(f"bri is now {bri}")

    # intersection
    common = bri.intersection(bric)
    print(f"bri & bric is {common}")


if __name__ == "__main__":
    main()
