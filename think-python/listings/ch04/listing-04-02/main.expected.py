def draw_row(ch, width):
    print(ch * width)


def draw_box(ch, width, height):
    draw_row(ch, width)
    for i in range(height - 2):
        print(f"{ch}" + " " * (width - 2) + f"{ch}")
    if height > 1:
        draw_row(ch, width)


def draw_centered_box(ch, width, height, canvas_width):
    padding = (canvas_width - width) // 2
    for i in range(height):
        print(" " * padding + draw_row_str(ch, width))


def draw_row_str(ch, width):
    return ch * width


def main():
    # Simple row
    print("Simple row:")
    draw_row("*", 10)
    print()

    # Box
    print("Box 5x3:")
    draw_box("#", 5, 3)
    print()

    # Centered box on a wider canvas
    print("Centered box 7x3 on canvas of 15:")
    draw_centered_box("+", 7, 3, 15)


if __name__ == "__main__":
    main()
