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


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"Line({self.p1}, {self.p2})"

    def __eq__(self, other):
        return ((self.p1 == other.p1 and self.p2 == other.p2) or
                (self.p1 == other.p2 and self.p2 == other.p1))

    def midpoint(self):
        mx = (self.p1.x + self.p2.x) / 2
        my = (self.p1.y + self.p2.y) / 2
        return Point(mx, my)


def main():
    # Creating Point objects
    start = Point(0.0, 0.0)
    print(start)  # Point(0.0, 0.0)

    end = Point(300.0, 150.0)
    print(end)    # Point(300.0, 150.0)

    # Equivalence vs identity
    p1 = Point(200.0, 100.0)
    p2 = Point(200.0, 100.0)
    print(p1 == p2)  # True  (equivalent)
    print(p1 is p2)  # False (different objects)

    # Translating a point
    end.translate(50.0, 25.0)
    print(end)  # Point(350.0, 175.0)

    # Composition: Line contains Point objects
    line1 = Line(start, end)
    print(line1)  # Line(Point(0.0, 0.0), Point(350.0, 175.0))

    # Line equivalence (order-independent)
    line2 = Line(end, start)
    print(line1 == line2)  # True

    # Midpoint of a line
    mid = line1.midpoint()
    print(mid)  # Point(175.0, 87.5)


if __name__ == "__main__":
    main()
