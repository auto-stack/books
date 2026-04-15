def main():
    # Writing lines to a file
    writer = open("output.txt", "w")
    writer.write("First line\n")
    writer.write("Second line\n")
    writer.write("Third line\n")
    writer.close()

    # Reading lines from a file
    print("Contents of output.txt:")
    for line in open("output.txt"):
        stripped = line.strip()
        if len(stripped) > 0:
            print(stripped)

    # Find and replace in a file
    reader = open("output.txt")
    writer2 = open("output_replaced.txt", "w")
    for line in reader:
        new_line = line.replace("line", "row")
        writer2.write(new_line)
    reader.close()
    writer2.close()

    print("\nContents of output_replaced.txt:")
    for line in open("output_replaced.txt"):
        stripped = line.strip()
        if len(stripped) > 0:
            print(stripped)


if __name__ == "__main__":
    main()
