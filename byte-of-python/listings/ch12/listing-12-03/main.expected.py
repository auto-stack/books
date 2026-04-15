import pickle


def main():
    shoplist = ["apple", "mango", "carrot"]

    # Write to file
    f = open("shoplist.data", "wb")
    pickle.dump(shoplist, f)
    f.close()

    # Read back from the storage
    f = open("shoplist.data", "rb")
    storedlist = pickle.load(f)
    print(storedlist)
    f.close()


if __name__ == "__main__":
    main()
