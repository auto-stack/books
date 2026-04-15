def main():
    list_one = [2, 3, 4]

    # Python list comprehension: concise and expressive
    list_two = [2 * i for i in list_one if i > 2]
    print(list_two)


if __name__ == "__main__":
    main()
