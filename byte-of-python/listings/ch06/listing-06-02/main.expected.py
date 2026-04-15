def main():
    running = True
    count = 0

    while running:
        print(count)
        count += 1
        if count >= 5:
            running = False


if __name__ == "__main__":
    main()
