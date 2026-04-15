class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"Line({self.p1}, {self.p2})"

    def draw(self):
        print(f"Drawing line from ({self.p1.x}, {self.p1.y}) to ({self.p2.x}, {self.p2.y})")


class Rectangle:
    def __init__(self, width, height, corner):
        self.width = width
        self.height = height
        self.corner = corner

    def __str__(self):
        return f"Rectangle({self.width}, {self.height}, {self.corner})"

    def draw(self):
        p1 = self.corner
        p2 = Point(self.corner.x + self.width, self.corner.y)
        p3 = Point(self.corner.x + self.width, self.corner.y + self.height)
        p4 = Point(self.corner.x, self.corner.y + self.height)
        print(f"Drawing rectangle with corners ({p1.x},{p1.y}), ({p2.x},{p2.y}), ({p3.x},{p3.y}), ({p4.x},{p4.y})")


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __str__(self):
        return f"Circle(center={self.center}, radius={self.radius})"

    def draw(self):
        print(f"Drawing circle at ({self.center.x}, {self.center.y}) with radius {self.radius}")


def draw_shapes(shapes):
    for shape in shapes:
        shape.draw()


def main():
    origin = Point(0.0, 0.0)
    line1 = Line(origin, Point(300.0, 0.0))
    line2 = Line(origin, Point(0.0, 150.0))
    rect = Rectangle(100.0, 50.0, Point(30.0, 20.0))
    circle = Circle(Point(80.0, 45.0), 25.0)

    # Polymorphism: same interface, different types
    shapes = [line1, line2, rect, circle]
    draw_shapes(shapes)
    # Drawing line from (0.0, 0.0) to (300.0, 0.0)
    # Drawing line from (0.0, 0.0) to (0.0, 150.0)
    # Drawing rectangle with corners (30.0,20.0), (130.0,20.0), (130.0,70.0), (30.0,70.0)
    # Drawing circle at (80.0, 45.0) with radius 25.0


if __name__ == "__main__":
    main()
