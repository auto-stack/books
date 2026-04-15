import sys


def main():
    print(f"Python version: {sys.version}")
    print(f"Version info: {sys.version_info}")

    if sys.version_info.major >= 3:
        print("You are running Python 3 or later.")
    else:
        print("You need to upgrade to Python 3!")


if __name__ == "__main__":
    main()
