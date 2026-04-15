import io


def main():
    with open("poem.txt") as f:
        for line in f:
            print(line, end="")


if __name__ == "__main__":
    main()
