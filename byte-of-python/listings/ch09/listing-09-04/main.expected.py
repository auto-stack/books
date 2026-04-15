def main():
    shoplist = ["apple", "mango", "carrot", "banana"]

    # Indexing or 'subscription' operation
    print("Item 0 is:", shoplist[0])
    print("Item 1 is:", shoplist[1])
    print("Item 2 is:", shoplist[2])
    print("Item 3 is:", shoplist[3])
    print("Item -1 is:", shoplist[-1])
    print("Item -2 is:", shoplist[-2])

    # Slicing on a list
    print("Item 1 to 3 is:", shoplist[1:3])
    print("Item 2 to end is:", shoplist[2:])
    print("Item 1 to -1 is:", shoplist[1:-1])
    print("Item start to end is:", shoplist[:])

    # Slicing with step
    print("Item 1 to 3 step 1 is:", shoplist[1:3:1])
    print("Item start to end step 2 is:", shoplist[::2])
    print("Item start to end step 3 is:", shoplist[::3])
    print("Item reversed is:", shoplist[::-1])


if __name__ == "__main__":
    main()
