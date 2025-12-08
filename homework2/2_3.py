import math

class Graphic:
    def area(self):
        pass

    def perimeter(self):
        pass

    def compare_area(self, other):
        if self.area() > other.area():
            return "bigger"
        elif self.area() < other.area():
            return "smaller"
        else:
            return "equal"

    def compare_perimeter(self, other):
        if self.perimeter() > other.perimeter():
            return "bigger"
        elif self.perimeter() < other.perimeter():
            return "smaller"
        else:
            return "equal"


class Square(Graphic):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side


class Rectangle(Graphic):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Graphic):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        semi_perimeter = (self.a + self.b + self.c) / 2
        return math.sqrt(
            semi_perimeter * (semi_perimeter - self.a) * (semi_perimeter - self.b) * (semi_perimeter - self.c))

    def perimeter(self):
        return self.a + self.b + self.c


class Circle(Graphic):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * (self.radius ** 2)

    def perimeter(self):
        return 2 * math.pi * self.radius


square = Square(4)
rectangle = Rectangle(3, 4)
triangle = Triangle(3, 4, 5)
circle = Circle(5)

print(square.area())
print(triangle.perimeter())
print(circle.compare_area(rectangle))
print(rectangle.compare_perimeter(circle))