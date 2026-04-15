def draw_filled_box(ch, width, height):
    for i in range(height):
        for j in range(width):
            print(ch, end="")
        print()


def draw_empty_box(ch, width, height):
    for i in range(height):
        for j in range(width):
            if i == 0 or i == height - 1 or j == 0 or j == width - 1:
                print(ch, end="")
            else:
                print(" ", end="")
        print()


def make_row(ch, fill, width, is_edge):
    if is_edge:
        return ch * width
    else:
        return f"{ch}" + fill * (width - 2) + f"{ch}"


def draw_box_v2(ch, width, height, filled):
    fill = ch if filled else " "
    for i in range(height):
        is_edge = i == 0 or i == height - 1
        print(make_row(ch, fill, width, is_edge))


def main():
    # Before refactoring: two separate functions
    print("Filled box 5x3:")
    draw_filled_box("*", 5, 3)
    print()

    print("Empty box 5x3:")
    draw_empty_box("#", 5, 3)
    print()

    # After refactoring: one function with a parameter
    print("Filled box 5x3 (v2):")
    draw_box_v2("*", 5, 3, True)
    print()

    print("Empty box 5x3 (v2):")
    draw_box_v2("#", 5, 3, False)


if __name__ == "__main__":
    main()
