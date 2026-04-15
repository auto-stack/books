# Python

def main():
    raw = "  Hello, World!  "
    trimmed = raw.strip()
    print(trimmed)

    greeting = "Hello, {}!".format("Auto")
    print(greeting)

    csv = "one,two,three,four"
    parts = csv.split(",")
    for part in parts:
        print(part)

    joined = " ".join(["Hello", "World"])
    print(joined)

    msg = "Hello, World!"
    print("World" in msg)
    print(msg.startswith("Hello"))
    print(msg.endswith("!"))
    print(msg.upper())
    print(msg.replace("World", "Auto"))

if __name__ == "__main__":
    main()
