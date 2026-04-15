class Point:
    pass


class Rectangle:
    pass


def print_point(p):
    print(f"({p.x}, {p.y})")


def print_rect(box):
    print(f"Corner: ({box.corner.x}, {box.corner.y})")
    print(f"Width: {box.width}, Height: {box.height}")


def find_center(box):
    cx = box.corner.x + box.width / 2
    cy = box.corner.y + box.height / 2
    result = Point()
    result.x = cx
    result.y = cy
    return result


def grow_rectangle(box, dwidth, dheight):
    result = Rectangle()
    result.corner = box.corner
    result.width = box.width + dwidth
    result.height = box.height + dheight
    return result


def main():
    # Creating a Point
    origin = Point()
    origin.x = 0.0
    origin.y = 0.0

    # Creating a Rectangle (objects as fields)
    box = Rectangle()
    box.corner = origin
    box.width = 100.0
    box.height = 200.0
    print_rect(box)

    # Function returning an object
    center = find_center(box)
    print("Center:")
    print_point(center)  # (50.0, 100.0)

    # Growing the rectangle returns a new object
    grown = grow_rectangle(box, 50.0, 100.0)
    print_rect(grown)

    # Original is unchanged
    print_rect(box)


if __name__ == "__main__":
    main()
