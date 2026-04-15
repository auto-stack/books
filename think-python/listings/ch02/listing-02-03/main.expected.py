def main():
    # Legal variable names
    my_name = "Alice"
    _private = 42
    item_count = 100
    speed2 = 60

    print(my_name)
    print(_private)
    print(item_count)
    print(speed2)

    # These would cause syntax errors:
    # 76trombones = "big parade"   # starts with a number
    # million! = 1000000           # contains punctuation
    # fn = "keyword"               # fn is a keyword (in Auto)


if __name__ == "__main__":
    main()
