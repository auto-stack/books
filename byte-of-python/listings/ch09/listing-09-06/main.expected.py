def main():
    print("Making a copy of a list")
    mylist = ["a", "b", "c", "d"]
    print("mylist:", mylist)

    # Make a copy by doing a full slice
    mylist_copy = mylist[:]
    print("mylist_copy:", mylist_copy)

    # Remove an item from the copy
    del mylist_copy[0]
    print("mylist after removing first item:", mylist)
    print("mylist_copy after removing first item:", mylist_copy)


if __name__ == "__main__":
    main()
