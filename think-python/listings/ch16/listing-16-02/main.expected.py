from copy import copy, deepcopy


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy


class Rectangle:
    def __init__(self, width, height, corner):
        self.width = width
        self.height = height
        self.corner = corner

    def __str__(self):
        return f"Rectangle({self.width}, {self.height}, {self.corner})"

    def grow(self, dwidth, dheight):
        self.width += dwidth
        self.height += dheight

    def translate(self, dx, dy):
        self.corner.translate(dx, dy)


def main():
    # Creating a Rectangle with a Point as its corner
    corner = Point(30.0, 20.0)
    box1 = Rectangle(100.0, 50.0, corner)
    print(box1)  # Rectangle(100.0, 50.0, Point(30.0, 20.0))

    # Shallow copy -- corner is shared
    box2 = copy(box1)
    print(box1 is box2)                  # False
    print(box1.corner is box2.corner)    # True (shared!)

    # Growing box2 does not affect box1
    box2.grow(60.0, 40.0)
    print(box1)  # Rectangle(100.0, 50.0, Point(30.0, 20.0))
    print(box2)  # Rectangle(160.0, 90.0, Point(30.0, 20.0))

    # Translating box2 moves its corner, which is shared with box1!
    box2.translate(30.0, 20.0)
    print(box1)  # Rectangle(100.0, 50.0, Point(60.0, 40.0))  <-- bug!
    print(box2)  # Rectangle(160.0, 90.0, Point(60.0, 40.0))

    # Deep copy -- corner is independent
    corner2 = Point(20.0, 20.0)
    box3 = Rectangle(100.0, 50.0, corner2)
    box4 = deepcopy(box3)
    print(box3.corner is box4.corner)    # False (independent!)

    box3.translate(50.0, 30.0)
    box4.grow(100.0, 60.0)
    print(box3)  # Rectangle(100.0, 50.0, Point(70.0, 50.0))
    print(box4)  # Rectangle(200.0, 110.0, Point(20.0, 20.0))


if __name__ == "__main__":
    main()
