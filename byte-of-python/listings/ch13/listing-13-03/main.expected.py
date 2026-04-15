class ShortInputException(Exception):
    length = 0
    atleast = 0

    def __init__(self, length, atleast):
        self.length = length
        self.atleast = atleast

    def to_string(self):
        return f"ShortInputException: The input was {self.length} long, expected at least {self.atleast}"


def main():
    try:
        text = input("Enter something: ")
        if len(text) < 3:
            raise ShortInputException(len(text), 3)
        else:
            print("No exception was raised.")
    except ShortInputException as e:
        print(e.to_string())
    except EOFError:
        print("Why did you do an EOF on me?")
    else:
        print("OK")


if __name__ == "__main__":
    main()
