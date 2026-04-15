import io


def main():
    try:
        f = open("poem.txt")
        # File is automatically closed
        for line in f:
            print(line, end="")
    except IOError:
        print("Could not find file poem.txt")
    finally:
        print("(Cleaning up: Closed the file)")


if __name__ == "__main__":
    main()
