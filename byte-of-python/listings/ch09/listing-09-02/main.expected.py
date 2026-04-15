def main():
    zoo = ("python", "elephant", "penguin")
    print(f"Number of animals in the zoo is {len(zoo)}")

    new_zoo = ("monkey", zoo, "dolphin")
    print(f"Number of cages in the new zoo is {len(new_zoo)}")
    print(f"All animals in new zoo are {new_zoo}")
    print(f"Animals brought from old zoo are {new_zoo[1]}")
    print(f"Last animal brought from old zoo is {new_zoo[1][2]}")
    print(f"Number of animals in the new zoo is {len(new_zoo) - 1 + len(new_zoo[1])}")


if __name__ == "__main__":
    main()
