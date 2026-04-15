def main():
    try:
        text = input("Enter something: ")
    except EOFError:
        print("\nWhy did you do an EOF on me?")
    except KeyboardInterrupt:
        print("\nYou cancelled the operation.")
    else:
        print(f"You entered: {text}")


if __name__ == "__main__":
    main()
