class Student:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return f"Student({self.name}, {self.age})"

    def __lt__(self, other: "Student") -> bool:
        return self.age < other.age


def main():
    s1 = Student("Alice", 20)
    s2 = Student("Bob", 22)

    print(s1)
    print(s2)


if __name__ == "__main__":
    main()
