import io


def main():
    poem = """\
Programming is fun
When the work is done
if you wanna make your work also fun:
    use Auto!"""

    # Open for 'w'riting
    f = open("poem.txt", "w")
    # Write text to file
    f.write(poem)
    # Close the file
    f.close()

    # If no mode is specified,
    # 'r'ead mode is assumed by default
    f = open("poem.txt")
    if f:
        print(f.read())
        f.close()


if __name__ == "__main__":
    main()
