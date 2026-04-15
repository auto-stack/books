import io


def main():
    # Write Unicode content
    f = open("unicode.txt", "w", encoding="utf-8")
    f.write("Imagine non-English language here")
    f.close()

    # Read Unicode content
    f = open("unicode.txt", encoding="utf-8")
    print(f.read())
    f.close()


if __name__ == "__main__":
    main()
