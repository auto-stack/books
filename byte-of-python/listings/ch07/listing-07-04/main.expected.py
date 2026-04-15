def say(message, times=1):
    for i in range(0, times):
        print(message)


def main():
    say("Hello")
    say("World", 5)


if __name__ == "__main__":
    main()
